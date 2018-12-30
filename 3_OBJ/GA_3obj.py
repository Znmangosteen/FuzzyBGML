import copy
import os

import algorithm_3obj, random, time
import fuzzyRule_3obj


class GA():
    def __init__(self, dataset, logger):
        self.data = dataset
        self.p = [0.9, 0.25, 0.5, 0.9, 0.25]
        self.constant = [1]
        self.logger = logger
        self.pareto_set = None

    def init_run(self, size=150, gen_num=5):
        '''

        :param size: population size
        :param gen_num: generation number
        :return: a initial population after gen_num generations
        '''

        population = []

        while len(population) < size:
            # use_data = random.randint(1, 15)
            use_data = 20
            init_trainingData_idx = random.sample(range(0, len(self.data)), use_data)
            init_trainingData = []

            for idx in init_trainingData_idx:
                init_trainingData.append(self.data[idx])
            RS = fuzzyRule_3obj.rule_set(init_trainingData)
            if len(RS.rules) > 0:
                RS.getFitness(self.data)
                population.append(RS)

        time_start = time.time()
        print("start")
        pareto_set, population = algorithm_3obj.NSGAII(population=population, p=self.p, gen_num=gen_num,
                                                       constant=self.constant,
                                                       size=size, trainingData=self.data)
        self.pareto_set = pareto_set
        time_end = time.time()
        time_cost = time_end - time_start

        # print("time cost: " + str(time_cost))
        # print("time each gen: " + str(time_cost / gen_num))
        # print()

        self.population = population

    def run(self, gen_num, size):
        time_start = time.time()

        pareto_set, population = algorithm_3obj.NSGAII(population=self.population, p=self.p, gen_num=gen_num,
                                                       constant=self.constant, size=size, trainingData=self.data)
        self.pareto_set = pareto_set
        time_end = time.time()
        time_cost = time_end - time_start
        self.logger.write('{}\n'.format(time_cost))
        # print("time cost: " + str(time_cost))
        # print("time each gen: " + str(time_cost / gen_num))
        # print()

        self.population = population

    def getPop(self):
        return self.population

    def setPop(self, population):
        self.population = population

    def setDataset(self, dataset):
        self.data = dataset

    def getBst(self):
        max_acc = 0
        bst=self.pareto_set[0]
        for rule_set in self.pareto_set:
            if rule_set.fitness > max_acc:
                bst = rule_set
                max_acc = rule_set.fitness

        return copy.deepcopy(bst)

    def updatePop(self, bst):
        min_acc = 1
        worst_idx=0
        for i,rule_set in enumerate(self.population):
            if rule_set.fitness < min_acc:
                worst_idx = i
                min_acc = rule_set.fitness

        del self.population[worst_idx]
        self.population.append(bst)


# data, NClass, dictL2I, dictI2L = util.readData("./data/a1_va3.csv")
# # data, NClass, dictL2I, dictI2L = util.readData("./data/iris.dat")
# pData = 0.4  # proportion of training data
# N = int(pData * len(data))
# random.shuffle(data)
# trainingData = data[:N]
# testData = data

if __name__ == '__main__':

    while True:

        # p = [0.9, 0.25, 0.5, 0.9, 0.25]

        # print('Result')
        # shown = set()
        # for RS in pareto_set:
        #     if RS.fitness2 in shown:
        #         pass
        #     else:
        #         shown.add(RS.fitness2)
        #         print("Before refit: " + str(RS.fitness) + '  ' + str(40 - RS.fitness2) + '  ' + str(RS.correct_num))
        #         RS.getFitness(testData)
        #         print("After refit: " + str(RS.fitness) + '  ' + str(40 - RS.fitness2) + '  ' + str(RS.correct_num))

        if input() == "no":
            break
