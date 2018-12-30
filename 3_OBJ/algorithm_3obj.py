import crossover, mutation, selection, random


def NSGAII(population, p, gen_num, constant, trainingData, size=100) -> list:
    pc = p[0]
    pm = p[1]
    pMchi = p[2]
    N = constant[0]

    # 进化gen_num代
    for j in range(gen_num):
        # print("gen_num:" + str(j))
        offspring_population = []
        pareto_ranking(population)
        # print("ranked")
        # 生成子代个体并放到offspring_population
        for i in range(size):
            # print("i th: " + str(i))
            # 拿到两个deepcopy过的父类
            p1, p2 = selection.binary_tournament_selection(population)
            # print("selected")

            # c = copy.deepcopy(p1)

            # cp1_rules = copy.deepcopy(p1.rules)
            # cp2_rules = copy.deepcopy(p2.rules)

            if random.random() < pc:
                # crossover for rule set
                child = crossover.rule_set_crossover(p1, p2)
            else:
                child = [p1, p2][random.random() < 0.5]

            # print("crossover")
            # if random.random() < pm:
            #     child = mutation.rule_set_mutation(child)

            # c.rules = child
            child.getFitness(trainingData)

            if random.random() < pMchi:
                child = michigan(child, N, p[3:5], trainingData)
            # print("Michigan over")

            # c.rules = child
            child.getFitness(trainingData)

            offspring_population.append(child)
            # print("added")
            # print()
        # print("offspring generated")

        # 合并父子代并选择
        population = merge_and_select(population, offspring_population, size)
        # print("re-ranked")

    pareto_ranking(population)
    # print("final ranked")
    # print()

    '''
        for RS in population:
            for r in RS.rules:
                if r.fitness == 0:
                    RS.rules.remove(r)
            RS.getFitness(exer4.trainingData)
            print()
    '''
    pareto_set = []
    for solution in population:
        if solution.pareto == 1:
            pareto_set.append(solution)
    return pareto_set, population


def merge_and_select(population: list, offspring_population: list, size):
    total_population = population + offspring_population

    pareto_ranking(total_population)
    total_population.sort(key=lambda x: x.pareto, reverse=False)

    dividing_pareto = total_population[size - 1].pareto
    start = size - 1
    end = size
    while total_population[start - 1].pareto == dividing_pareto and start > 0:
        start -= 1
    while total_population[end].pareto == dividing_pareto and end < 2 * size - 1:
        end += 1

    re_sort_pop = total_population[start:end]
    crowding_measure(re_sort_pop)
    re_sort_pop.sort(key=lambda x: x.distance, reverse=True)
    total_population[start:end] = re_sort_pop

    return total_population[:size]


def pareto_ranking(population: list):
    size = len(population)
    n = [0] * size
    S = []
    for i in range(size):
        a = set()
        S.append(a)
    for i in range(size - 1):
        for j in range(i + 1, size):
            s1 = population[i]
            s2 = population[j]

            if (s1.fitness >= s2.fitness and s1.fitness2 >= s2.fitness2 and s1.fitness3 >= s2.fitness3) and (
                    s1.fitness > s2.fitness or s1.fitness2 > s2.fitness2 or s1.fitness3 > s2.fitness3):
                n[j] += 1
                S[i].add(j)
            elif (s1.fitness <= s2.fitness and s1.fitness2 <= s2.fitness2 and s1.fitness3 <= s2.fitness3) and (
                    s1.fitness < s2.fitness or s1.fitness2 < s2.fitness2 or s1.fitness3 < s2.fitness3):
                n[i] += 1
                S[j].add(i)

    F = set()
    for i in range(size):
        if n[i] == 0:
            F.add(i)

    H = set()
    pareto_num = 1
    while len(F) > 0:
        for k in F:
            population[k].pareto = pareto_num

            for i in S[k]:
                n[i] -= 1
                if n[i] == 0:
                    H.add(i)
        F = H.copy()
        H.clear()
        pareto_num += 1


def crowding_measure(I: list):
    for i in I:
        i.distance = 0

    I.sort(key=lambda x: x.fitness, reverse=False)
    I[0].distance = 5
    I[-1].distance = 5
    total_length = I[-1].fitness - I[0].fitness

    for i in range(1, len(I) - 1):
        if total_length != 0:
            I[i].distance += (I[i + 1].fitness - I[i - 1].fitness) / total_length

    I.sort(key=lambda x: x.fitness2, reverse=False)
    I[0].distance = 5
    I[len(I) - 1].distance = 5
    total_length = I[-1].fitness2 - I[0].fitness2
    for i in range(1, len(I) - 1):
        if total_length != 0:
            I[i].distance += (I[i + 1].fitness2 - I[i - 1].fitness2) / total_length

    I.sort(key=lambda x: x.fitness3, reverse=False)
    I[0].distance = 5
    I[len(I) - 1].distance = 5
    total_length = I[-1].fitness3 - I[0].fitness3
    for i in range(1, len(I) - 1):
        if total_length != 0:
            I[i].distance += (I[i + 1].fitness3 - I[i - 1].fitness3) / total_length


def michigan(population, N, p, trainingData):
    '''

    :param population: a fuzzy rule set
    :param N: number of iteration
    :param p: rate
    :return:
    '''
    pc = p[0]
    pm = p[1]

    # sort population
    population.rules.sort(key=lambda x: x.fitness, reverse=True)

    # child_set = []

    # for i in range(N):
    # child_set.append(p1)

    # P1 p2是rule
    p1, p2 = selection.binary_tournament_selection(population.rules)

    # c = copy.deepcopy(p1)

    cp1_rule = p1.rule
    cp2_rule = p2.rule

    if random.random() < pc:
        # crossover for rule
        child_rule = crossover.uniform_crossover(cp1_rule, cp2_rule)
    else:
        child_rule = [cp1_rule, cp2_rule][random.random() < 0.5]

    if random.random() < pm:
        child_rule = mutation.rule_mutation(child_rule)

    p1.rule = child_rule
    p1.Cq, p1.CFq = p1.getCqCFq(child_rule, trainingData)

    population.rules[-1] = p1

    return population
