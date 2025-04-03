# -*- coding: utf-8 -*-
"""
THREADING EXAMPLES
"""

import threading
import concurrent.futures
import time

from antools.logging import get_logger
from antools.threading import ThreadProcess


def worker_A(lock, logger):
    p = ThreadProcess(lock, logger)
    log = p.get_logger()

    p.data = ["A", "B", "C"]
    log.info("Hello!")

    if not "D" in p.data:
        log.warning("A not in data!")
        # log.error("A not in data!") # will terminate all

    p.status = "OK"
    return p.finish(terminate_all=False)


def worker_B(lock, logger, result):
    p = ThreadProcess(lock, logger)
    log = p.get_logger()

    time.sleep(2)

    p.status = "OK"
    return p.finish(terminate_all=False)

if __name__ == "__main__":

    logger = get_logger(level="INFO", file_log=False)
    lock = threading.Lock()

    logger.info("Starting threading ... ")

    with concurrent.futures.ThreadPoolExecutor() as executor:

        p1 = executor.submit(worker_A, lock, logger)
        p2 = executor.submit(worker_A, lock, logger)

        if p2.result().status == "OK":
            p3 = executor.submit(worker_B, lock, logger, p2.result().data)

            print(p3.result().data)

    logger.info("Finishing threading ... ")
