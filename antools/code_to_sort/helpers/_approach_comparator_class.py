# -*- coding: utf-8 -*-
"""
APPROACH COMPARATOR CLASS
"""

import concurrent.futures
import time
import os
import numpy as np
from antools.logging import get_logger
from antools.multiprocessing import MultiProcess
from antools.threading import ThreadProcess


class _AbstractLock():
    """ Abstract Lock for threading/multiprocessing locking simulation """
    
    acquired = False

    def acquire(self):
        while self.acquired:
            time.sleep(0.005)
        self.acquired = True

    def release(self):
        self.acquired = False


class ApproachComparator():
    """ Customizable Logger for tracking logs and catching unexpected errors.
    The class should be activated only separated method get_logger().

    ...

    Attributes
    ----------
    results: dict
        Sorted data from performed processed
    _func: method
        Function to be tested, must be in format -> func(args:list = [], lock)
    _args: list
        List which should be passed to test function
    _abstract_lock : object
        Lock with acquire and release funtion, which does nothing
    _logger: Logger
        Logger object
        
    
    Methods
    -------
    __init__(self, func, args=None)
        Class constructor.
     __call__(self)
        When class instance is called, it compare results and print them.
    compare_all(self, max_workers:list or int=None, mp_lock:object=None, thread_lock:object=None, 
                    run_main:bool=True, run_threading:bool=True, run_mp:bool=True, batch_only:bool=True)
        Compare all processed instructed by user and prints results.
    main(self)
        Run simple python process.
    multiprocessing(self, max_workers=os.cpu_count(), lock=None,  batch=True)
        Run multiprocessing.
    threading(self, max_workers=os.cpu_count(), lock=None,  batch=True)
        Run threading.

    Examples
    ------- 
    antools/helpers/_examples/_example_approach_comparator.py   
    """

    data = {}
    _abstract_lock = _AbstractLock()


    def __init__(self, func, args=None, logger:object=None):
        """ Class constructor.

        Parameters
        ----------
        _func: method
            Function to be tested, must be in format -> func(args:list = [], lock).
        _args: list, optional
            List which should be passed to test function (default is None).
        _logger
            Class for logging messages
        """     

        self._logger = get_logger(_activate=False) if not logger else logger
        self._func = func
        self._args = [] if not args else args

    def __call__(self):
        """ When class instance is called, it compare results and print them."""

        print("\n")
        print("###################")
        print("  PROCESS RESULTS  ")
        print("###################")
        print("")

        if not self.results:
            print("NO RESULTS")
        else:
            i = 0
            last_value = self.results[list(self.results)[-1]]
            for key, value in self.results.items():
                i+=1
                if last_value != value:
                    comparison = f" ({round(last_value/value, 2)}x faster)"
                else:
                    comparison = " (slowest)" if not len(self.results) == 1 else ""

                print(f"{str(i)}. {key} -> {value} seconds {comparison}")
            
            print("\n")


    def compare_all(self, max_workers:list or int=None, mp_lock:object=None, thread_lock:object=None, 
                    run_main:bool=True, run_threading:bool=True, run_mp:bool=True, batch_only:bool=True):
        """ Compare all processed instructed by user and prints results.

        Parameters
        ----------
        max_workers: list or int
            Maximum mumber of workers which should be run (default is None -> try multiple possibilities including maximum).
        mp_lock: object, optional
            Instance of multiprocessing lock created in main function (default is None).
        thread_lock: object, optional
            Instance of thread lock created in main function (default is None).
        run_main : bool
            Run simple Python (default is True).
        run_mp : bool
            Run multiple_processing (default is True).
        run_thread : bool
            Run threading (default is True).
        batch_only: bool
            Set False if possibility not using batching should be used
        """ 

        if not max_workers:
            max_cpu = os.cpu_count()
            max_workers = []
            for i in range(1, 13):
                if 2**i <= max_cpu:
                    max_workers.append(2**i)
                else:
                    max_workers.append(max_cpu) if not (max_cpu) in max_workers else None
                    break
              
        elif isinstance(max_workers, int):
            max_workers = [max_workers]

        for workers in max_workers:
            batches = [True, False] if not batch_only else [True]
            for batch in batches:
                if run_mp:
                    lock=mp_lock
                    self.multiprocessing(workers, lock, batch)
                if run_threading:
                    lock=thread_lock
                    self.threading(workers, lock, batch)

        if run_main:
            self.main()

        # print results
        self()


    def main(self):
        """ Run simple python process """
        lock = self._abstract_lock
        print(f"Starting single thread ... ")
        st = time.perf_counter()
        [self._func(value, lock) for value in self._args]
        process_time = round(time.perf_counter() - st, 5)
        print(f"Process finished. Total time {process_time} seconds.")
        self.data[f"Main"] = process_time
        return process_time


    def multiprocessing(self, max_workers=os.cpu_count(), lock=None,  batch=True):
        """ Run multiprocessing.

        Parameters
        ----------
        max_workers: list or int
            Maximum mumber of workers which should be run (default is os.cpu_count()).
        lock: object, optional
            Instance of multiprocessing lock created in main function (default is None).
        batch_only: bool
            Set False if batching is not wanted (default = True).
        """

        args = self._args if not batch else np.array_split(self._args, max_workers)
        batch_msg = "True" if batch else "False"
        lock_msg = "True" if lock else "False"
        lock = self._abstract_lock if not lock else lock

        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            print(f"Starting multiprocessing (max_workers={max_workers}, lock={lock_msg}, batch={batch_msg}) ...")
            st = time.perf_counter()
            proc_results = [executor.submit(self._run_multiprocess, self._func, curr_args, lock, batch) for curr_args in args]

            for f in concurrent.futures.as_completed(proc_results):
                f.result()

        process_time = round(time.perf_counter() - st, 5)
        print(f"Process finished. Total time: {process_time} seconds.")
        self.data[f"Multiprocessing(max_workers={max_workers}, lock={lock_msg}, batch={batch_msg})"] = process_time
        return process_time


    def threading(self, max_workers=os.cpu_count(), lock=None,  batch=True):
        """ Run threading.

        Parameters
        ----------
        max_workers: list or int
            Maximum mumber of workers which should be run (default is os.cpu_count()).
        lock: object, optional
            Instance of thread lock created in main function (default is None).
        batch_only: bool
            Set False if batching is not wanted (default = True).
        """

        args = self._args if not batch else np.array_split(self._args, max_workers)
        batch_msg = "True" if batch else "False"
        lock_msg = "True" if lock else "False"
        lock = self._abstract_lock if not lock else lock

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            print(f"Starting threading (max_workers={max_workers}, lock={lock_msg}, batch={batch_msg}) ...")
            st = time.perf_counter()
            proc_results = [executor.submit(self._run_multiprocess, self._func, curr_args, lock, batch) for curr_args in args]

            for f in concurrent.futures.as_completed(proc_results):
                f.result()

        process_time = round(time.perf_counter() - st, 5)
        print(f"Process finished. Total time: {process_time} seconds.")
        self.data[f"Threading(max_workers={max_workers}, lock={lock_msg}, batch={batch_msg})"] = process_time
        return process_time
    

    @property
    def results(self) -> dict:
        """ Returns data dict soreted by time """
        return {k: v for k, v in sorted(self.data.items(), key=lambda item: item[1])}


    def _run_multiprocess(self, func, args:list, lock:object, batch:bool) -> object:
        """ Run function from self.multiprocessing() """
        p = MultiProcess(lock, self._logger)
        func(args, lock) if not batch else [func(value, lock) for value in args]
        p.status = "OK"
        return p.finish(terminate_all=True)


    def _run_thread(self, func, args:list, lock:object, batch:bool) -> object:
        """ Run function from self.threading() """
        p = ThreadProcess(lock, self._logger)
        p.data = func(args, lock) if not batch else [func(value, lock) for value in args]
        p.status = "OK"
        return p.finish(terminate_all=True)