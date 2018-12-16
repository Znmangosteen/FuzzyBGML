import random, copy


def binary_tournament_selection(front: list):
    results = []

    if front is None:
        raise Exception('The front is null')
    elif len(front) == 0:
        raise Exception('The front is empty')

    if len(front) == 1:
        results = [front[0], front[0]]
    else:
        for a in range(2):
            # Sampling without replacement
            i, j = random.sample(range(0, len(front)), 2)
            solution1 = front[i]
            solution2 = front[j]

            flag = solution1.compare(solution2)

            if flag:
                result = copy.deepcopy(solution1)
            else:
                result = copy.deepcopy(solution2)
            # else:
            #     result = [copy.deepcopy(solution1), copy.deepcopy(solution2)][random.random() < 0.5]
            results.append(result)
    return results
