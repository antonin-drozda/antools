"""
DATA TYPE VALIDATOR

@ author: Antonín Drozda
@ organization: Freelancer
@ project: Anton's Tools
@ date: 28/02/2021

Base Logger for Windows OS
"""

# %% FILE METADATA
__title__ = "DATA TYPE VALIDATOR"
__author__ = "Antonín Drozda"
__organization__ = "Freelancer"
__project__ = "Anton's Tools"
__date__ = "28/02/2021"

# %% LIBRARY IMPORT

# %% FILE IMPORT

# %% INPUTS

# %% CLASSES

# !!! DRAFT

class DataTypeValidator:
    r"""
    DataTypeValidor class helping to validate various data types and its attributes

    ...

    Attributes
    ----------
    None

    Methods
    -------
    validate_str(self, user_input, min_len:int = None, max_len:int = None, only_ascii:bool = False) -> bool:
        Validate string and on demand checks its length and if only first 128 ascii codes is used (no diacritics etc.)
        
    validate_int(self, user_input, min_value:int = None, max_value:int = None) -> bool:
        Validate integer and on demand checks its value

    validate_float(self, user_input, min_value:int = None, max_value:int = None) -> bool:
        TO BE CONTINUED ...
       
    Raises
    --------   
    None
        
    Examples
    --------   
    None
        
    Notes
    --------       
    @ author:  Antonín Drozda (https://github.com/antonin-drozda)
    @ created: 28/02/2021
    
    """    
    def __init__(self):
        pass


    def validate_str(self, user_input, min_len:int = None, max_len:int = None, only_ascii:bool = False) -> bool:
        
        if not isinstance (user_input, str):
            return False
        
        if min_len:
            if len(user_input) < min_len:
                return False
            
        if max_len:
            if len(user_input) > max_len:
                return False
            
        if only_ascii:
            if not all(ord(c) < 128 for c in user_input):
                return False
            
        return True 


    def validate_int(self, user_input, min_value:int = None, max_value:int = None) -> bool:
        
        if not isinstance (user_input, int):
            return False
        
        if min_value:
            if user_input < min_value:
                return False
            
        if max_value:
            if user_input > max_value:
                return False
         
        return True


    def validate_float(self, user_input, min_value:int = None, max_value:int = None) -> bool:
        
        if not isinstance (user_input, float) and not isinstance (user_input, int):
            return False
        
        if min_value:
            if user_input < min_value:
                return False
            
        if max_value:
            if user_input > max_value:
                return False
         
        return True    

    def validate_complex(self, user_input) -> bool:
        
        if not isinstance (user_input, complex):
            return False
        
        return True
        
    def validate_bool(self, user_input) -> bool:
        if not isinstance (user_input, bool):
            return False    
        
        return True

    def validate_list(self, user_input, min_len:int = None, max_len:int = None, no_duplicity:bool = False) -> bool:
        if not isinstance (user_input, list):
            return False    
        
        if min_len:
            if len(user_input) < min_len:
                return False
            
        if max_len:
            if len(user_input) > max_len:
                return False            
        
        if no_duplicity:
            if len(user_input) != len(set(user_input)):
                return False
            
        return True

    def validate_set(self, user_input, min_len:int = None, max_len:int = None) -> bool:
        if not isinstance (user_input, set):
            return False    
        
        if min_len:
            if len(user_input) < min_len:
                return False
            
        if max_len:
            if len(user_input) > max_len:
                return False            
            
        return True

    def validate_dict(self, user_input, min_len:int = None, max_len:int = None, not_nested:bool = True) -> bool:
        
        if not isinstance (user_input, dict):
            return False    
        
        if min_len:
            if len(user_input) < min_len:
                return False
            
        if max_len:
            if len(user_input) > max_len:
                return False            
        
        if not_nested:
            if any(isinstance(i,dict) for i in user_input.values()):
                return False
            
        return True   
    
# %% NOTES
