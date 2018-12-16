import pandas as pd
import numpy as np
import random


class PopPool(object):
    def __init__(self, dtype=np.float64):
        # self.pool = pd.Series([], dtype=dtype)
        self.pool = []
        self.fin_pool = []

    def init_pool(self, pops):
        # for pop in pops:
        #     self.pool.append(pd.Series(pop))
        self.pool = pops

    def update_pool(self, pop: list):
        self.pool.extend(pop)
        # amount = pop.size
        # for p in pop:
        #     self.pool.append(pd.Series(p))
        amount = len(pop)
        # print('amount '+str(amount))
        # print('total ' +str(len(self.pool)))
        random.shuffle(self.pool)
        new_pop = self.pool[:amount]
        self.pool=self.pool[:-amount]
        # new_pop = self.pool.sample(amount)
        # self.pool.drop(new_pop.index, inplace=True)

        return new_pop
        # return new_pop.tolist()

    def insert_fin_pop(self, pop):
        self.fin_pool.extend(pop)

    def get_fin_pop(self):
        return self.fin_pool
