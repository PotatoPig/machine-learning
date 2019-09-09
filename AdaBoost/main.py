from numpy import *
from BuildStump import build_stump, get_stump_classify
from WatermelonDataSet_3 import createDataSet
from AdaBoost import AdaBoost, adaboost_classify


def loadDataSet(fileName):  # general function to parse tab -delimited floats
    numFeat = len(open(fileName).readline().split('\t'))  # get number of fields
    dataMat = []
    labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = []
        curLine = line.strip().split('\t')
        for i in range(numFeat - 1):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat, labelMat


if __name__ == '__main__':
    datArr, labelArr = loadDataSet('horseColicTraining2.txt')
    AdaBoostClassifier = AdaBoost(datArr, labelArr, numIt=10)

    testdatArr, testLabelArr = loadDataSet('horseColicTraining2.txt')
    prediction = adaboost_classify(testdatArr, AdaBoostClassifier)

    num = len(testLabelArr)
    errorArr = mat(ones((num, 1)))
    predict_error = errorArr[prediction != mat(testLabelArr).T].sum()
    errorRate = float(predict_error) / float((num))
    print("the errorRate is: %.2f", errorRate)
