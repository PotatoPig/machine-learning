from SMO_Assistant import *


def simple_smo(data, labels, C, tolerance, maxiteration, kernel):
    smo_data = SmoDataStructure(np.mat(data), np.mat(labels).transpose(), C, tolerance, kernel)
    max_iter = maxiteration
    iteration = 0
    while iteration < max_iter:
        alphaPairsChanged = 0
        for i in range(smo_data.dataAmount):
            e_i = calculate_e_xk(smo_data, i)
            if break_KKT(smo_data, i):
                j, e_j = random_select_alphaj(i, smo_data)

                alphai_old = smo_data.alphas[i].copy()
                alphaj_old = smo_data.alphas[j].copy()
                lower, upper = alphaj_boundary(smo_data.label[i], smo_data.label[j], alphai_old, alphaj_old, smo_data.C)
                if lower == upper:
                    print('lower == upper')
                    continue
                eta = 2.0 * smo_data.KernelMatrix[i, j] - smo_data.KernelMatrix[i, i] - smo_data.KernelMatrix[j, j]
                if eta >= 0:
                    print('eta >= 0')
                    continue
                smo_data.alphas[j] = alphaj_old - (e_i - e_j) * smo_data.label[j] / eta
                smo_data.alphas[j] = limit_alpha(smo_data.alphas[j], upper, lower)
                update_e_xk(smo_data, j)
                if abs(smo_data.alphas[j] - alphaj_old) < 0.00001:
                    print("alphaj is not a efficient change ")
                    continue
                smo_data.alphas[i] = alphai_old + (alphaj_old - smo_data.alphas[j]) * smo_data.label[i] * smo_data.label[j]
                update_e_xk(smo_data, i)

                b_i = smo_data.b - e_i - smo_data.label[i] * smo_data.KernelMatrix[i, i] * (smo_data.alphas[i] - alphai_old) \
                                       - smo_data.label[j] * smo_data.KernelMatrix[i, j] * (smo_data.alphas[j] - alphaj_old)

                b_j = smo_data.b - e_j - smo_data.label[i] * smo_data.KernelMatrix[i, j] * (smo_data.alphas[i] - alphai_old) \
                                       - smo_data.label[j] * smo_data.KernelMatrix[j, j] * (smo_data.alphas[j] - alphaj_old)

                if 0 < smo_data.alphas[i] < smo_data.C:
                    smo_data.b = b_i
                elif 0 < smo_data.alphas[j] < smo_data.C:
                    smo_data.b = b_j
                else:
                    smo_data.b = (b_i + b_j) / 2.0
                alphaPairsChanged += 1

        if alphaPairsChanged == 0:
            iteration += 1

    print(smo_data.alphas, smo_data.b)
    return smo_data.alphas, smo_data.b


# heuristic smo : choose the alpha_i and alpha_j whose bounded data is most far away
def heuristic_smo(data, labels, C, tolerance, maxiteration, kernel):
    smo_data = SmoDataStructure(np.mat(data), np.mat(labels).transpose(), C, tolerance, kernel)
    max_iter = maxiteration
    iteration = 0
    alphaPairsChanged = 0
    entireDataSet = True
    while iteration < max_iter:
        alphaPairsChanged = 0
        if entireDataSet:
            for i in range(smo_data.dataAmount):
                if update_alpha_pair(i, smo_data):
                    alphaPairsChanged += 1
                print("fullSet--iter: %d i:%d pairs changed:%d" % (iteration, i, alphaPairsChanged))
        else:
            boundary_list = np.nonzero((smo_data.alphas.A > 0) * (smo_data.alphas.A < smo_data.C))[0]
            for i in boundary_list:
                if update_alpha_pair(i, smo_data):
                    alphaPairsChanged += 1
                print("boundarySet--iter: %d i:%d pairs changed:%d" % (iteration, i, alphaPairsChanged))

        if entireDataSet:
            entireDataSet = False
        elif alphaPairsChanged == 0:
            entireDataSet = True

        '''
        if alphaPairsChanged > 0:
            iteration += 1
        else:
            iteration += 0
        '''
        iteration += 1
        print("iteration number: %d" % iteration)
    print(smo_data.alphas, smo_data.b)
    return smo_data.alphas, smo_data.b


def update_alpha_pair(i, SmoDS):
    e_i = calculate_e_xk(SmoDS, i)
    if break_KKT(SmoDS, i):
        j, e_j = max_select_alphaj(SmoDS, i, e_i)
        # j, e_j = random_select_alphaj(i, SmoDS)
        alphai_old = SmoDS.alphas[i].copy()
        alphaj_old = SmoDS.alphas[j].copy()
        lower, upper = alphaj_boundary(SmoDS.label[i], SmoDS.label[j], SmoDS.alphas[i], SmoDS.alphas[j], SmoDS.C)

        # if L equals H, then it's impossible to update the alpha
        if lower == upper:
            print('lower == upper')
            return False

        eta = 2.0 * SmoDS.KernelMatrix[i, j] - SmoDS.KernelMatrix[i, i] - SmoDS.KernelMatrix[j, j]
        if eta >= 0:
            print('eta >= 0')
            return False

        SmoDS.alphas[j] = alphaj_old - (e_i - e_j) * SmoDS.label[j] / eta
        SmoDS.alphas[j] = limit_alpha(SmoDS.alphas[j], upper, lower)
        update_e_xk(SmoDS, j)
        if abs(SmoDS.alphas[j] - alphaj_old) < 0.00001:
            print("alphaj is not a efficient change ")
            return False
        SmoDS.alphas[i] = alphai_old + (alphaj_old - SmoDS.alphas[j])*SmoDS.label[i]*SmoDS.label[j]
        update_e_xk(SmoDS, i)

        b_i = SmoDS.b - e_i - SmoDS.label[i] * SmoDS.KernelMatrix[i, i] * (SmoDS.alphas[i] - alphai_old) \
                            - SmoDS.label[j] * SmoDS.KernelMatrix[i, j] * (SmoDS.alphas[j] - alphaj_old)

        b_j = SmoDS.b - e_j - SmoDS.label[i] * SmoDS.KernelMatrix[i, j] * (SmoDS.alphas[i] - alphai_old) \
                            - SmoDS.label[j] * SmoDS.KernelMatrix[j, j] * (SmoDS.alphas[j] - alphaj_old)

        if 0 < SmoDS.alphas[i] < SmoDS.C:
            SmoDS.b = b_i
        elif 0 < SmoDS.alphas[j] < SmoDS.C:
            SmoDS.b = b_j
        else:
            SmoDS.b = (b_i + b_j) / 2.0

        return True

    else:
        return False
