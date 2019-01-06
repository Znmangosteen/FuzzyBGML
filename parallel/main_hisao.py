import multiprocessing as mp

import algorithm_3obj, fuzzyRule_3obj, time, sys, os
from parallel.Worker import Signal, Worker

from parallel.data_distributor import DataDistributor
from parallel.data_reader import DataReader

if __name__ == '__main__':

    # data_set = sys.argv[1]
    # size = 264
    # each_gen = int(sys.argv[2])
    # iterations = int(sys.argv[3])
    # gen_num = each_gen * iterations

    data_set = 'a1_va3'
    size = 264
    each_gen = 10
    iterations = 2
    gen_num = each_gen * iterations

    # CPU_NUM = mp.cpu_count()
    CPU_NUM = 8
    reader = DataReader(data_set)
    distributor = DataDistributor(CPU_NUM)

    distributor.set_dataset(reader.getTrainingData())
    datasets = distributor.partition()

    init_worker = []
    pipe_conns = []
    pipes = [{} for _ in range(CPU_NUM)]

    pops = []

    # init_process_communication

    for i in range(0, CPU_NUM, 2):
        d_conn1_s, d_conn1_r = mp.Pipe()
        d_conn2_s, d_conn2_r = mp.Pipe()
        r_conn1_s, r_conn1_r = mp.Pipe()
        r_conn2_s, r_conn2_r = mp.Pipe()
        prev_idx = (i - 1) % CPU_NUM
        next_idx = (i + 1) % CPU_NUM
        pipes[prev_idx]['data_s'] = d_conn1_s
        pipes[prev_idx]['ruleset_r'] = r_conn1_r
        pipes[i] = {
            'data_s': d_conn2_s,
            'data_r': d_conn1_r,
            'ruleset_s': r_conn1_s,
            'ruleset_r': r_conn2_r,
            'main': None
        }
        pipes[next_idx]['data_r'] = d_conn2_r
        pipes[next_idx]['ruleset_s'] = r_conn2_s

    for i in range(CPU_NUM):
        parent_conn, child_conn = mp.Pipe()
        pipes[i]['main'] = child_conn
        worker = Worker(i, datasets[i], pipes[i], int(size / CPU_NUM), 1, each_gen, iterations, verbose=True)

        init_worker.append(worker)
        pipe_conns.append(parent_conn)

    for worker in init_worker:
        worker.start()

    start = time.time()
    for conn in pipe_conns:
        while True:
            signal = conn.recv()
            if signal == Signal.FirstStepDone:
                break

    # send run main signal
    for pipe in pipe_conns:
        pipe.send(Signal.StartMain)

    while True:
        cnt = 0
        signal = None
        for pipe in pipe_conns:
            signal = pipe.recv()
            if signal == Signal.Terminate:
                pop = pipe.recv()
                pops.extend(pop)
            elif signal == Signal.OneIterDone:
                cnt += 1

        if signal == Signal.Terminate:
            print('islands all finished')
            break
        elif signal == Signal.OneIterDone:
            print('Start Rotate')
            for i, pipe in enumerate(pipe_conns):
                if i == 0:
                    pipe.send(Signal.StartRotateData)
                elif i == CPU_NUM - 1:
                    pipe.send(Signal.StartRotateRuleSet)
                else:
                    pipe.send(Signal.WaitRotate)

        cnt = 0

    train_data = reader.getTrainingData()
    test_data = reader.getTestData()
    fin_pop = pops

    for RS in fin_pop:
        RS.getFitness(train_data)

    algorithm_3obj.pareto_ranking(fin_pop)

    time_cost = time.time() - start
    each_time = time_cost / (each_gen * iterations)

    time_info = "time cost: " + str(time_cost) + '\r' + "time each gen: " + str(each_time)
    RS_info = ''
    draw_info1 = ''
    draw_info2 = ''

    print(time_info)
    print('Result')

    pareto_set = []
    for RS in fin_pop:
        if RS.pareto == 1:
            pareto_set.append(RS)

    shown = set()
    for RS in pareto_set:
        if (RS.fitness2, RS.fitness3) in shown:
            pass
        else:
            shown.add((RS.fitness2, RS.fitness3))
            RS_before = str(RS.fitness) + '  ' + str(40 - RS.fitness2) + '  ' + str(
                sys.maxsize - RS.fitness3)
            draw_info1 += RS_before + '\r'
            RS_before = "Before refit: " + RS_before
            print(RS_before)

            RS.getFitness(test_data)

            RS_after = str(RS.fitness) + '  ' + str(40 - RS.fitness2) + '  ' + str(
                sys.maxsize - RS.fitness3)
            draw_info2 += RS_after + '\r'
            RS_after = "After refit: " + RS_after
            print(RS_after)
            RS_info += RS_before + '\r' + RS_after + '\r\n'

    result_print = time_info + '\r\nResult\r\n' + RS_info + '\r\n' + draw_info1 + '\r\n' + draw_info2

    path = '../3_OBJ/运行结果/' + data_set + '/result data/'

    exist_result = [int(x[:-4].split(' ')[0]) for x in os.listdir(path)]
    last_result = max(exist_result) if exist_result else 0

    write_as = path + '{0} c {1} g {2} s {3} e {4}.txt'.format(last_result + 1, CPU_NUM, gen_num, size, each_gen)
    with open(write_as, 'w') as f:
        f.write(result_print)
