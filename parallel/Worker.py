import os
import time
from enum import Enum
import multiprocessing as mp
from GA_3obj import GA

class Signal(Enum):
    FirstStepDone = 0
    StartMain = 2
    OneIterDone = 4
    StartRotateData = 8
    StartRotateRuleSet = 16
    WaitRotate = 32
    Terminate = 64

class Worker(mp.Process):
    def __init__(self, cpuid, dataset, pipes, size, init_gen, each_gen, iterations, verbose=True):
        mp.Process.__init__(self)
        self.cpuid = cpuid
        self.dataset = dataset
        self.pipes = pipes
        self.size = size
        self.init_gen = init_gen
        self.each_gen = each_gen
        self.iterations = iterations
        self.verbose=verbose

    def run(self):
        dataset = self.dataset
        r_pipe_r = self.pipes['ruleset_r']
        r_pipe_s = self.pipes['ruleset_s']
        d_pipe_r = self.pipes['data_r']
        d_pipe_s = self.pipes['data_s']
        m_pipe = self.pipes['main']
        size = self.size
        init_gen = self.init_gen
        each_gen = self.each_gen
        iterations = self.iterations
        verbose=self.verbose
        cpuid=self.cpuid

        logger_name = '../time_log/time_cpu{0}_{1}.txt'.format(cpuid,
                                                        time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
        # if not os.path.exists(logger_name):

        logger = open(logger_name, 'w', encoding='utf-8')
        ga = GA(dataset, logger)

        # init part
        ga.init_run(size=size, gen_num=init_gen)
        m_pipe.send(Signal.FirstStepDone)

        signal = m_pipe.recv()  # wait for a signal.
        if signal != Signal.StartMain:
            print('error')
            return

        # main part
        for i in range(iterations):
            time_start = time.time()
            ga.run(size=size, gen_num=each_gen)
            if verbose:
                print("cpu:{} iter:{}".format(cpuid,i+1))
            m_pipe.send(Signal.OneIterDone)
            rotate_signal = m_pipe.recv()
            rotate_start=time.time()
            # rotate
            if (rotate_signal == Signal.StartRotateData):
                dataset = ga.data
                d_pipe_s.send(dataset)
                if verbose:
                    print('+cpu{} dataset send complete'.format(cpuid))
                new_dataset = d_pipe_r.recv()
                if verbose:
                    print('+cpu{} recv dataset length:{}'.format(cpuid, len(new_dataset)))
                ga.setDataset(new_dataset)


                bst = ga.getBst()
                new_bst = r_pipe_r.recv()
                if verbose:
                    print('+cpu{} recv ruleset'.format(cpuid))
                ga.updatePop(new_bst)
                r_pipe_s.send(bst)
                if verbose:
                    print('+cpu{} ruleset send complete'.format(cpuid))
            elif (rotate_signal == Signal.StartRotateRuleSet):
                dataset = ga.data
                new_dataset = d_pipe_r.recv()
                if verbose:
                    print('*cpu{} recv dataset length:{}'.format(cpuid,len(new_dataset)))
                ga.setDataset(new_dataset)
                d_pipe_s.send(dataset)
                if verbose:
                    print('*cpu{} dataset send complete'.format(cpuid))

                bst = ga.getBst()
                r_pipe_s.send(bst)
                if verbose:
                    print('*cpu{} ruleset send complete'.format(cpuid))
                new_bst = r_pipe_r.recv()
                if verbose:
                    print('*cpu{} recv ruleset'.format(cpuid))
                ga.updatePop(new_bst)
            elif (rotate_signal == Signal.WaitRotate):
                dataset = ga.data
                new_dataset = d_pipe_r.recv()
                if verbose:
                    print('cpu{} recv dataset length:{}'.format(cpuid, len(new_dataset)))
                ga.setDataset(new_dataset)
                d_pipe_s.send(dataset)
                if verbose:
                    print('cpu{} dataset send complete'.format(cpuid))

                bst = ga.getBst()
                new_bst = r_pipe_r.recv()
                if verbose:
                    print('cpu{} recv ruleset'.format(cpuid))
                ga.updatePop(new_bst)
                r_pipe_s.send(bst)
                if verbose:
                    print('cpu{} ruleset send complete'.format(cpuid))

            time_end = time.time()
            time_cost = time_end - time_start
            rotate_time=time_end-rotate_start
            logger.write('{} {}\n'.format(time_cost,rotate_time))

        logger.close()
        m_pipe.send(Signal.Terminate)
        m_pipe.send(ga.getPop())
