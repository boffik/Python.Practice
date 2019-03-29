# -*- coding: utf-8 -*-
import multiprocessing as mp
import time


def run_proccess(queue):
    """Процесс потока"""
    counts_num = 0
    t0 = time.time()

    while True:
        if time.time() - t0 > 10:
            break
        counts_num += 1

    queue.put(counts_num)


if __name__ == "__main__":
    n_cpus = mp.cpu_count() * 9
    queue = mp.Queue()
    counts_num = 0

    for i in range(n_cpus):
        proc = mp.Process(target=run_proccess, args=(queue,))
        proc.start()

    time.sleep(11)

    for i in range(n_cpus):
        counts_num += queue.get()

    print(counts_num, counts_num/n_cpus)
