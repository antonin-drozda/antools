# -*- coding: utf-8 -*-
"""
MULTIPROCESSING EXAMPLES
"""

import multiprocessing as mp
import concurrent.futures
import time

from antools.logging import get_logger
from antools.multiprocessing import MultiProcess


def worker_A(lock, logger):
    p = MultiProcess(lock, logger, log=False)
    log = p.get_logger()

    p.data = ["A", "B", "C"]
    log.info("Hello!")

    if not "D" in p.data:
        log.warning("A not in data!")
        # log.error("A not in data!") # will terminate all

    p.status = "OK" 
    return p.finish(terminate_all=False)


def worker_B(lock, logger, result):
    p = MultiProcess(lock, logger, log=False)
    log = p.get_logger()

    time.sleep(2)

    p.status = "OK"
    return p.finish(terminate_all=False)

if __name__ == "__main__":

    logger = get_logger(level="DEBUG", file_log=False)
    lock = mp.Manager().Lock()

    logger.info("Starting multiprocessing ... ")

    with concurrent.futures.ProcessPoolExecutor() as executor:

        p1 = executor.submit(worker_A, lock, logger)
        p2 = executor.submit(worker_A, lock, logger)

        if p2.result().status == "OK":
            p3 = executor.submit(worker_B, lock, logger, p2.result().data)

            print(p3.result().data)

    logger.info("Finishing multiprocessing ... ")
