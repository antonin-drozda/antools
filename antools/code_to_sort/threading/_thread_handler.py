# -*- coding: utf-8 -*-
"""
THREADING HANDLER
"""

import os
import concurrent.futures
import time
import numpy as np
from antools.threading import ThreadProcess


class ThreadHandler():
    """ Handler used in threading.

        ...

        Attributes
        ----------
        _logger : object
            Logger class.

        Methods
        -------
        __init__(self, logger:object)
            Class constructor.
        run_schedule(self):
            Run multiplefunctions dependent between themselves.
        run_func(self)
            Run function in multiprocess.

        Examples
        ------- 
        antools/threading/_examples/_example_threading_handler.py
        """    

    def __init__(self, logger):
        """ Class constructor. """
        self._logger = logger


    def run_schedule(self, schedule:dict, max_workers:int = os.cpu_count(), lock:object = None) -> dict:
        """ Run multiple functions dependent between themselves.

        Parameters
        ----------
        schedule : dict
            Key -> name of function
            Value -> list of names of dependent functions or directly dependent function
        max_workers : int
            Max workers used for the process.
        lock
           Threading lock.

        Returns
        ----------
        Dictionary with results
        """
        
        waiting_processes = {}
        run_processes = {}
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)

        for func, dependencies in schedule.items():
            dependencies = [] if dependencies is None else dependencies
            dependencies = [dependencies] if not isinstance(dependencies,list) else dependencies
            waiting_processes[func] = dependencies


        self._logger.info(f"Starting threading schedule with {max_workers} workers ...")
        main_loop = True
        while main_loop:

            finished = True

            # if no processes waiting to be done
            if not waiting_processes:
                break

            new_funcs_waiting = []
            for func, dependencies in waiting_processes.items():
                func_to_be_done = True
                for dependency in dependencies:

                    # check if dependent function is running, else skip
                    if dependency not in run_processes:
                        func_to_be_done = False
                        break

                if func_to_be_done:
                    new_funcs_waiting = [].append(func)

                # if dependency is in running_processes, check if it is finished
                if func_to_be_done:
                    for dependency in dependencies:
                        if run_processes[dependency]._state != "FINISHED":
                            func_to_be_done = False
                            break

                    # if all dependencies are finished, run it
                    if func_to_be_done:
                        data = dict()
                        for dependency in dependencies:
                            data[func.__name__] = run_processes[dependency].result().data

                        p = executor.submit(func, lock, self._logger, data)
                        run_processes[func] = p


            # delete new run functions in waiting processes
            for func in run_processes:
                if func in waiting_processes:
                    del waiting_processes[func]

            if waiting_processes:
                finished = False

            # if there remains functions dependent on each other, raise Error
            elif waiting_processes and not new_funcs_waiting:
                self._logger.error(f"Function dependencies are corrupted! Remaining dependent functions -> {list(waiting_processes)}", ValueError)
                return False

            else:
                for func, process in run_processes.items():
                    if process._state != "FINISHED":
                        finished = False

            if not finished:
                time.sleep(0.1)

        # wait for all to be finished
        while True:
            finished = True
            for func, process in run_processes.items():
                if process._state != "FINISHED":
                    finished = False

            # if all finished
            if finished:
                status_list = []
                for func, process in run_processes.items():
                    data[func.__name__] = {"status": f"{process.result().status}",
                                           "data": f"{process.result().data}",
                                           "error": f"{process.result().error}"}

                    status_list.append(process.result().status)
                msg = f"Thread schedule is finished! TOTAL_RUN={len(status_list)}, OK={status_list.count('OK')}, ERROR={status_list.count('ERROR')}"
                self._logger.info(msg) if status_list.count("OK") == len(status_list) else self._logger.error(msg, terminate=False)

                return data


    def run_func(self, func, args:list, max_workers:int = os.cpu_count(), lock:object = None) -> list:
        """ Run function in threading.

        Parameters
        ----------
        func
            Name of function
        args : list
            List of data which should be processed
        max_workers : int
            Max workers used for the process.
        lock
            Threading lock.

        Returns
        ----------
        List with results
        """

        # split args to multiple arrays by max_workers
        args = np.array_split(args, max_workers)

        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            self._logger.info(f"Spliting function <{func}> into {max_workers} threads ...")
            proc_results = [executor.submit(self._run_threading, func, curr_args, lock) for curr_args in args]

        data = []
        i = 0
        for process in proc_results:
            data.append(process.result().data)

        status_list = []
        for process in proc_results:
            status_list.append(process.result().status)

        msg = f"Threading function <{func.__name__}> is finished! TOTAL_RUN={len(status_list)}, OK={status_list.count('OK')}, ERROR={status_list.count('ERROR')}"
        self._logger.info(msg) if status_list.count("OK") == len(status_list) else self._logger.error(msg, terminate=False)

        # RETURN FLAT LIST OF RESULTS
        return [item for sublist in data for item in sublist]


    def _run_threading(self, func, args:list, lock:object) -> object:
        """ Split function. """

        p = ThreadProcess(lock, self._logger, log=False)

        p.data = []
        try:
            for value in args:
                p.data.append(func(value, lock))
            p.status = "OK"
        except Exception as err:
            p._logger.exception(f"Threading failed due to: {err}", add_info=True, terminate=True)
            p.status = "ERROR"
            p.error = err

        return p.finish(terminate_all=True)


