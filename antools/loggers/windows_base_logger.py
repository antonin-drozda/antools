"""
WINDOWS BASE LOGGER

@ author: Antonín Drozda
@ organization: Freelancer
@ project: Anton's Tools
@ date: 28/02/2021

Base Logger for Windows OS
"""

# %% FILE METADATA
__title__ = "WINDOWS BASE LOGGER"
__author__ = "Antonín Drozda"
__organization__ = "Freelancer"
__project__ = "Anton's Tools"
__date__ = "28/02/2021"

# %% LIBRARY IMPORT
import logging
import os
import inspect
import re
import sys
import traceback
from functools import wraps
from IPython.core.interactiveshell import InteractiveShell
from datetime import datetime

# %% FILE IMPORT

# %% INPUTS

# %% CLASSES
class WindowsBaseLogger:
    r"""
    Customized Logger class responsible for logging through entire code adjusted for Windows OS use
    Logs into console and into specific directory

    ...

    Attributes
    ----------
    _user_name : str
        Name of the user who uses the application supported by this Logger class      
    _dev_mode : bool, optional
        Switcher between normal user and developer logging (default True)
    _logger_name : str, optional
        The name of the logger (default 'logger')
    _time_format: str, optional
        Format of day and time the Logger uses when logging messages
    _folder_path : str, optional
        Path to the folder where log_file is stored (default os.path.join(os.getcwd(), "logs"))
    _SUPPORTED_OS: list
        List of supported operating systems Logger can run on

    Methods
    -------
    _check_inputs(self)
        Checks validity of class inputs during Class initialization
    _setup_logger(self)
        Creates logger and its environment
    _replace_traceback(self)
        Replace traceback with self.error function to catch unexpected errors
    pfx(self)
        Returns string of path from cwd and file line where method was performed
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
       
    Raises
    --------   
    ValueError
        If any inputs does not correspond to its intended data type.
    SystemExit
        If unexcpected error occurs in the script where this class is used
        When error or exception method runs with parameter terminate == True
        
    Examples
    --------   
    
    if _dev_mode:
        
        log.debug(log.pfx() + "Hello!") 
        >>> 20:54:56 : DEBUG : <USER_NAME> : \logger_class.py : line 70 : Hello!

        log.debug("Hello!") 
        >>> 20:54:56 : DEBUG :  <USER_NAME> : Hello!    
        
    if not _dev_mode: (no file and line location, no debug messages)
        
        log.debug(log.pfx() + "Hello!") 
        >>> 20:54:56 : DEBUG : <USER_NAME> : Hello!

        log.debug("HELLO") 
        >>> None
        
        log.info(log.pfx() + "Hello!") 
        >>> 20:54:56 : INFO :  <USER_NAME> : Hello!     
        
    Notes
    --------       
    @ author:  Antonín Drozda (https://github.com/antonin-drozda)
    @ created: 28/02/2021
    
    """
      
    def __init__(self, 
                 user_name:str = "UNKNOWN USER",
                 dev_mode:bool = True, 
                 logger_name:str = "logger", 
                 time_format:str = "%Y-%m-%d %H:%M:%S",
                 folder_path:str = os.path.join(os.getcwd(), "logs")):
        """
        ...
        
        Parameters
        ----------
        user_name : str
            Name of the user who uses the application supported by this Logger class       
        dev_mode : bool, optional
            Switcher between normal user and developer logging (default True)
        logger_name : str, optional
            The name of the logger (default 'logger')
        time_format: str, optional
            Format of day and time the Logger uses when logging messages
        folder_path : str, optional
            Path to the folder where log_file is stored (default os.path.join(os.getcwd(), "logs"))
            
        """
                
        self._user_name = user_name
        self._dev_mode = dev_mode
        self._logger_name = logger_name
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
        if not isinstance (self._user_name, str): 
            raise ValueError(f"Logger obtained invalid variable: <user_name> = <{self._user_name}>. It must be a string!")
            
        # check if <_dev_mode> is boolean
        if not isinstance (self._dev_mode, bool):            
            raise ValueError(f"Logger obtained invalid variable: <dev_mode> = <{self._dev_mode}>. It must be a boolean!")
            
        # check if <_logger_name> is string
        if not isinstance (self._logger_name, str):
            raise ValueError(f"Logger obtained invalid variable: <logger_name> = <{self._logger_name}>. It must be a string!")
                
        # check if path exists or can be created
        if not os.access(os.path.dirname(self._folder_path), os.W_OK):
            raise ValueError("Logger obtained invalid variable <folder_path> = <{self._folder_path}>. Invalid system path!")
            
            
    def _setup_logger(self):        
        """ Creates logger and its environment 
        
        Parameters
        ----------
        None
        
        """
        
        self.logger = logging.getLogger(self._logger_name)
        
        # if runs as <dev_mode> level == DEBUG, else INFO
        if self._dev_mode:            
            self.logger.setLevel("DEBUG")
        else:
            self.logger.setLevel("INFO")
        
        now = datetime.now()
        full_path = os.path.join(self._folder_path, self._logger_name, str(now.year), now.strftime('%B'))
        
        # if <folder> does not exist, create it
        if not os.path.isdir(full_path):
            os.makedirs(full_path)
        
        # if Class with same name is called more than once, do not add handlers
        if len(self.logger.handlers) == 0:
            formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(message)s", self._time_format)
                            
            fh = logging.FileHandler(os.path.join(full_path, f"{now.strftime('%B-%d-%Y')}.log"), mode='w')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
        
            sh = logging.StreamHandler()
            sh.setFormatter(formatter)
            self.logger.addHandler(sh)
          
            self.debug(self.pfx() + f"Logger <{self._logger_name}> has been initialized!")
            
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

            self.logger.error("Serious error has been encountered! System must be terminated!", exc_info=(exc_type, exc_value, exc_traceback))
            
        sys.excepthook = log_traceback_system
        
        # when run in spyder       
        def log_traceback_spyder(func):    
            @wraps(func)
            def handle_exception(*args, **kwargs):
                self.error("Serious error has been encountered! System must be terminated! \n" + traceback.format_exc(limit=1), terminate=False)                

            return handle_exception
        
        InteractiveShell.showtraceback = log_traceback_spyder(InteractiveShell.showtraceback)
            
    def pfx(self):
        """ Returns string of path from cwd and file line where method was performed
        
        Parameters
        ----------
        None
        
        Returns
        ----------
        String of path from cwd and file line where method was performed
        
        Examples
        ----------
        
        self.pfx()
        
        if _dev_mode: 
        >>> /logger_class.py : line 203
        
        if not _dev_mode:
        >>> ''
        
        self.info(self.pfx() + "Hello!")
        
        if _dev_mode: 
        >>> 08:01:40 : INFO : <USER_NAME> : /logger_class.py : line 203 : Hello!
        
        if not _dev_mode:
        >>> 08:01:40 : INFO : <USER_NAME> : Hello!
        
        """ 
        # returns filename in cwd hiearchy + lineno where log was called
        if self._dev_mode:
            info = inspect.getframeinfo(inspect.stack()[1][0])
            cwd_name = re.split(r"\\", os.getcwd())[-1]
            filename = re.split(cwd_name, info.filename)[-1]
            return filename + " : " + "line " + str(info.lineno) + " : "
        else:
            return ""
        
    def debug(self, msg:str):
        """ Logs debug messages
        
        Parameters
        ----------
        msg
            Message to be logged
        
        """
        
        self.logger.debug(self._user_name + " : " + msg)

    def info(self, msg:str):
        """ Logs info messages
        
        Parameters
        ----------
        msg
            Message to be logged
        
        """
        self.logger.info(self._user_name + " : " + msg)

    def warning(self, msg:str):
        """ Logs warning messages
        
        Parameters
        ----------
        msg
            Message to be logged
        
        """
        self.logger.warning(self._user_name + " : " + msg)
    
    def critical(self, msg:str):
        """ Logs critical messages.
        
        Parameters
        ----------
        msg
            Message to be logged
        
        """
        self.logger.critical(self._user_name + " : " + msg)      
                    
    def error(self, msg:str, terminate:bool = True):
        """ Logs error messages, performs SystemExit if intended
        
        Parameters
        ----------
        msg : str
            Message to be logged
        terminate : bool
            If True, performs SystemExit
        """
                
        self.logger.error(self._user_name + " : " + msg)
        
        if terminate:
            self.logger.error(self._user_name + " : " + "This error cannot be handled! System Down!")
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
        if terminate:
            add_info = True
            
        self.logger.exception(self._user_name + " : " + msg, exc_info=add_info)
        
        if terminate:
            self.logger.error(self._user_name + " : " + "This error cannot be handled! System Down!")
            raise SystemExit(msg)
    
# %% NOTES
