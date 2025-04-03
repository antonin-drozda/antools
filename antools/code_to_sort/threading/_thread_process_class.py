# -*- coding: utf-8 -*-
"""
MULTIPROCESS CLASS
"""

# lib import
import inspect
from antools.logging._logger_class import _get_thread_logger


class ThreadProcess():
    """ Process used in threading subprocess. Used for logging and handling workflow.

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
            Lock from threading libraty.
        _logger : object
            New logger instance from main_logger.


        Methods
        -------
        __init__(self, lock:mp.Manager().Lock(), main_logger:object)
            Class constructor.
        get_logger(self):
            Returns Logger class for loggin in threading.
        lock(self)
            Lock threading lock.
        release(self)
            Release threading lock
        log(self, level:str, msg:str, terminate:bool=None, error=SystemError):
            Logs messages. 
        finish(self, terminate_all:bool=True)
            Evaluates and finish the process.  

        Examples
        ------- 
        antools/threading/_examples/_example_thread_process_class.py
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


    def __init__(self, lock:object, main_logger:object, log:bool=True):
        """ Class constructor.

        Parameters
        ----------
        lock
            Instance of threading.lock() from main process
        logger
            Instance of logger from main process
        log
            If messages process messages should be logged
        """     

        self._lock = lock
        self._process_name = inspect.stack()[1].function   
        activate = True if main_logger else False
        self._logger = _get_thread_logger(main_logger=main_logger, process_name= self._process_name)   
        self._log = log
        self._started = True
        self._processing = True
        self.status = "PROCESSING"
        self._logger.info("Process has started!") if self._log else None


    def __repr__(self):
        """ Representative string. """
        return f"MPProcess(name={self._process_name}, status={self.status}, _started={self._started}, _processing={self._processing}, _finished={self._finished})"


    def __call__(self, msg:str):
        """ Logs info messages. """
        self.log(msg)


    def get_logger(self):
        """ Returns Logger class for logging in thread. """
        return self._logger


    def lock(self):
        """ Lock threading lock. """
        self._lock.acquire()


    def release(self):
        """ Release threading lock """
        self._lock.release()


    def finish(self, terminate_all:bool=False):
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

