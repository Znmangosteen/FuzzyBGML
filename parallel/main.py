import multiprocessing as mp
import threading
import algorithm, fuzzyRule, time

from parallel.data_distributor import DataDistributor
from parallel.data_reader import DataReader
from GA import GA
from parallel.pop_pool import PopPool


def run(dataset, pipe, size, init_gen, each_gen, total_time):
    ga = GA(dataset)

    # init part
    ga.init_run(size=size, gen_num=init_gen)
    pipe.send(ga.getPop())
    pipe.recv()  # wait for a signal. TODO: need auth?

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
    CPU_NUM = mp.cpu_count()
    reader = DataReader()
    distributor = DataDistributor(CPU_NUM)
    popPool = PopPool()
    listen_lock = threading.RLock()
    each_gen = 50
    total_time = 12

    distributor.set_dataset(reader.getTrainingData())
    datasets = distributor.partition()

    init_worker = []
    pipe_conns = []
    lisen_threads = []
    for i in range(CPU_NUM):
        parent_conn, child_conn = mp.Pipe()
        worker = mp.Process(target=run, args=(datasets[i], child_conn, 12, 5, each_gen, total_time))
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

    algorithm.pareto_ranking(fin_pop)

    time_cost = time.time() - start
    print('time cost: ' + str(time_cost))
    each_time = time_cost / 200
    print('time each gen: ' + str(each_time))

    pareto_set = []
    for RS in fin_pop:
        if RS.pareto == 1:
            pareto_set.append(RS)

    shown = set()
    for RS in pareto_set:
        if RS.fitness2 in shown:
            pass
        else:
            shown.add(RS.fitness2)
            print("Before refit: " + str(RS.fitness) + '  ' + str(40 - RS.fitness2) + '  ' + str(RS.correct_num))
            RS.getFitness(test_data)
            print("After refit: " + str(RS.fitness) + '  ' + str(40 - RS.fitness2) + '  ' + str(RS.correct_num))
