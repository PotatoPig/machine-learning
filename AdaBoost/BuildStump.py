from numpy import *
from WatermelonDataSet_3 import createDataSet


def loadSimpData():
    dataMat=matrix([[1. ,2.1],
        [2. ,1.1],
        [1.3,1. ],
        [1. ,1. ],
        [2. ,1. ]])
    classLabels=[1.0,1.0,-1.0,-1.0,1.0]
    return dataMat,classLabels


def get_stump_classify(dataset, feature, thresh, classify_mode):
    res_classify = ones((shape(dataset)[0], 1))
    if classify_mode == 'low_negative':
        res_classify[dataset[:, feature] <= thresh] = -1.0
    elif classify_mode == 'high_negative':
        res_classify[dataset[:, feature] >= thresh] = -1.0
    return res_classify


def build_stump(dataset, labels, DataWeight):
    dataMatrix = mat(dataset)
    labelMatrix = mat(labels).T

    m, num_feature = shape(dataMatrix)
    num_steps = 10.0
    DTstump = {}
    bestStumpClass = mat(zeros((m, 1)))

    min_error = inf
    for i in range(num_feature):
        minValue = dataMatrix[:, i].min()
        maxValue = dataMatrix[:, i].max()
        step_length = (maxValue - minValue) / num_steps
        for j in range(-1, int(num_steps)+1):
            for mode in ['low_negative', 'high_negative']:
                thresh = minValue + float(j) * step_length
                predict = get_stump_classify(dataMatrix, i, thresh, mode)
                error = mat(ones((m, 1)))
                error[predict == labelMatrix] = 0
                cur_error = DataWeight.T * mat(error)
                # print(cur_error)
                if cur_error < min_error:
                    min_error = cur_error
                    bestStumpClass = predict.copy()
                    DTstump['feature'] = i
                    DTstump['thresh'] = thresh
                    DTstump['mode'] = mode
    return DTstump, min_error, bestStumpClass


if __name__ == '__main__':
    dataSet, features, labels = createDataSet()
    m = len(labels)
    DataWeight = mat(ones((m, 1))/m)
    a, b, c = build_stump(dataSet, labels, DataWeight)
    print(a)
    print(b)
    print(c)
