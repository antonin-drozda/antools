"""
DATA TYPE VALIDATOR

@ author: Antonín Drozda
@ organization: Freelancer
@ project: Anton's Tools
@ date: 28/02/2021

Validator for various data types
"""

# %% FILE METADATA
__title__ = "DATA TYPE VALIDATOR"
__author__ = "Antonín Drozda"
__organization__ = "Freelancer"
__project__ = "Anton's Tools"
__date__ = "28/02/2021"

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
    


    def _report(self, cause:str = None, reason:bool = False) -> tuple or bool:
        valid = False if cause else True
        return (valid, cause) if reason else valid
    
    def _check_none(self, input):
        """ TO BE EXTENDED by np.nan, NULL etc. """
        return True if input == None else False 
            
 

# create instance of the class
TypeValidator = DataTypeValidator()
x = TypeValidator.str("null", reason=True, none_allowed=True, forbidden=["null"])
# %% INPUTS

# %% CLASSES

# class DataTypeValidator():
    
#     def __init__(self):
#         pass
    
#     def str(self, input):
#         logger.info("User performed some funtion.")
        

# class Borek():    
    
#     def validation_method(self):
#         Validator = DataTypeValidator()
#         Validator.str("X")
        
# x = Borek()
# x.validation_method()

# =============================================================================
# class DataTypeValidator:
#     r"""
#     DataTypeValidor class helping to validate various data types and its attributes
# 
#     ...
# 
#     Attributes
#     ----------
#     None
# 
#     Methods
#     -------
#     validate_str(self, user_input, min_len:int = None, max_len:int = None, only_ascii:bool = False) -> bool:
#         Check if type of user_input is string and on demand checks its length and if only first 128 ascii codes is used (no diacritics etc.)
#         
#     validate_int(self, user_input, min_value:int = None, max_value:int = None) -> bool:
#         Check if type of user_input is integer and on demand checks its value
# 
#     validate_float(self, user_input, min_value:int = None, max_value:int = None) -> bool:
#         Check if type of user_input is integer and on demand checks its value
# 
#     validate_complex(self, user_input) -> bool:
#         Check if type of user_input is complex number
#         
#     validate_bool(self, user_input) -> bool:
#         Check if type of user_input is boolean
#         
#     validate_bool(self, user_input) -> bool:
#         Check if type of user_input is boolean
#         
#     validate_list(self, user_input, min_len:int = None, max_len:int = None, no_duplicity:bool = False) -> bool:
#         Check if type of user_input is list and on demand check its length and fact is has no duplicities
#         
#     validate_set(self, user_input, min_len:int = None, max_len:int = None) -> bool:
#         Check if type of user_input is set and on demand check its length
#     
#     validate_dict(self, user_input, min_len:int = None, max_len:int = None, not_nested:bool = True) -> bool:
#         Check if type of user_input is dict and on demand check its length and fact is is not nested
#         
#     Raises
#     --------   
#     None
#         
#     Examples
#     --------   
#     None
#         
#     Notes
#     --------       
#     @ author:  Antonín Drozda (https://github.com/antonin-drozda)
#     @ created: 28/02/2021
#     
#     """    
#     
#     def __init__(self):
#         """
#         ...
#         
#         Parameters
#         ----------
#         None
#             
#         """
#         
#         pass
# 
# 
#     def validate_str(self, user_input, min_len:int = None, max_len:int = None, only_ascii:bool = False) -> bool:
#         """ Check if type of user_input is string and on demand checks its length and if only first 128 ascii codes is used (no diacritics etc.)          
#         
#         Parameters
#         ----------
#         user_input
#             Input which should be validated
#         min_len : int, optional
#             Minimum length of user_input (default None)
#         max_len : int, optional
#             Maximum length of user_input (default None)            
#         only_ascii : bool, optional
#             Set true for check that user_input is only in 128 ascii characters (default False) 
#         
#         Returns
#         ----------
#         Boolean if user_input is valid
#                 
#         Raises
#         ----------
#         None
#             
#         """        
#         if not isinstance (user_input, str):
#             return False
#         
#         if min_len:
#             if len(user_input) < min_len:
#                 return False
#             
#         if max_len:
#             if len(user_input) > max_len:
#                 return False
#             
#         if only_ascii:
#             if not all(ord(c) < 128 for c in user_input):
#                 return False
#             
#         return True 
# 
# 
#     def validate_int(self, user_input, min_value:int = None, max_value:int = None) -> bool:
#         """ Check if type of user_input is integer and on demand checks its value
#         
#         Parameters
#         ----------
#         user_input
#             Input which should be validated
#         min_value : int, optional
#             Minimum value of user_input (default None)
#         max_value : int, optional
#             Maximum value of user_input (default None)            
#         
#         Returns
#         ----------
#         Boolean if user_input is valid
#                 
#         Raises
#         ----------
#         None
#             
#         """        
#         if not isinstance (user_input, int):
#             return False
#         
#         if min_value:
#             if user_input < min_value:
#                 return False
#             
#         if max_value:
#             if user_input > max_value:
#                 return False
#          
#         return True
# 
# 
#     def validate_float(self, user_input, min_value:int = None, max_value:int = None) -> bool:
#         """ Check if type of user_input is integer and on demand checks its value          
#         
#         Parameters
#         ----------
#         user_input
#             Input which should be validated
#         min_value : int, optional
#             Minimum value of user_input (default None)
#         max_value : int, optional
#             Maximum value of user_input (default None)  
#         
#         Returns
#         ----------
#         Boolean if user_input is valid
#                 
#         Raises
#         ----------
#         None
#             
#         """          
#         if not isinstance (user_input, float) and not isinstance (user_input, int):
#             return False
#         
#         if min_value:
#             if user_input < min_value:
#                 return False
#             
#         if max_value:
#             if user_input > max_value:
#                 return False
#          
#         return True    
# 
# 
#     def validate_complex(self, user_input) -> bool:
#         """ Check if type of user_input is complex number  
#         
#         Parameters
#         ----------
#         user_input
#             Input which should be validated
#         
#         Returns
#         ----------
#         Boolean if user_input is valid
#                 
#         Raises
#         ----------
#         None
#             
#         """         
#         if not isinstance (user_input, complex):
#             return False
#         
#         return True
#        
#     
#     def validate_bool(self, user_input) -> bool:
#         """ Check if type of user_input is boolean 
#         
#         Parameters
#         ----------
#         user_input
#             Input which should be validated 
#         
#         Returns
#         ----------
#         Boolean if user_input is valid
#                 
#         Raises
#         ----------
#         None
#             
#         """ 
#         if not isinstance (user_input, bool):
#             return False    
#         
#         return True
# 
# 
#     def validate_list(self, user_input, min_len:int = None, max_len:int = None, no_duplicity:bool = False) -> bool:
#         """ Check if type of user_input is list and on demand check its length and fact is has no duplicities         
#         
#         Parameters
#         ----------
#         user_input
#             Input which should be validated
#         min_len : int, optional
#             Minimum length of user_input (default None)
#         max_len : int, optional
#             Maximum length of user_input (default None)            
#         no_duplicity : bool, optional
#             Set true for check that list has no duplicities
#         
#         Returns
#         ----------
#         Boolean if user_input is valid
#                 
#         Raises
#         ----------
#         None
#             
#         """ 
#         if not isinstance (user_input, list):
#             return False    
#         
#         if min_len:
#             if len(user_input) < min_len:
#                 return False
#             
#         if max_len:
#             if len(user_input) > max_len:
#                 return False            
#         
#         if no_duplicity:
#             if len(user_input) != len(set(user_input)):
#                 return False
#             
#         return True
# 
# 
#     def validate_set(self, user_input, min_len:int = None, max_len:int = None) -> bool:
#         """ Check if type of user_input is set and on demand check its length
#         
#         Parameters
#         ----------
#         user_input
#             Input which should be validated
#         min_len : int, optional
#             Minimum length of user_input (default None)
#         max_len : int, optional
#             Maximum length of user_input (default None)            
#         
#         Returns
#         ----------
#         Boolean if user_input is valid
#                 
#         Raises
#         ----------
#         None
#         
#         """
#             
#         if not isinstance (user_input, set):
#             return False    
#         
#         if min_len:
#             if len(user_input) < min_len:
#                 return False
#             
#         if max_len:
#             if len(user_input) > max_len:
#                 return False            
#             
#         return True
# 
# 
#     def validate_dict(self, user_input, min_len:int = None, max_len:int = None, not_nested:bool = True) -> bool:
#         """  Check if type of user_input is dict and on demand check its length and fact is is not nested
#         
#         Parameters
#         ----------
#         user_input
#             Input which should be validated
#         min_len : int, optional
#             Minimum length of user_input (default None)
#         max_len : int, optional
#             Maximum length of user_input (default None)            
#         no_duplicity : bool, optional
#             Set true for check that dictiory is not nested (default False)
#         
#         Returns
#         ----------
#         Boolean if user_input is valid
#                 
#         Raises
#         ----------
#         None
#         
#         """        
#         if not isinstance (user_input, dict):
#             return False    
#         
#         if min_len:
#             if len(user_input) < min_len:
#                 return False
#             
#         if max_len:
#             if len(user_input) > max_len:
#                 return False            
#         
#         if not_nested:
#             if any(isinstance(i,dict) for i in user_input.values()):
#                 return False
#             
#         return True   
#  
# =============================================================================
# create instance of the class

# %% NOTES
