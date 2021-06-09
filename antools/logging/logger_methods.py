# -*- coding: utf-8 -*-
"""
LOGGER METHODS
"""

# %% LIBRARY IMPORT
import getpass

# %% FILE IMPORT
from antools.logging.logger_class import _LOGGER
from antools.logging.dummy_logger import _DUMMY_LOGGER

# %% INPUTS
LOGGER_LEVEL = "INFO"

# %% CLASSES              
def set_logger(console_log:bool = True,
               level:str = "INFO",
               user_name:str = getpass.getuser(),
               **kwargs):
    
    if not _LOGGER.active:
        _LOGGER._set_logger(console_log, level, user_name, **kwargs)
    return _LOGGER

def get_logger():
    return _LOGGER if _LOGGER.active else _DUMMY_LOGGER