# -*- coding: utf-8 -*-
from threading import Thread
import time

class TestThread(Thread):
    """
    A threading test
    """
    def __init__(self, number):
        """Инициализация потока"""
        Thread.__init__(self)
        self.number = number
        self.counts = 0
        self.total_counts = 0
        

    def run(self):
        """Запуск потока"""
        t0 = time.time()
        while True:
            if time.time() - t0 > 10:
                break
            self.counts += 1

        self.total_counts += self.counts


def create_threads(list_threads, a):
    """
    Создаем группу потоков
    """
    for i in range(a):
        number = i+1
        my_thread = TestThread(number)
        list_threads.append(my_thread)
        my_thread.start()


if __name__ == "__main__":
    all_threads = []
    a = 36
    create_threads(all_threads, a)

    time.sleep(11)
    counts = 0

    for item in all_threads:
        counts += item.counts
#        print(item.counts, end="\n")

    print(counts, counts/a)
