import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# data = np.random.randint(0, 255, size=[40, 40, 40])

# x, y, z = data[0], data[1], data[2]
ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
data = np.loadtxt('../3_OBJ/运行结果/a1_va3/figure/20 c 1 g 800 s 264 e 0.txt')
# data = np.loadtxt('../3_OBJ/运行结果/phoneme/figure/20 c 1 g 800 s 264 e 0.txt')
#  将数据点分成三部分画，在颜色上有区分度
# ax.scatter(x[:10], y[:10], z[:10], c='y')  # 绘制数据点

# ax.scatter(x[10:20], y[10:20], z[10:20], c='r')
# ax.scatter(x[30:40], y[30:40], z[30:40], c='g')
n = 10
# x, y, z = data[:n, 1], data[:n, 2], 1 - data[:n, 0]
x, y, z = data[n:, 1], data[n:, 2], 1 - data[n:, 0]

type1 = ax.scatter(x, y, z, c='b')

n = 7
data = np.loadtxt('../3_OBJ/运行结果/a1_va3/figure/22 c 8 g 800 s 264 e 50.txt')
# x, y, z = data[:n, 1], data[:n, 2], 1 - data[:n, 0]

x, y, z = data[n:, 1], data[n:, 2], 1 - data[n:, 0]
type2 = ax.scatter(x, y, z, c='r')

ax.set_zlabel('error rate')  # 坐标轴
ax.set_ylabel('number of antecedent conditions')
ax.set_xlabel('number of rules')

# ax.legend((type1, type2), ("train data", "test data"), loc=0)
ax.legend((type1, type2), ("single core", "8 cores"), loc=0)

plt.show()
