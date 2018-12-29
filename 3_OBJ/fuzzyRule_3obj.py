import mbFunc as mb
import random
import sys

N = 15  # number of membership functions


class rule_set:
    pareto = 0
    rules = []
    fitness = 0
    fitness2 = 0
    fitness3 = 0
    correct_num = 0
    distance = 0

    def __lt__(self, other):
        if self.pareto > other.pareto:
            return 1
        else:
            return -1

    def __init__(self, trainingData):
        pop = []
        for p in trainingData:
            rule = fuzzy_rule(p, trainingData)
            if (rule.CFq > 0):
                pop.append(rule)
        self.rules = pop

    def classify(self, xp):

        # print("pattern:",xp)
        scores = []
        for i in range(0, len(self.rules)):
            rule = self.rules[i]
            score = (fuzzy_rule.getCompGrade(rule.rule, xp)) * rule.CFq
            scores.append([rule.Cq, score, i])
        # print(scores[0])
        # print("-----------")
        # print(xp)
        # print(scores)
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[0][0], scores[0][2]

        pass

    def getFitness(self, testData):
        fitness = 0
        hit = [0] * len(self.rules)
        for data in testData:
            result, index = self.classify(data)
            # print(result, index)
            if (result == data[-1]):
                fitness += 1
                hit[index] += 1
        self.fitness = fitness / len(testData)
        self.fitness2 = 40 - len(self.rules)
        self.correct_num = fitness
        self.fitness3 = sys.maxsize - len(self.rules) * len(self.rules[0].rule)
        # print(hit)
        for i in range(len(self.rules)):
            self.rules[i].fitness = hit[i]
            self.fitness3 += self.rules[i].rule.count(1)

        # return self.fitness / len(testData)

    def compare(self, other):
        if self.pareto < other.pareto:
            return True
        else:
            return False


class fuzzy_rule:
    pDC = 0.85  # probablity of don't care
    # pDC = 0.5  # probablity of don't care
    rule = []
    Cq = 0
    CFq = 0
    fitness = 0

    # fuzzy rule包括规则的主体(list)和适应度
    def __init__(self, pattern, trainingData):
        # print("pattern: ", pattern)
        self.rule = self.genRule(pattern)
        self.Cq, self.CFq = self.getCqCFq(self.rule, trainingData)

    def get_fitness(self, rule):
        return 0

    def __lt__(self, other):
        if self.fitness > other.fitness:
            return 1
        else:
            return -1

    def genRule(self, pattern):
        rule = []
        for x in pattern[:-1]:
            maxV = -float("inf")
            index = -1
            if (random.random() > self.pDC):
                for n in range(2, N + 1):

                    score = mb.u(n, x)
                    if (score > maxV):
                        maxV = score
                        index = n
            else:
                index = 1
            rule.append(index)
        return rule

    def getCqCFq(self, p, trainingData):
        total = 0
        c = [0] * (N + 1)
        for pattern in trainingData:
            # print("pattern:",pattern)
            score = fuzzy_rule.getCompGrade(p[:-1], pattern)
            c[pattern[-1]] += score
            total += score
        for i in range(len(c)):
            if total > 0:
                c[i] /= total
        # print("_____", p, ":", c)
        cqh = max(c)
        result = c.index(cqh)
        CFq = cqh
        for x in c:
            if (x != cqh):
                CFq -= x
        return result, CFq

    def getCompGrade(r, pattern):
        score = 1
        for i in range(len(r)):
            score *= mb.u(r[i], pattern[i])
        return score

    def fitRule(self, rule, dataSet):
        pass

    def prints(self, list):
        for i in list:
            print(i)

    def compare(self, other):
        if self.fitness > other.fitness:
            return True
        else:
            return False

# data, NClass, dictL2I, dictI2L = util.readData("./data/iris.dat")
# pData = 0.1  # proportion of training data
# N = int(pData * len(data))

# print("train: ",len(trainingData))
# print("test: ",len(testData))
# for data in testData:
#   print(data)


# print(xp)

# for rule in RS.rules:
#   print(rule.rule," Cq:",rule.Cq, " CFq:",rule.CFq)

# nRight = 0
# accuracy = 0
# for i in range(10):

# accuracy += nRight/(len(testData)*10)
# print("accuracy: ", accuracy)
# trainingData = []
# testData = []
# random.shuffle(data)
# trainingData = data[:N]
# testData = data
# rule = fuzzy_rule(trainingData[0], trainingData)
# RS = rule_set(trainingData)
# index = random.randint(0, len(trainingData) - 1)
# xp = trainingData[index]
# nRight = 0
# for data2 in testData:
#     xp = data2[:-1]
#     result = RS.classify(xp)
#     if (result == data2[-1]):
#         nRight += 1
#
# print("accuracy:", nRight / len(testData), "fitness:", RS.getFitness(testData))
# for i in range(len(RS.rules)):
#     print("rule ", i, " win ", RS.rules[i].fitness)
#
# print(RS.fitness)
