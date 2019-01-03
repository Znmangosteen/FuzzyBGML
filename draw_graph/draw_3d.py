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


def draw(fname, color, ecolor):
    global data, _x, _y, x, y, top, bottom
    data = np.loadtxt("D:/program/3rd_year_project/Fuzzy-BW/FuzzyGBML/3_OBJ/运行结果/a1_va3/figure/" + fname)
    _x = data[:, 1]
    _x = _x - 0.5
    _y = data[:, 2]
    _y = _y - 0.5
    x, y = _x, _y
    top = 1 - data[:, 0]
    bottom = np.zeros_like(top)
    ax1.bar3d(x, y, bottom, width, depth, top, color=color, edgecolors=ecolor, zsort='min')


if __name__ == '__main__':
    # setup the figure and axes
    fig = plt.figure(figsize=(10, 10))
    ax1 = fig.add_subplot(111, projection='3d')
    # ax2 = fig.add_subplot(122, projection='3d')

    data = np.loadtxt("D:/program/3rd_year_project/Fuzzy-BW/FuzzyGBML/3_OBJ/运行结果/a1_va3/figure/temp.txt")

    # fake data
    # _x = np.arange(4)
    _x = data[:, 1]
    _x = _x - 0.5
    # _y = np.arange(5)
    _y = data[:, 2]
    _y = _y - 0.5
    _xx, _yy = np.meshgrid(_x, _y)
    # x, y = _xx.ravel(), _yy.ravel()
    x, y = _x, _y
    top = 1 - data[:, 0]
    # top = x + y
    bottom = np.zeros_like(top)
    width = 1
    depth = 1.8

    ax1.bar3d(x, y, bottom, width, depth, top, color='#1136561E', edgecolors='#0E2E49', zsort='min')

    fname = 'temp2.txt'
    color = '#FE6F6120'
    ecolor = '#FE6F61'

    draw(fname, color, ecolor)

    fname = 'temp3.txt'
    color = '#FE6F6120'
    ecolor = '#FE6F61'

    # draw(fname,color,ecolor)

    fname = 'temp4.txt'
    color = '#FE6F6120'
    ecolor = '#FE6F61'

    # draw(fname,color,ecolor)

    blue_proxy = plt.Rectangle((5, 5), 5, 5, fc="#113656")
    red_proxy = plt.Rectangle((0, 0), 5, 5, fc="#FE6F61")
    ax1.legend([blue_proxy, red_proxy], ['Island model', 'Asynchronous-island model'])
    # ax1.legend([blue_proxy,red_proxy],['training data','test data'])

    # name = 'non-parallel on training data'
    # name = 'non-parallel on training data'
    # name = 'non-parallel on test data'
    # name = 'non-parallel'
    # name = 'Island model 100 gen'
    # name = 'Asynchronous-island model 8 cores 100 gen'
    # name = 'Asynchronous-island model 4 cores 100 gen'
    # name = 'Asynchronous-island model 12 cores 100 gen'
    # name='comparing on different model 8 cores 10 gen training data'
    gen = '10'
    # name = 'comparing on different model 8 cores 100 gen test data'
    name = 'comparing on different cores 100 gen train data'
    # name = 'comparing on different cores 100 gen test data'

    ax1.set_title(name)

    #
    # ax2.bar3d(x, y, bottom, width, depth, top, shade=False)
    # ax2.set_title('Not Shaded')
    ax1.set_zlabel('error rate')  # 坐标轴
    ax1.set_ylabel('number of antecedent conditions')
    ax1.set_xlabel('number of rules')

    # ax1.voxels(x, y, top, filled, facecolors=fcolor, edgecolors=ecolor)
    plt.xlim(0, 15)
    plt.ylim(0, 30)

    plt.show()
    # plt.savefig('../3_OBJ/运行结果/a1_va3/figure/' + name + '.png')
