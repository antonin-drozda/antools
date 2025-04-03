# -*- coding: utf-8 -*-
"""
MULTIPROCESS CLASS
"""

# lib import
import inspect
from antools.logging import get_logger
from antools.logging._logger_class import _get_mp_logger


class MultiProcess():
    """ Process used in multiprocessing subprocess. Used for logging and handling workflow.

        ...

        Attributes
        ----------
        status : str
            Process status. Options are ["OK", "FAIL", "PROCESSING"]. Default is "OK".
        error : str
            If process failed, reason for it should be held here
        data : ?
            Data for further purposes should be held here
        _started : bool
            Value True if Process has started.
        _processing : bool
            Value True if Process is active.
        _finished : bool
            Value True if Process has finished.
        _lock : object
            Lock from multiprocessing library.
        _logger : object
            New logger instance from main_logger.


        Methods
        -------
        __init__(self, lock:mp.Manager().Lock(), main_logger:object)
            Class constructor.
        get_logger(self):
            Returns Logger class for loggin in multiprocess.
        lock(self)
            Lock multiprocessing lock.
        release(self)
            Release multiprocessing lock
        finish(self, terminate_all:bool=True)
            Evaluates and finish the process.       

        Examples
        ------- 
        antools/multiprocessing/_examples/_example_mp_process_class.py
        """    

        
    STATUS_OPTIONS = ["OK", "ERROR", "PROCESSING"]

    status = "OK"
    error = None
    data = None

    _started = False
    _processing = False
    _finished = False

    _logger = None
    _lock = None


    def __init__(self, lock:object, main_logger:object=None, log:bool = True):
        """ Class constructor.

        Parameters
        ----------
        lock
            Instance of multiprocess.Manager().lock() from main process
        logger
            Instance of logger from main process
        log
            If messages process messages should be logged
        """     

        self._lock = lock
        self._process_name = inspect.stack()[1].function   
        self._log = log
        activate = True if main_logger else False
        main_logger = get_logger(_activate=False) if main_logger is None else main_logger
        self._logger = _get_mp_logger(main_logger=main_logger, process_name= self._process_name)   
        self._started = True
        self._processing = True
        self.status = "PROCESSING"
        self._logger.info("Process has started!") if self._log else None


    def __repr__(self) -> str:
        """ Representative string. """
        return f"MPProcess(name={self._process_name}, status={self.status}, _started={self._started}, _processing={self._processing}, _finished={self._finished})"


    def get_logger(self) -> object:
        "Returns Logger class for logging in multiprocess."
        return self._logger


    def lock(self):
        """ Lock multiprocessing lock. """
        self._lock.acquire()


    def release(self):
        """ Release multiprocessing lock """
        self._lock.release()


    def finish(self, terminate_all:bool=False) -> object:
        """ Evaluates and finish the process.

        Parameters
        ----------
        terminate_all : bool
            If mistake will be found, the system will shut down.

        Returns
        ----------
        self

        """

        if self.error:
            self.status = "ERROR"
        if self.status == "OK":
            if self._log:
                self._logger.info("Process finished successfully!") if not self.data is None else self._logger.warning("Process finished successfully, but returning no data!")
        elif self.status == "PROCESSING":
            self.status = "ERROR"  
            self._logger.error("Process finished while still processing!", terminate=terminate_all)
        elif self.status == "ERROR":
            self.error = self.error if self.error else "UNKNOWN ERROR"
            self._logger.error(f"Process failed due to <{self.error}>!", terminate=terminate_all)
        else:
            self._logger.error(f"Process finished, however status is invalid <{self.status}>. Status must be in {self.STATUS_OPTIONS}!", terminate=terminate_all)
            self.error = f"Invalid status name <{self.status}>"
            self.status = "ERROR"

        self._processing = False
        self._finished = True

        return self

