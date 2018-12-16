from fuzzyRule import fuzzy_rule
import random


def rule_mutation(c: list):
    rule = c
    k = random.randint(0, len(rule) - 1)
    # 把k位置的membership function变异
    rule[k] = random.randint(1, 15)
    return rule


def rule_set_mutation(c: fuzzy_rule):
    pass
