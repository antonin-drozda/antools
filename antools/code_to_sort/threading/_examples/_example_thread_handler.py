from antools.threading import ThreadProcess, ThreadHandler

from antools.logging import get_logger

import threading
import time

def worker_A(lock, logger, args=None):
    p = ThreadProcess(lock, logger)

    p.status = "OK"
    p.data = ["A", "B", "C"]
    time.sleep(1)

    return p.finish(terminate_all=False)


def worker_B(lock, logger, args=None):
    p = ThreadProcess(lock, logger)

    p.status = "OK"
    p.data = ["D", "E", "F"]
    time.sleep(1)


    return p.finish(terminate_all=False)

def worker_C(lock, logger, args=None):
    p = ThreadProcess(lock, logger)

    p.status = "OK"
    p.data = ["G", "H", "I"]
    time.sleep(1)

    return p.finish(terminate_all=False)

def worker_D(lock, logger, args=None):
    p = ThreadProcess(lock, logger)
    
    p.status = "OK"
    p.data = ["J", "K", "L"]
    time.sleep(1)
    p.error = "SOME ERROR"

    return p.finish(terminate_all=False)

def worker_E(lock, logger, args=None):
    p = ThreadProcess(lock, logger)

    p.status = "OK"
    p.data = ["A", "B", "C"]
    time.sleep(1)

    return p.finish(terminate_all=False)

def worker_F(lock, logger, args=None):
    p = ThreadProcess(lock, logger)

    p.status = "OK"
    p.data = ["A", "B", "C"]
    p.status = "X"
    time.sleep(1)

    return p.finish(terminate_all=False)

def my_func(args, lock):

    x = True if args % 2 == 0 else False
    return (args, x)


if __name__ == "__main__":

    logger = get_logger(level="INFO", file_log=False)
    lock = threading.Lock()

    # FIRST EXAMPLE 
    # RUN FUNTIONS AS SOON AS ITS DEPENDENCY IS RESOLVED
    SCHEDULE = {worker_A : None, 
                worker_B : [worker_A], 
                worker_C: [worker_A, worker_D], 
                worker_D : [worker_B],
                worker_E: None,
                worker_F: worker_E}

    Scheduler = ThreadHandler(logger)
    data = Scheduler.run_schedule(schedule=SCHEDULE, max_workers=4)
    print(data)


    time.sleep(3)

    # SECOND EXAMPLE
    # RUN ONE FUNCTION ON MULTIPLE PROCESSES
    DATA = [i for i in range(200)]
    Scheduler = ThreadHandler(logger)
    workers = 8 if len(DATA) >= 10000 else 4
    data = Scheduler.run_func(my_func, args=DATA, max_workers=workers)
    print(data)



