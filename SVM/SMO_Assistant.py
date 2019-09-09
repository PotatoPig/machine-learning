import random
from KernelMethods import calculate_kernel_element
import numpy as np
import math


# data process(separate the data and label)
def data_separate(data_set):
    data_box = []
    label_box = []
    for i in data_set:
        data_box.append(i[:-1])
        label_box.append(i[-1])
    return data_box, label_box


# choose another alpha by random
def random_select_alphaj(i, SmoDS):
    j = i
    while j == i:
        j = int(random.uniform(0, SmoDS.dataAmount))
    e_j = calculate_e_xk(SmoDS, j)
    return j, e_j


def alphaj_boundary(labeli, labelj, alphai_old, alphaj_old, C):
    if labeli != labelj:
        L = max(0, alphaj_old - alphai_old)
        H = min(C, C + alphaj_old - alphai_old)
    else:
        L = max(0, alphaj_old + alphai_old - C)
        H = min(C, alphaj_old + alphai_old)
    return L, H


# limitation while optimize the parameter
def limit_alpha(alpha, upper, lower):
    if alpha > upper:
        alpha = upper
    elif alpha < lower:
        alpha = lower
    return alpha


# data structure
class SmoDataStructure:
    def __init__(self, data, label, C, tolerance, kernel):
        self.data = data
        self.label = label
        self.C = C
        self.tolerance = tolerance
        self.kernel = kernel

        self.dataAmount = np.shape(self.data)[0]  # amount of data
        self.dataSize = np.shape(self.data)[1]
        self.b = 0
        self.alphas = np.mat(np.zeros((self.dataAmount, 1)))
        self.errorCache = np.mat(np.zeros((self.dataAmount, 2)))
        self.KernelMatrix = np.mat(np.zeros((self.dataAmount, self.dataAmount)))
        for i in range(self.dataAmount):
            for j in range(self.dataAmount):
                self.KernelMatrix[i, j] = calculate_kernel_element(data[i], data[j], kernel=kernel)


# get the predict error of Kth data
def calculate_e_xk(SmoDS, k):
    f_xk = float(np.multiply(SmoDS.alphas, SmoDS.label).T*SmoDS.KernelMatrix[:, k] + SmoDS.b)
    e_xk = f_xk - float(SmoDS.label[k])
    return e_xk


def update_e_xk(SmoDS, k):
    e_xk = calculate_e_xk(SmoDS, k)
    SmoDS.errorCache[k] = [1, e_xk]


def max_select_alphaj(SmoDS, i, e_xi):
    max_index = -1
    max_delta_e = -1
    e_xj = 0
    SmoDS.errorCache[i] = [1, e_xi]

    optional_alphaj_list = np.nonzero(SmoDS.errorCache[:, 0].A)[0]
    if len(optional_alphaj_list) > 0:
        for k in optional_alphaj_list:
            if k == i:
                continue
            e_xk = calculate_e_xk(SmoDS, k)
            delta_eij = abs(e_xk - e_xi)
            if delta_eij > max_delta_e:
                max_index = k
                max_delta_e = delta_eij
                e_xj = e_xk
        return max_index, e_xj
    else:
        max_index, e_xj = random_select_alphaj(i, SmoDS.dataAmount)
        return max_index, e_xj


def break_KKT(SmoDS, i):
    e_i = calculate_e_xk(SmoDS, i)
    if (e_i * SmoDS.label[i] < -SmoDS.tolerance and SmoDS.alphas[i] < SmoDS.C) or \
       (e_i * SmoDS.label[i] > SmoDS.tolerance and SmoDS.alphas[i] > 0):
        return True
    else:
        return False
