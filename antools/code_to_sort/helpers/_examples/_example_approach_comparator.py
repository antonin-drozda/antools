# -*- coding: utf-8 -*-
"""
HELPERS EXAMPLES
"""

# APPROACH COMPARATOR
from antools.helpers import ApproachComparator
import multiprocessing as mp
import threading

def _is_prime(args, lock):
    num = args[0]
    num_2 = args[1]
    is_prime = False

    lock.acquire()
    if not num == 1:
            for value in range(2, int(num/2)+1):
                if num % value == 0:
                    break
                is_prime = True

    lock.release()
    return is_prime

if __name__ == "__main__":
    mp_lock = mp.Manager().Lock()
    thread_lock = threading.Lock()

    NUMS = []
    for i in range (1, 1000):
        NUMS.append([i, i+1])

    mp_lock = mp.Manager().Lock()
    thread_lock = threading.Lock()

    Comparator = ApproachComparator(_is_prime, args=NUMS)
    # Comparator.compare_all()
    # Comparator.multiprocessing()
    Comparator()