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
from functools import wraps
from IPython.core.interactiveshell import InteractiveShell
from datetime import datetime

# %% FILE IMPORT
from antools.shared import TypeValidator

# %% INPUTS

# %% CLASSES

class Logger:
    """ Customized Logger class responsible for logging for antools methods
        Logs into console and into specific directory
    
    ...
    
    Attributes
    ----------
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

        
    Methods
    -------
    _check_inputs(self)
        Checks validity of class inputs during Class initialization
    _setup_logger(self)
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
      
    def __init__(self, 
                 user_name:str = getpass.getuser(),
                 logger_name:str = "logger",
                 level:str = "INFO",
                 time_format:str = "%Y-%m-%d %H:%M:%S",
                 folder_path:str = os.path.join(os.getcwd(), "logs")):
        """
        ...
        
        Parameters
        ----------
        user_name : str
            Name of the user who uses the application supported by this Logger class       
        logger_name : str, optional
            The name of the logger (default 'logger')
        time_format: str, optional
            Format of day and time the Logger uses when logging messages
        folder_path : str, optional
            Path to the folder where log_file is stored (default os.path.join(os.getcwd(), "logs"))
            
        """
                
        self._user_name = user_name
        self._logger_name = logger_name
        self._level = level
        self._time_format = time_format
        self._folder_path = folder_path        
                       
        # automatically check inputs and create logger during __init__ method
        self._check_inputs()
        self._setup_logger()

              
    def _check_inputs(self):        
        """Checks validity of class inputs during Class initialization
        
        Parameters
        ----------
        None
        
        Raises
        ----------
        ValueError
            If any inputs does not correspond to its intended data type.
            
        """
        
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
            raise SystemExit("{self.__class__.__name__}: is not supported on other than Windows operating system!")
            
    def _setup_logger(self):        
        """ Creates logger and its environment 
        
        Parameters
        ----------
        None
        
        """
        
        self.logger = logging.getLogger(self._logger_name)
        self.logger.setLevel(self._level)
        now = datetime.now()
        full_path = os.path.join(self._folder_path, str(now.year), now.strftime('%B'), self._user_name)
        
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
                            
            fh = logging.FileHandler(os.path.join(full_path, f"{now.strftime('%B-%d-%Y')}.log"), mode='w')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
        
            sh = logging.StreamHandler()
            sh.setFormatter(formatter)
            self.logger.addHandler(sh)
          
            self.debug(f"<{self._logger_name}> has been initialized!")
            
            # replace traceback to handle unhandled errors
            self._replace_traceback()

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

            self.logger.error(self._get_msg_format() + "Serious error has been encountered! System must be terminated! \n", exc_info=(exc_type, exc_value, exc_traceback))
            
        sys.excepthook = log_traceback_system
        
        # when run in spyder       
        def log_traceback_spyder(func):    
            @wraps(func)
            def handle_exception(*args, **kwargs):
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
            raise SystemExit(msg)

    def wrong_input(self, call_object:object, var_name:"str", var_value, reason:str) -> ValueError:
        """ Used in classes for checking right DataType """
        
        object_name = call_object.__class__.__name__ if isinstance(call_object, object) else object
        msg = f"{object_name} obtained invalid parameter <{var_name}> = <{var_value}>. IT IS {reason}!"
        raise ValueError(msg)
            
# create Logger instance
LOGGER_LEVEL = "INFO"
logger = Logger(level=LOGGER_LEVEL)    
# %% NOTES