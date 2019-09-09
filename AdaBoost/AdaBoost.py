from numpy import *
from BuildStump import build_stump, get_stump_classify
from WatermelonDataSet_3 import createDataSet


def AdaBoost(dataset, labels, numIt=5):
    baselearner = []
    m = shape(dataset)[0]
    DataWeight = mat(ones((m, 1)) / m)
    aggClassEst = mat(zeros((m, 1)))
    for i in range(numIt):
        DTstump, error, classEst = build_stump(dataset, labels, DataWeight)
        # print("DataWeight:", DataWeight.T)
        if error > 0.5:
            break
        alpha = float(0.5*log((1.0-error)/(max(error, 1e-16))))
        DTstump['alpha'] = alpha
        baselearner.append(DTstump)

        expon = multiply(-1 * alpha * mat(labels).T, classEst)
        DataWeight = multiply(DataWeight, exp(expon))
        DataWeight = DataWeight / DataWeight.sum()

        aggClassEst += alpha * classEst
        aggErrors = multiply(sign(aggClassEst) != mat(labels).T, ones((m, 1)))
        errorRate = aggErrors.sum() / m
        print("total error:", errorRate, "\n")
        if errorRate == 0:
            break
    return baselearner


def adaboost_classify(testdata, boost_classifier):
    dataMatrix = mat(testdata)
    m = shape(dataMatrix)[0]
    aggClassEst = mat(zeros((m, 1)))
    for classifier in range(len(boost_classifier)):
        res_class = get_stump_classify(dataMatrix, boost_classifier[classifier]['feature'],
                                                   boost_classifier[classifier]['thresh'],
                                                   boost_classifier[classifier]['mode'])
        aggClassEst += boost_classifier[classifier]['alpha'] * res_class
    return sign(aggClassEst)


if __name__ == '__main__':
    dataSet, features, labels = createDataSet()
    AdaBoost(dataSet, labels, numIt=10)
