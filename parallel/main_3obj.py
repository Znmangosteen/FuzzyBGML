import multiprocessing as mp
import threading
import algorithm_3obj, fuzzyRule_3obj, time, sys, os

from parallel.data_distributor import DataDistributor
from parallel.data_reader import DataReader
from GA_3obj import GA
from parallel.pop_pool import PopPool


def run(dataset, pipe, size, init_gen, each_gen, total_time):
    logger_name = '../time_log/time_{0}_{1}'.format(os.getpid(), time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
    logger = open(logger_name, 'w', encoding='utf-8')
    ga = GA(dataset, logger)

    # init part
    ga.init_run(size=size, gen_num=init_gen)
    pipe.send(ga.getPop())
    while True:
        signal = pipe.recv()  # wait for a signal.
        if signal == 'Run Main':
            break

    # main part
    # while True:
    for i in range(total_time):
        # terminate_flag = ga.run(size=size, gen_num=each_gen)
        # if terminate_flag:
        #     break

        ga.run(size=size, gen_num=each_gen)
        # update pop
        pipe.send(ga.getPop())
        new_pop = pipe.recv()
        ga.setPop(new_pop)

    logger.close()
    pipe.send("END_FALG")
    pipe.send(ga.getPop())


def lisen(pipe):
    global popPool
    global listen_lock
    while True:
        info = pipe.recv()
        if info == "END_FALG":
            fin_pop = pipe.recv()
            popPool.insert_fin_pop(fin_pop)
            break
        pop = info
        with listen_lock:
            new_pop = popPool.update_pool(pop)
        pipe.send(new_pop)


if __name__ == '__main__':

    data_set = sys.argv[1]
    size = 264
    each_gen = int(sys.argv[2])
    total_time = int(sys.argv[3])
    gen_num = each_gen * total_time

    # CPU_NUM = mp.cpu_count()
    CPU_NUM = 4
    reader = DataReader(data_set)
    distributor = DataDistributor(CPU_NUM)
    popPool = PopPool()
    listen_lock = threading.RLock()

    distributor.set_dataset(reader.getTrainingData())
    datasets = distributor.partition()

    init_worker = []
    pipe_conns = []
    lisen_threads = []
    for i in range(CPU_NUM):
        parent_conn, child_conn = mp.Pipe()
        worker = mp.Process(target=run, args=(datasets[i], child_conn, int(size / CPU_NUM), 5, each_gen, total_time))
        lisener = threading.Thread(target=lisen, args=(parent_conn,))
        init_worker.append(worker)
        lisen_threads.append(lisener)
        pipe_conns.append(parent_conn)

    for worker in init_worker:
        worker.start()

    pops = []
    for conn in pipe_conns:
        pop = conn.recv()
        pops.extend(pop)

    popPool.init_pool(pops)

    start = time.time()

    # run main part
    for lisen_thread in lisen_threads:
        lisen_thread.start()

    # send run main signal
    for conn in pipe_conns:
        conn.send('Run Main')

    for lisen_thread in lisen_threads:
        lisen_thread.join()

    train_data = reader.getTrainingData()
    test_data = reader.getTestData()
    fin_pop = popPool.get_fin_pop()
    for RS in fin_pop:
        RS.getFitness(train_data)

    algorithm_3obj.pareto_ranking(fin_pop)

    time_cost = time.time() - start
    each_time = time_cost / (each_gen * total_time)

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
