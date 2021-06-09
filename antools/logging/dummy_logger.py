# -*- coding: utf-8 -*-
"""
DUMMY LOGGER
"""

# %% LIBRARY IMPORT

# %% FILE IMPORT
from antools.logging.abstract_logger import AbstractLogger

# %% CLASSES
class _DummyLogger(AbstractLogger):
    """ Class which represents Logger when user does not want to use it """
       
    def __init__(self):
        self.name = "DummyLogger"
  
    def debug(self, msg:str):
        pass

    def info(self, msg:str):
        pass
        
    def warning(self, msg:str):
        pass
    
    def critical(self, msg:str):
        pass     
                       
    def error(self, msg:str, terminate:bool = True):
        if terminate:
            raise SystemExit(msg)

    def exception(self, msg:str, add_info:bool = False, terminate:bool = False):
        if terminate:
            raise SystemExit(msg)
            
    def wrong_input(self, call_object:object, var_name:"str", var_value, reason:str) -> ValueError:
        object_name = call_object.__class__.__name__ if isinstance(call_object, object) else object
        msg = f"{object_name} obtained invalid parameter <{var_name}> = <{var_value}>. IT IS {reason}!"
        raise ValueError(msg)   



# %% CREATE INSTANCE         
_DUMMY_LOGGER = _DummyLogger()