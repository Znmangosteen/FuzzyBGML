import matplotlib.pyplot as plt

name_list = ['200', '400', '600']
num_list = [2432,3339, 4658]
# num_list = [12.16,16.696, 23.2927]
num_list1 = [22, 36, 44]
# num_list1 = [0.1109, 0.1810, 0.2225]
x = list(range(len(num_list)))
total_width, n = 0.8, 2
width = total_width / n

plt.bar(x, num_list, width=width, label='non parallel', fc='blue')
for xp,y in zip(x,num_list):
    plt.text(xp, y + 0.01, "%.2f" % y, ha='center', va='bottom')
for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, num_list1, width=width, label='parallel', tick_label=name_list, fc='green')
for xp,y in zip(x,num_list1):
    plt.text(xp, y + 0.01, "%.2f" % y, ha='center', va='bottom')
plt.legend()

plt.xlabel('number of generations')  # x轴名称
plt.ylabel('time(s) for each generation')  # y轴名称


plt.show()
