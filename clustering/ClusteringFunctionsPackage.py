import numpy as np
import random
import copy


def dist_cal(vec1, vec2):
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    dist = np.sqrt(np.sum(np.square(v1-v2)))
    return dist


# k-means algorithm
def k_means_cluster(k, iteration, dataset):
    # generate source data
    data_size = len(dataset)
    sample_data = np.array(dataset)
    # initialize the cluster center randomly
    center = {}
    for i in range(k):
        center[i] = sample_data[random.randint(0, data_size-1)]
    # dict to save the clustering result
    cluster = {}
    # loop control flag
    running = 1
    current_loop = 1

    while running == 1 and current_loop <= iteration:
        # refresh the cluster dict
        cluster.clear()
        for i in range(k):
            cluster[i] = []
        # cluster based on distance
        for data in sample_data:
            distance = np.zeros(k)
            for j in range(k):
                distance[j] = np.sqrt(np.sum(np.square(data-center[j])))
            distance_list = distance.tolist()
            data_label = distance_list.index(min(distance_list))
            cluster[data_label].append(data)

        # calculate the new center
        center_new = {}
        for p in range(k):
            sum = np.zeros(2)
            cluster_num = len(cluster[p])
            for sample in cluster[p]:
                sum += sample
            if cluster_num != 0:
                center_new[p] = sum/cluster_num
            else:
                center_new[p] = center[p]

        # check if cluster center have to be updated
        update = True
        for q in range(k):
            center_dist = np.sqrt(np.sum(np.square(center[q]-center_new[q])))
            if center_dist != 0:
                update = True
        if update:
            for m in range(k):
                center[m] = center_new[m]
        else:
            running = 0

        current_loop += 1

    return cluster


# Mixture of Gassian algorithm(MoG)
def GM_cluster(k, iteration, dataset):
    return 0


# density-based clustering algorithm(DBSCAN)
def DBSCAN_cluster(dataset, eps, MinPoits):
    # initialize the core objective
    OMEGA = []  # to contain the core data sample
    for i in dataset:
        num_neighbor = 0
        for j in dataset:
            dist_ij = dist_cal(i, j)
            if dist_ij < eps:
                num_neighbor += 1
        if num_neighbor >= MinPoits:
            OMEGA.append(i)

    cluster = {}
    cluster_box = []
    k = 0
    data_pool = dataset
    while len(OMEGA) is not 0:
        data_pool_old = copy.deepcopy(data_pool)
        seed = OMEGA[random.randint(0, len(OMEGA)-1)]
        queue = [seed]
        cluster_box.clear()
        while len(queue) is not 0:
            obj = queue[0]
            queue.pop(0)
            if obj in OMEGA:
                OMEGA.remove(obj)
                for item in data_pool:
                    distance = dist_cal(item, obj)
                    if distance < eps:
                        cluster_box.append(item)
                        queue.append(item)
                        data_pool.remove(item)


        # cluster[k] = [x for x in data_pool_old if x not in data_pool]
        cluster[k] = [x for x in cluster_box]
        k += 1

    cluster[k] = [x for x in data_pool]

    return cluster


# hierarchical clustering algorithm(AGNES)
def AGNES_cluster(k, dataset):
    return 0