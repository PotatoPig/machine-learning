from WatermelonDataSet_4 import createDataSet
from ClusteringFunctionsPackage import DBSCAN_cluster
import matplotlib.pyplot as plt


k = 5
iteration = 15

DataSet, labels, labels_full = createDataSet()

cluster_result = DBSCAN_cluster(DataSet, 0.11, 5)
print(cluster_result)

fig, ax = plt.subplots()
pattern_list = ['ro', 'bo', 'go', 'r+', 'b+', 'g+']
for i in range(len(cluster_result)):
    for point in cluster_result[i]:
        ax.plot(point[0], point[1], pattern_list[i])

plt.show()

