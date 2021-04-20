"""
LOGGER CLASS

@ author: Antonín Drozda
@ organization: Freelancer
@ project: Anton's Tools
@ date: 25/03/2021

Logger.
"""

# %% FILE METADATA
__title__ = "LOGGER CLASS"
__author__ = "Antonín Drozda"
__organization__ = "Freelancer"
__project__ = "Anton's Tools"
__date__ = "25/03/2021"

# %% LIBRARY IMPORT
import logging
import os
import sys
import traceback
import getpass
import platform
import shutil
import inspect
import time
import pandas as pd
from functools import wraps
from IPython.core.interactiveshell import InteractiveShell
from datetime import datetime

# %% FILE IMPORT
from antools.shared import TypeValidator
from .abstract_logger import AbstractLogger

# %% INPUTS

# %% CLASSES

class _Logger(AbstractLogger):
    """ Customized Logger class responsible for logging for antools methods
        Logs into console and into specific directory
    
    ...
    
    Attributes
    ----------
    _active: bool
        Holds value if Logger is being used or not
    _user_name : str
        Name of the user who uses the application supported by this Logger class      
    _logger_name : str, optional
        The name of the logger (default 'logger')
    _level:str, optional
        Minimal level of logging (default 'INFO')
    _time_format: str, optional
        Format of day and time the Logger uses when logging messages
    _folder_path : str, optional
        Path to the folder where log_file is stored (default os.path.join(os.getcwd(), "logs"))
    _executed_funtions
        Information about functions with track decorator

        
    Methods
    -------
    _set_logger(self)
        Creates logger and its environment
    _replace_traceback(self)
        Replace traceback with self.error function to catch unexpected errors
    _get_msg_format(self) -> str:
        Formats logger info calls for logging messages
    debug(self, msg:str)
        Logs debug messages
    info(self, msg:str)
        Logs info messages
    warning(self, msg:str)
        Logs warning messages
    critical(self, msg:str)
        Logs critical messages
    error(self, msg:str, terminate:bool = False)
        Logs error messages, performs SystemExit if intended
    exception(self, msg:str, terminate:bool = False)
        Logs error messages including SystemTraceback, used in try-except statement
        Performs SystemExit if intended
    track(self, func):
        Log all information about function, usage as decorator
    get_track_stats(self) -> pd.DataFrame:
        Returns complete statistics of funtions with logger.track decorator
    wrong_input(self, call_object:object, var_name:"str", var_value, reason:str) -> ValueError
        Raises ValueError and logs message in data is not corrent in the script
        
    Raises
    --------   
    ValueError
        If any inputs does not correspond to its intended data type.
    SystemExit
        If unexcpected error occurs in the script where this class is used
        When error or exception method runs with parameter terminate == True   
        
    Notes
    --------       
    @ author:  Antonín Drozda (https://github.com/antonin-drozda)
    @ created: 25/03/2021
    
    """
    _executed_functions = {}
      
    def __init__(self):
        self.active = False

    def __str__(self):
        return f"{self._logger_file_path}"    
    
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self._user_name}, {self._level}, {self._logger_file_path})"
            
    
    def _set_logger(self, 
                    console_log:bool = True,
                    level:str = "INFO",
                    user_name:str = getpass.getuser(),
                    logger_name:str = "logger",
                    time_format:str = "%Y-%m-%d %H:%M:%S",
                    folder_path:str = os.path.join(os.getcwd(), "logs")): 
    
        
        """
        Creates logger and its environment
        ...
        
        Parameters
        ----------
        console_log : bool
            If Logger should also print messages into console  
        user_name : str
            Name of the user who uses the application supported by this Logger class       
        logger_name : str, optional
            The name of the logger (default 'logger')
        time_format: str, optional
            Format of day and time the Logger uses when logging messages
        folder_path : str, optional
            Path to the folder where log_file is stored (default os.path.join(os.getcwd(), "logs"))
            
        """
        
        self._console_log = console_log
        self._level = level
        self._user_name = user_name
        self._logger_name = logger_name
        self._time_format = time_format
        self._folder_path = folder_path

        # check if <_console_log> is bool
        if not TypeValidator.bool(self._console_log):
            raise ValueError(f"{self.__class__.__name__} obtained invalid variable: <console_log> = <{self._console_log}>. It must be a boolean!")
                       
        # check if <_user_name> is string
        if not TypeValidator.str(self._user_name):
            raise ValueError(f"{self.__class__.__name__} obtained invalid variable: <user_name> = <{self._user_name}>. It must be a string!")
            
        # check if <_logger_name> is string
        if not TypeValidator.str(self._logger_name):
            raise ValueError(f"{self.__class__.__name__}: <logger_name> = <{self._logger_name}>. It must be a string!")
        
        # check if logging level exists
        if not self._level in ["DEBUG", "INFO", "WARNING", "CRITICAL", "ERROR"]:
            raise ValueError(f"{self.__class__.__name__}: <level> = <{self._level}>. It is not valid logging level!")
            
        # check if path exists or can be created
        if not os.access(os.path.dirname(self._folder_path), os.W_OK):
            raise ValueError("{self.__class__.__name__}: <folder_path> = <{self._folder_path}>. It is invalid system path!")
            
        # check if run on Windows
        if not platform.system() == "Windows":
            raise SystemExit("{self.__class__.__name__}: is not yet supported on other than Windows operating system!")  
            
            
        
        # set logger
        self.logger = logging.getLogger(self._logger_name)
        self.logger.setLevel(self._level)
        now = datetime.now()
        full_path = os.path.join(self._folder_path, str(now.year), now.strftime('%B'), self._user_name)
        self._logger_file_path = os.path.join(full_path, f"{now.strftime('%B-%d-%Y_%H_%M_%S')}.log")
        
        # if <folder> does not exist, create it
        os.makedirs(full_path) if not os.path.isdir(full_path) else None
        
        # delete old logs
        years = os.listdir(self._folder_path)
        for year_dir in years:
            if os.path.isdir(os.path.join(self._folder_path, year_dir)):
                if not year_dir in [str(now.year), str(now.year - 1)]:
                    try:
                        shutil.rmtree(os.path.join(self._folder_path, year_dir))
                    except:
                        pass
                    
        # if Class with same name is called more than once, do not add handlers
        if len(self.logger.handlers) == 0:
            formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(message)s", self._time_format)             
            fh = logging.FileHandler(self._logger_file_path, mode='w')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
            
            if console_log:
                sh = logging.StreamHandler()
                sh.setFormatter(formatter)
                self.logger.addHandler(sh)
          
            self.debug(f"<{self._logger_name}> has been initialized!")
            
            # replace traceback to handle unhandled errors
            self._replace_traceback()

        self.active = True
        
    def _replace_traceback(self):  
        """ Replace traceback with self.error function to catch unexpected errors
        
        Parameters
        ----------
        None
        
        """
        
        # when run in python system
        def log_traceback_system(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            
            # if any function used track decorator
            if self._executed_functions:
                self.info(f"\n {self.get_track_stats()}\n")
                pd.set_option("display.max_rows", None, "display.max_columns", None)
                
            self.logger.error(self._get_msg_format() + "Serious error has been encountered! System must be terminated! \n", exc_info=(exc_type, exc_value, exc_traceback))
             
        sys.excepthook = log_traceback_system
        
        # when run in spyder       
        def log_traceback_spyder(func):    
            @wraps(func)
            def handle_exception(*args, **kwargs):
                # if any function used track decorator
                if self._executed_functions:
                    self.info(f"\n {self.get_track_stats()}\n")
                    pd.set_option("display.max_rows", None, "display.max_columns", None)
                self.error(self._get_msg_format() + "Serious error has been encountered! System must be terminated! \n" + traceback.format_exc(limit=20), terminate=False)                

            return handle_exception
        
        InteractiveShell.showtraceback = log_traceback_spyder(InteractiveShell.showtraceback)
        
    def _get_msg_format(self) -> str:
        """ Formats logger info for logging messages """
        
        if self._level == "DEBUG":
            stack = inspect.stack()[2]
            path = stack.filename
            cwd = os.getcwd()
            path = "..\\" + os.path.relpath(path, cwd) if cwd in path else path
            function = stack.function if stack.function != "<module>" else "module"
            return f"[{self._user_name}]" + " : " + f"{path} : line {stack.lineno} : function <{function}>" + " : "
        else:
            return f"[{self._user_name}]" + " : "
     
        
    def debug(self, msg:str):
        """ Logs debug messages
        
        Parameters
        ----------
        msg
            Message to be logged
        
        """
        
        self.logger.debug(self._get_msg_format() + msg)


    def info(self, msg:str):
        """ Logs info messages
        
        Parameters
        ----------
        msg
            Message to be logged
        
        """

        self.logger.info(self._get_msg_format() + msg)
        
    def warning(self, msg:str):
        """ Logs warning messages
        
        Parameters
        ----------
        msg
            Message to be logged
        
        """
        self.logger.warning(self._get_msg_format() + msg)
    
    
    def critical(self, msg:str):
        """ Logs critical messages.
        
        Parameters
        ----------
        msg
            Message to be logged
        
        """
        self.logger.critical(self._get_msg_format() + msg)      
                
        
    def error(self, msg:str, terminate:bool = True):
        """ Logs error messages, performs SystemExit if intended
        
        Parameters
        ----------
        msg : str
            Message to be logged
        terminate : bool
            If True, performs SystemExit
        """
                
        
        if not terminate:
            self.logger.error(self._get_msg_format() + msg)
        else:
            if not self._console_log:
                print("ERROR: " + self._get_msg_format() + msg)
            raise SystemExit(msg)

    def exception(self, msg:str, add_info:bool = False, terminate:bool = False):
        """ Logs error messages including SystemTraceback, used in try-except statement
        Performs SystemExit if intended
        
        Parameters
        ----------
        msg : str
            Message to be logged
        terminate : bool
            If True, performs SystemExit
        """
        
        # if script is terminated, include info automatically
        add_info = True if terminate else add_info   
        self.logger.exception(self._get_msg_format() + msg, exc_info=add_info)
        if terminate:
            if not self._console_log:
                print("ERROR: " + self._get_msg_format() + msg)
            raise SystemExit(msg)



    def track(self, func):
        """Log all information about function, usage as decorator"""
        
        function_fn = f"{func.__module__}.{func.__name__}"
        if not function_fn in self._executed_functions:
            self._executed_functions[function_fn] = {"run_times": 0,
                                                    "total_time": 0,
                                                    "avg_time": 0,
                                                    "min_time": 999999,
                                                    "max_time": 0,
                                                    "last_input": None,
                                                    "last_output": None,
                                                    "last_time": 0}
            
        @wraps(func)
        def log_track(*args, **kwargs):
            start_time = time.perf_counter()    
            value = func(*args, **kwargs)
            end_time = time.perf_counter()      
            run_time = end_time - start_time
            
            func_data = self._executed_functions[function_fn]
            func_data["run_times"] += 1
            func_data["total_time"] += run_time
            func_data["avg_time"] = func_data["total_time"] / func_data["run_times"]
            
            func_data["min_time"] = run_time if func_data["min_time"] > run_time else func_data["min_time"]
            func_data["max_time"] = run_time if func_data["max_time"] < run_time else func_data["max_time"]
            
            func_data["last_input"] = {"args": args, "kwargs": args}
            func_data["last_output"] = value
            func_data["last_time"] = run_time
            
            if self._level == 'DEBUG':
                self.logger.debug(f"""\nFunction: {func.__module__}.{func.__name__}
                             
Input: args={args},\nkwargs={kwargs}
Output: {value}
Time: {run_time:.4f} secs\n""")
            return value
        return log_track
    
    
    def get_track_stats(self) -> pd.DataFrame:
        """ Returns complete statistics of funtions with logger.track decorator"""
        data = pd.DataFrame(self._executed_functions)
        data = data.transpose()
        if not data.empty:
            data = data.sort_values(by=["total_time"], ascending=False)
            
        return data
    
    
    def wrong_input(self, call_object:object, var_name:"str", var_value, reason:str) -> ValueError:
        """ Used in classes for checking right DataType """
        
        object_name = call_object.__class__.__name__ if isinstance(call_object, object) else object
        msg = f"{object_name} obtained invalid parameter <{var_name}> = <{var_value}>. IT IS {reason}!"
        raise ValueError(msg)

# %% CREATE LOGGER INSTANCE        
_LOGGER = _Logger() 

# %% NOTES