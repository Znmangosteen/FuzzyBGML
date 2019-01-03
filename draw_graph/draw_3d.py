# import scipy.io as sio
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
# import numpy as np
#
# def Detectionplot():
#
#     data = sio.loadmat('F:\detection.mat')    #完成数据的导入
#     m = data['data'] #将其与m数组形成对应关系
#
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')   #此处因为是要和其他的图像一起展示，用的add_subplot，如果只是展示一幅图的话，可以用subplot即可
#
#     x = m[0]
#     y = m[1]
#     z = m[2]
#
#     x = x.flatten('F')   #flatten功能具体可从Declaration中看到
#     y = y.flatten('F')
#
# #更改柱形图的颜色，这里没有导入第四维信息，可以用z来表示了
#     C = []
#     for a in z:
#         if a < 10:
#             C.append('b')
#         elif a < 20:
#             C.append('c')
#         elif a < 30:
#             C.append('m')
#         elif a < 40:
#             C.append('pink')
#         elif a > 39:
#             C.append('r')
#
# #此处dx，dy，dz是决定在3D柱形图中的柱形的长宽高三个变量
#     dx = 0.6 * np.ones_like(x)
#     dy = 0.2 * np.ones_like(y)
#     dz = abs(z) * z.flatten()
#     dz = dz.flatten() / abs(z)
#     z = np.zeros_like(z)
#
# #设置三个维度的标签
#     ax.set_xlabel('Xlabel')
#     ax.set_ylabel('Ylabel')
#     ax.set_zlabel('Amplitude')
#
#     ax.bar3d(x, y, z, dx, dy, dz, color=C, zsort='average')
#
#     plt.show()
#
# Detectionplot()

# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
# import numpy as np
#
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# x, y = np.random.rand(2, 100) * 4
#
# hist, xedges, yedges = np.histogram2d(x, y, bins=4, range=[[0, 4], [0, 4]])
#
# # Construct arrays for the anchor positions of the 16 bars.
# # Note: np.meshgrid gives arrays in (ny, nx) so we use 'F' to flatten xpos,
# # ypos in column-major order. For numpy >= 1.7, we could instead call meshgrid
# # with indexing='ij'.
# xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25)
# xpos = xpos.flatten('F')
# ypos = ypos.flatten('F')
# zpos = np.zeros_like(xpos)
#
# # Construct arrays with the dimensions for the 16 bars.
# dx = 1 * np.ones_like(zpos)
# dy = dx.copy()
# dz = hist.flatten()
#
# ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b', zsort='average')
#
# plt.show()


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# setup the figure and axes
fig = plt.figure(figsize=(8, 8))
ax1 = fig.add_subplot(111, projection='3d')
# ax2 = fig.add_subplot(122, projection='3d')

data = np.loadtxt("D:/program/3rd_year_project/Fuzzy-BW/FuzzyGBML/3_OBJ/运行结果/a1_va3/figure/8 c 4 g 3000 s 264 e 50.txt")

# fake data
# _x = np.arange(4)
_x = data[:, 1]
# _x = _x - 0.5
# _y = np.arange(5)
_y = data[:, 2]
# _y = _y - 0.5
_xx, _yy = np.meshgrid(_x, _y)
# x, y = _xx.ravel(), _yy.ravel()
x, y = _x, _y
top = 1 - data[:, 0]
# top = x + y
bottom = np.zeros_like(top)
width = 1
depth = 1.8

ax1.bar3d(x, y, bottom, width, depth, top, color='#FFCEEF88',edgecolors='#BFAB6E',zsort='min')
ax1.set_title('Shaded')
#
# ax2.bar3d(x, y, bottom, width, depth, top, shade=False)
# ax2.set_title('Not Shaded')
ax1.set_zlabel('error rate')  # 坐标轴
ax1.set_ylabel('number of antecedent conditions')
ax1.set_xlabel('number of rules')

# filled = np.ones_like(x)
# filled = np.zeros((50, 50, 50), dtype=bool)
# fcolor = np.where(filled, '#FFD65DC0', '#7A88CCC0')
# ecolor = np.where(filled, '#BFAB6E', '#7D84A6')
#
# ax1.voxels(x, y, top, filled, facecolors=fcolor, edgecolors=ecolor)
plt.xlim(0,15)
plt.ylim(0,30)
# plt.show()
plt.savefig('../3_OBJ/运行结果/a1_va3/figure/test.png')