# -*- coding: utf-8 -*-
"""
LOGGER CLASS
"""

import logging
import os
import sys
import getpass
import shutil
import inspect
from datetime import datetime
import time


class _Logger():
    """ Customizable Logger for tracking logs and catching unexpected errors.
    The class should be activated only separated method get_logger().

    ...

    Attributes
    ----------
    _logger : class, optional
        Logger class from logging library.
    _activated : bool
        Until activated, default logger, level ERROR will be returned.
    _level : str
        When not activated, default level is 'ERROR' else 'INFO'. Options are ["DEBUG", "INFO", "WARNING", "CRITICAL", "ERROR"].
    _console_log : bool
        Determines whether logging should be done to console too (default is True).
    _file_log : bool
        Determines whether logging should be done to file (default is True).
    _user_name : bool
        Name of the user (default is '<Your user profile>').
    _folder path : bool
        Folder where logs will be stored (default is <CWD>/logs).
    _process_name : str, optional
        If multiprocessing or threading is used, process_name has to be filled.
    _activated_time : str
        Holds time value when object was first activated
    _formatter
        Format of the logger.

    Methods
    -------
    __call__(msg:str)
        Works like info method
    debug(msg:str)
        Logs debug messages.
    info(msg:str)
        Logs info messages.
    warning(msg:str)
        Logs warning messages.
    critical(msg:str)
        Logs critical messages.
    error(self, msg:str, error=SystemError, terminate:bool=True)
        Logs error messages and terminates the system if wanted.
    exception(self, msg:str, error=SystemError, add_info:bool = False, terminate:bool = False)
        Logs exception messages and terminates the system if wanted.

    Examples
    ------- 
    antools/logging/_examples/_example_logger.py   
    """

    _LEVEL_OPTIONS = ["DEBUG", "INFO", "WARNING", "CRITICAL", "ERROR"]
    _logger = logging.getLogger()
    _activated = False
    _level = "ERROR"
    _console_log = False
    _file_log = False
    _user_name = getpass.getuser()
    _folder_path = os.path.join(os.getcwd(), "logs")
    _process_name = "MAIN"
    _formatter = logging.Formatter("%(asctime)s.%(msecs)03d : %(levelname)s : %(message)s", datefmt='%Y-%m-%d %H:%M:%S')


    def __init__(self):
        """ Class constructor. """
        self._logger = logging.getLogger()
        self._logger.setLevel(self._level)
        self.console_log = True


    def __repr__(self):
        return f"Logger(level={self.level})"

        
    def debug(self, msg:str):
        """ Logs debug messages.
        
        Parameters
        ----------
        msg
            Message to be logged.

        """
        self._logger.debug(self._get_msg_format() + msg)
            

    def info(self, msg:str):
        """ Logs info messages.
        
        Parameters
        ----------
        msg
            Message to be logged.
        
        """
        self._logger.info(self._get_msg_format() + msg)
        

    def warning(self, msg:str):
        """ Logs warning messages.
        
        Parameters
        ----------
        msg
            Message to be logged.
        
        """

        self._logger.warning(self._get_msg_format() + msg)
    

    def critical(self, msg:str):
        """ Logs critical messages.
        
        Parameters
        ----------
        msg
            Message to be logged.
        
        """     

        self._logger.critical(self._get_msg_format() + msg)


    def error(self, msg:str, error=SystemError, terminate:bool = True):
        """ Logs error messages and terminates the system if wanted.
        
        Parameters
        ----------
        msg : msg
            Message to be logged.
        error : Error, optional
            ErrorType (default is SystemError).
        terminate : bool, optional
            If true, Logger will shut down process (default is True).

        """

        self._logger.error(self._get_msg_format() + msg)
        if terminate:
            # change for right traceback in VSCode
            error = SystemError if error == SystemExit else error
            raise error(msg)


    def exception(self, msg:str, error=SystemError, add_info:bool = False, terminate:bool = False):
        """ Logs exception messages and terminates the system if wanted.
        
        Parameters
        ----------
        msg : msg
            message to be logged
        error : Error, optional
            ErrorType (default is SystemError)
        add_info : bool, optional
            adds traceback to the message
        terminate : bool, optional
            if true, Logger will shut down process (default is False)

        """
        self._logger.exception(self._get_msg_format() + msg, exc_info=add_info)
        if terminate:
            add_info = True
            error = SystemError if error == SystemExit else error
            raise error(msg)


    def _get_msg_format(self) -> str:
        """ Formats logger info for logging messages. """

        if self._level == "DEBUG":
            try:
                stack = inspect.stack()[2]
                path = stack.filename
                cwd = os.getcwd()
                path = "..\\" + os.path.relpath(path, cwd) if cwd in path else path
                function = stack.function if stack.function != "<module>" else "module"
                return f"{self._process_name.upper()} : {path} : line {stack.lineno} : function <{function}>" + " : "
            except:
                return f"{self._process_name.upper()} : "

        else:
            return f"{self._process_name.upper()} : "


    def _replace_traceback(self):  
        """ Replace traceback for logging unexpected errors """

        def log_traceback_system(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
      
            self._logger.error(self._get_msg_format() + "The following error cannot be handled! \n", exc_info=(exc_type, exc_value, exc_traceback))

        sys.excepthook = log_traceback_system  


    @property
    def activated(self):
        return self._activated


    @activated.setter
    def activated(self, value:str):

        if self._activated and value:
            raise ValueError("Logger has already been activated!")
        elif not isinstance(value, bool):
            raise ValueError(f"Logger attribute <activated> must be a {type(True)}, inserted value is {type(value)}!")
        else:
            self._replace_traceback()
            self._activated = True
            self._activated_time = datetime.now()


    @property
    def level(self):
        return self._level


    @level.setter
    def level(self, value:str):
        if not value in self._LEVEL_OPTIONS:
            raise ValueError(f"Logger level must be in <{self._LEVEL_OPTIONS}>!")

        self._logger.setLevel(value)
        self._level = value


    @property
    def console_log(self):
        return self._console_log
        

    @console_log.setter
    def console_log(self, value):
        if not isinstance(value, bool):
            raise ValueError(f"Logger attribute <console_log> must be a {type(True)}, inserted value is {type(value)}!")

        if value and not self._console_log:
            sh = logging.StreamHandler()
            sh.setFormatter(self._formatter)
            self._logger.addHandler(sh)
            self._console_log = True

        elif not value and self._console_log:
            for handler in self._logger.handlers:
                if isinstance(handler, logging.StreamHandler):
                    self._logger.removeHandler(handler) 
            self._console_log = False


    @property
    def file_log(self):
        return self._file_log


    @file_log.setter
    def file_log(self, value):
        if not isinstance(value, bool):
            raise ValueError(f"Logger attribute <file_log> must be a {type(True)}, inserted value is {type(value)}!")

        if value and not self._file_log:

            if self._activated and not self._file_log:
                full_path = os.path.join(self._folder_path, str(self._activated_time.year), self._activated_time.strftime('%B'), self._user_name)
                file_path = os.path.join(full_path, f"{self._activated_time.strftime('%B_%d_%Y_%H_%M_%S')}.log")

                try:
                    os.makedirs(full_path) if not os.path.isdir(full_path) else None
                except:
                    raise ValueError(f"{value} is not valid system path!")
                
                # delete old logs
                years = os.listdir(self._folder_path)
                for year_dir in years:
                    if os.path.isdir(os.path.join(self._folder_path, year_dir)):
                        if not year_dir in [str(self._activated_time.year), str(self._activated_time.year - 1)]:
                            try:
                                shutil.rmtree(os.path.join(self._folder_path, year_dir))
                            except:
                                pass

                fh = logging.FileHandler(file_path, mode='a')
                fh.setFormatter(self._formatter)
                self._logger.addHandler(fh)
                self._file_log = True


        elif not value and self._file_log:
            for handler in self._logger.handlers:
                if isinstance(handler, logging.StreamHandler):
                    self._logger.removeHandler(handler) 
            self._file_log = False


    @property
    def user_name(self):
        return self._user_name


    @user_name.setter
    def user_name(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Logger attribute <user_name> must be a <str>, inserted value is {type(value)}!")
        self._user_name = value


    @property
    def folder_path(self):
        return self._folder_path


    @folder_path.setter
    def folder_path(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Logger attribute <folder_path> must be a <str> and valid system path, inserted value is {type(value)}!")
        self._folder_path = value


    @property
    def process_name(self):
        return self._process_name


    @process_name.setter
    def process_name(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Logger attribute <process_name> must be a <str>, inserted value is {type(value)}!")
        self._process_name = value.upper()



Logger = _Logger()


def get_logger(level:str = "INFO", console_log:bool = True, file_log:bool = True,  
                user_name:str = None, folder_path:str = None, _activate:bool = True) -> Logger:
    """
    Returns Instance of Logger class

    Parameters
    ----------
    level : str, optional
        Level of the logger (default is 'INFO'). Options are ["DEBUG", "INFO", "WARNING", "CRITICAL", "ERROR"]
    console_log : bool, optional
        Determines whether logging should be done to console (default is True).
    file_log : bool, optional
        Determines whether logging should be done to file (default is True).
    user_name : str, optional
        Name of the user (default is '<Your user profile>').
    folder path : str, optional
        Folder where logs will be stored (default is <CWD>/logs).
    _activate
        !!! DO NOT CHANGE !!!

    Returns
    -------
    Instance of Logger Class

    """ 
    if _activate:
        Logger.activated = True
        if level:
            Logger.level = level
        if console_log:
            Logger.console_log = console_log
        if file_log:
            Logger.file_log = file_log
        if user_name:
            Logger.user_name = user_name
        if folder_path:
            Logger.folder_path = folder_path
        
    return Logger


def _get_mp_logger(main_logger:Logger, process_name:str) -> Logger:
    """
    Returns Instance of Logger class for multiprocessing purposes

    Parameters
    ----------
    main_logger : object
        Instance of main logger
    process_name : str
        Name of the process
    Returns
    -------
    Instance of Logger Class

    """ 

    if not main_logger._activated:
        return Logger
    else:
        Logger._activated_time = main_logger._activated_time
        Logger.level = main_logger.level
        Logger.console_log = main_logger.console_log
        Logger.file_log = main_logger.file_log
        Logger.user_name = main_logger.user_name
        Logger.folder_path = main_logger.folder_path
        Logger.process_name = process_name

        return Logger

def _get_thread_logger(main_logger:Logger, process_name:str) -> Logger:
    """
    Returns Instance of Logger class for threading purposes.

    Parameters
    ----------
    main_logger : object
        Instance of main logger
    process_name : str
        Name of the process
    Returns
    -------
    Instance of Logger Class

    """ 

    if not main_logger._activated:
        return Logger
    else:
        Logger._activated_time = main_logger._activated_time
        Logger.level = main_logger.level
        Logger.console_log = main_logger.console_log
        Logger.file_log = main_logger.file_log
        Logger.user_name = main_logger.user_name
        Logger.folder_path = main_logger.folder_path
        Logger.process_name = process_name

        return Logger