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

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x, y = np.random.rand(2, 100) * 4

hist, xedges, yedges = np.histogram2d(x, y, bins=4, range=[[0, 4], [0, 4]])

# Construct arrays for the anchor positions of the 16 bars.
# Note: np.meshgrid gives arrays in (ny, nx) so we use 'F' to flatten xpos,
# ypos in column-major order. For numpy >= 1.7, we could instead call meshgrid
# with indexing='ij'.
xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25)
xpos = xpos.flatten('F')
ypos = ypos.flatten('F')
zpos = np.zeros_like(xpos)

# Construct arrays with the dimensions for the 16 bars.
dx = 1 * np.ones_like(zpos)
dy = dx.copy()
dz = hist.flatten()

ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b', zsort='average')

plt.show()