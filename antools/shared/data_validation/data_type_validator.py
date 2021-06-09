# -*- coding: utf-8 -*-
"""
DATA TYPE VALIDATOR

Validator for various data types
"""

# %% LIBRARY IMPORT

# %% FILE IMPORT

class DataTypeValidator():
    """ Class used for handling various datatypes and known objects and user requirements on them 
    TO BE FINISHED """
    
    def __call__(self, input):
        """ Returns as same output as function type() """
        return type(input)
    
    def str(self, input, reason:bool = False,
            none_allowed:bool = False,
            exceptions:list = [],
            forbidden:list = [],
            max_len:int = None, 
            min_len:int = None,
            only_ascii:bool = None) -> tuple or bool:
        """ TO BE FINISHED """
        
        # check none
        return_none = self._check_none(input) if none_allowed else False
        if return_none:
            return self._report(reason=reason)
        
        # check exceptions
        if exceptions and isinstance(exceptions, list):
            if input in exceptions:
               return self._report(reason=reason)
                              
        # check forbidden
        if forbidden and isinstance(forbidden, list):
            if input in forbidden:
               return self._report("VALUE IS FORBIDDEN", reason=reason)
               
        # check length
        if isinstance(max_len, int):
            if len(input) > max_len and max_len > 0:
                return self._report(f"STRING IS TOO LONG ({len(input)}/{max_len})", reason=reason)
            
        if isinstance(min_len, int):
            if len(input) < min_len and min_len > 0:
                return self._report(f"STRING IS TOO SHORT ({len(input)}/{min_len})", reason=reason)
        
        # check ascii
        if only_ascii:
            if not all(ord(c) < 128 for c in input):
                return self._report("STRING CONTAINS NON ASCII CHARACTERS", reason=reason)
            
        return self._report("NOT A STRING", reason=reason) if not isinstance(input, str) else self._report(reason=reason)


    def int(self, input, reason:bool = False,
            none_allowed:bool = False,
            exceptions:list = [],
            forbidden:list = [],
            max_value:int = None, 
            min_value:int = None) -> tuple or bool:
        """ TO BE FINISHED """
        

            
        # check none
        return_none = self._check_none(input) if none_allowed else False
        if return_none:
            return self._report(reason=reason)
        
        # check exceptions
        if exceptions and type(exceptions) == list:
            if input in exceptions:
               return self._report(reason=reason)
                           
        # check forbidden
        if forbidden and type(forbidden) == list:
            if input in forbidden:
               return self._report("VALUE IS FORBIDDEN", reason=reason)
               
        # check length
        if isinstance(max_value, int):
            if input > max_value:
                return self._report(f"INTEGER IS TOO BIG ({input}>{max_value})", reason=reason)
            
        # check length
        if isinstance(min_value, int):
            if input < min_value:
                return self._report(f"INTEGER IS TOO SMALL ({input}<{min_value})", reason=reason)
        
        # special case to avoid booleans mix -> Python definition: isinstance(False, int) == True
        if isinstance(input, bool):
            return self._report("NOT AN INTEGER", reason=reason)
             
        return self._report("NOT AN INTEGER", reason=reason) if not isinstance(input, int) else self._report(reason=reason)    
    
    
    def bool(self, input, reason:bool = False, 
             none_allowed:bool = False):

        # check none
        return_none = self._check_none(input) if none_allowed else False
        if return_none:
            return self._report(reason=reason)
        
        return self._report("NOT A BOOLEAN", reason=reason) if not isinstance(input, int) else self._report(reason=reason)

    def _report(self, cause:str = None, reason:bool = False) -> tuple or bool:
        valid = False if cause else True
        return (valid, cause) if reason else valid
    
    def _check_none(self, input):
        """ TO BE EXTENDED by np.nan, NULL etc. """
        return True if input == None else False 

# %% CREATE INSTANCE
            
TypeValidator = DataTypeValidator()