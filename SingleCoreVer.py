import algorithm, util, random, time
import fuzzyRule, os, sys


def run(data_set, size, gen_num, times):
    '''

    :param data_set: data_set
    :param size: population size
    :param gen_num: generation number for one time
    :param times: total times of generation
    '''

    data, NClass, dictL2I, dictI2L = util.readData("./data/" + data_set + '.csv')
    pData = 0.7  # proportion of training data
    N = int(pData * len(data))
    random.shuffle(data)
    trainingData = data[:N]
    testData = data[N:]

    accuracy = 0

    population = []
    while len(population) < size:
        # use_data = random.randint(1, 15)
        use_data = 20
        init_trainingData_idx = random.sample(range(0, len(trainingData)), use_data)
        init_trainingData = []

        for idx in init_trainingData_idx:
            init_trainingData.append(trainingData[idx])
        RS = fuzzyRule.rule_set(init_trainingData)
        if len(RS.rules) > 0:
            RS.getFitness(trainingData)
            population.append(RS)

    # for RS in population:
    #     print(str(RS.fitness) + '  ' + str(40 - RS.fitness2))

    time_start = time.time()

    for i in range(times):

        # p = [0.9, 0.25, 0.5, 0.9, 0.25]
        p = [0.9, 0.25, 0.5, 0.9, 0.25]
        constant = [1]

        print("start")
        pareto_set, population = algorithm.NSGAII(population=population, p=p, gen_num=gen_num, constant=constant,
                                                  size=size, trainingData=trainingData)

        time_end = time.time()
        time_cost = time_end - time_start

        time_info = "time cost: " + str(time_cost) + '\r' + "time each gen: " + str(time_cost / gen_num * (i + 1))
        RS_info = ''

        print(time_info)
        print()
        print('Result')
        shown = set()
        for RS in pareto_set:
            if RS.fitness2 in shown:
                pass
            else:
                shown.add(RS.fitness2)
                RS_before = "Before refit: " + str(RS.fitness) + '  ' + str(40 - RS.fitness2) + '  ' + str(
                    RS.correct_num)
                print(RS_before)
                RS.getFitness(testData)

                RS_after = "After refit: " + str(RS.fitness) + '  ' + str(40 - RS.fitness2) + '  ' + str(RS.correct_num)
                print(RS_after)
                RS_info += RS_before + '\r' + RS_after + '\r\n'

                RS.getFitness(trainingData)

        result_print = time_info + '\r\nResult\r\n' + RS_info

        path = './运行结果/' + data_set + '/result data/'

        exist_result = [int(x[:-4].split(' ')[0]) for x in os.listdir(path)]
        last_result = max(exist_result) if exist_result else 0

        write_as = path + '{0} c {1} g {2} s {3} e {4}.txt'.format(last_result + 1, 1, (i + 1) * gen_num, size, 0)
        with open(write_as, 'w') as f:
            f.write(result_print)


if __name__ == '__main__':
    # data_set = "iris"
    # data_set = "a1_va3"
    # data_set = "yeast"
    data_set = sys.argv[1]


    size = 264
    gen_num = int(sys.argv[2])
    times = int(sys.argv[3])

    run(data_set, size, gen_num, times)
