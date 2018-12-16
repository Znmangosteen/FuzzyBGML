import numpy as np
import random, util


class DataReader(object):
    def __init__(self):
        data, NClass, dictL2I, dictI2L = util.readData("../data/a1_va3.csv")
        # data, NClass, dictL2I, dictI2L = util.readData("./data/iris.dat")
        pData = 0.3  # proportion of training data
        N = int(pData * len(data))
        random.shuffle(data)
        self.trainingData = data[:N]
        self.testData = data

    def getTrainingData(self):
        return self.trainingData

    def getTestData(self):
        return self.testData

    def get_iris_data(self):
        data = []
        label_map = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
        inverse_label_map = self._build_inverse_map(label_map)

        with open('../data/iris.dat', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip('\n')
                if line == '':
                    continue

                parts = line.split(',')

                x = [parts[i] for i in range(4)]
                label = inverse_label_map[parts[4]]
                data.append((x, label))

        np.random.shuffle(data)
        return data

    def _build_inverse_map(self, label_map):
        inverse_label_map = {}
        for i, label in enumerate(label_map):
            inverse_label_map[label] = i
        return inverse_label_map
