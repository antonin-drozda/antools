"""
LOGGER METHODS

@ author: Antonín Drozda
@ organization: Freelancer
@ project: Anton's Tools
@ date: 20/04/2021

LOGGER METHODS.
"""

# %% FILE METADATA
__title__ = "LOGGER METHODS"
__author__ = "Antonín Drozda"
__organization__ = "Freelancer"
__project__ = "Anton's Tools"
__date__ = "20/04/2021"


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