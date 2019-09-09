from MyData import load_data_set
from SMO import *
import matplotlib.pyplot as plt


data, label = load_data_set('./SVM_data/linear.txt')
figure = fig, ax = plt.subplots()
for i in range(len(data)):
    if label[i] == 1:
        ax.plot(data[i][0], data[i][1], 'ro')
    else:
        ax.plot(data[i][0], data[i][1], 'b+')
alpha, b = simple_smo(data, label, 1, 0.001, 200, kernel='linear')
for i, alpha in enumerate(alpha):
    if abs(alpha) > 0:
        x, y = data[i]
        plt.scatter([x], [y], s=150, c='none', alpha=0.7, linewidth=1.5, edgecolor='red')
plt.show()
