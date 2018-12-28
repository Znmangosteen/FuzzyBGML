import numpy as np
import matplotlib.pyplot as plt

N = 1000
x = []
y = []
x2 = []
y2 = []
# x = [1,2,3,4,5]
# y=[0.635,0.34,0.17,0.08,0.07]
# y=[0.6645,0.34,0.19,0.07,0.07]
with open("./运行结果/a1_va3/result data/8 c 12 g 3000 s 264 e 100.txt", 'r') as f:
    file = f.read().splitlines()
    # print(file)

for line in range(3, len(file)):
    if line % 2 == 0:
        l = file[line].split(' ')
        print(l)
        x.append(int(l[4]))
        y.append(1 - float(l[2]))

with open("./运行结果/\"a1_va3\"/\"result data\"/\"8 c 12 g 3000 s 264 e 100.txt\"", 'r') as f:
    file = f.read().splitlines()
    # print(file)

for line in range(3, len(file)):
    if line % 2 == 0:
        l = file[line].split(' ')
        print(l)
        x2.append(int(l[4]))
        y2.append(1 - float(l[2]))

plt.scatter(x2, y2, alpha=1, edgecolors='black', c='k', label='non parallel')  # edgecolors = 'w',亦可
plt.scatter(x, y, alpha=1, edgecolors='blue', c='b', marker='x', label='parallel')  # edgecolors = 'w',亦可
plt.xlim((0,15))
plt.ylim((0.28,0.65))
# plt.title('Result on iris data set')#显示图表标题
plt.xlabel('Number of rules')  # x轴名称
# plt.ylabel('error rate on training patterns')  # y轴名称
plt.ylabel('error rate on test patterns')  # y轴名称
plt.legend()
plt.show()
