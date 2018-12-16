import init, algorithm, util, random, time
import fuzzyRule


class GA():
    def __init__(self, dataset):
        self.data = dataset
        self.p = [0.9, 0.25, 0.5, 0.9, 0.25]
        self.constant = [1]

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
            RS = fuzzyRule.rule_set(init_trainingData)
            if len(RS.rules) > 0:
                RS.getFitness(self.data)
                population.append(RS)

        time_start = time.time()
        print("start")
        pareto_set, population = algorithm.NSGAII(population=population, p=self.p, gen_num=gen_num,
                                                  constant=self.constant,
                                                  size=size, trainingData=self.data)

        time_end = time.time()
        time_cost = time_end - time_start
        # print("time cost: " + str(time_cost))
        # print("time each gen: " + str(time_cost / gen_num))
        # print()

        self.population = population

    def run(self, gen_num, size):

        time_start = time.time()
        print("start")
        pareto_set, population = algorithm.NSGAII(population=self.population, p=self.p, gen_num=gen_num,
                                                  constant=self.constant, size=size, trainingData=self.data)

        time_end = time.time()
        time_cost = time_end - time_start
        # print("time cost: " + str(time_cost))
        # print("time each gen: " + str(time_cost / gen_num))
        # print()

        self.population = population

    def getPop(self):
        return self.population

    def setPop(self, population):
        self.population = population


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
