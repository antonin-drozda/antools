# -*- coding: utf-8 -*-
"""
VARVALIDATOR CLASS
"""

from decimal import Decimal
from antools.logging import get_logger

class VariableValidator():
    """ Class used for handling various datatypes and known objects and user requirements on them """
    
    _log = get_logger(_activate=False)

    def __call__(self, value):
        return type(value)

    # TEXT TYPES
    def str(self, value:str, terminate:bool = False, max_len:int = None, min_len:int = None, 
            forbidden:list = None, allowed:list or dict = None, starts_with:str = None, ends_with:str = None,
            lower_only:bool = False, upper_only:bool = False,
            capital_only:bool = False, none_allowed:bool = False,
            only_ascii:bool = True) -> bool:

        forbidden = [] if forbidden is None else forbidden
        allowed = [] if allowed is None else allowed
        mistakes = []

        result = self._check_none_and_type(value, str, none_allowed, terminate)
        if not result == "CONTINUE":
            return result

        if max_len:
            if len(value) > max_len:
                mistakes.append(f"Value is too long (maximum {max_len}")

        if min_len:
            if len(value) < min_len:
                mistakes.append(f"Value is too short (minimum {min_len}")

        if value in forbidden:
            mistakes.append(f"Value found in forbidden words!")

        if allowed:
            if value not in allowed:
                mistakes.append(f"Value not found in allowed options!")

        if starts_with and not value.startswith(starts_with):
            mistakes.append(f"Value does not starts with {starts_with}")

        if ends_with and not value.endswith(ends_with):
            mistakes.append(f"Value does not ends with {ends_with}")

        if lower_only and not value.lower() == value:
            mistakes.append(f"Value does not contain only lower characters")

        if upper_only and not value.upper() == value:
            mistakes.append(f"Value does not contain only upper characters")

        if capital_only and not value.lower().capitalize() == value:
            mistakes.append(f"Value does not contain only capitalize characters")

        if only_ascii and not all(ord(c) < 128 for c in value):
            mistakes.append(f"Value does not contain only ASCII characters")

        return self._report_mistakes(value, terminate, mistakes)


    # NUMERIC TYPES
    def int(self, value:int, terminate:bool = False, max:int = None, min:int = None,
            none_allowed:bool = False, bool_allowed:bool = False, divisible_by:list = None, prime:bool = None) -> bool:

        mistakes = []
        
        # special case in Python -> isinstance(False, int) == True
        if value in [0, 1] and not bool_allowed:
            msg = f"Variable: <{value}>, type {type(value)} check failed due to: <Boolean values are not allowed>!"
            self._log.error(msg, ValueError) if terminate else self._log.debug(msg)
            return False

        result = self._check_none_and_type(value, int, none_allowed, terminate)
        if not result == "CONTINUE":
            return result

        if max:
            mistakes.append(f"Value is big (maximum {max}") if value > max else None

        if min:
            mistakes.append(f"Value is low (minimum {max}") if value < min else None

        if divisible_by:
            for num in divisible_by:
                if not value % num == 0:
                    mistakes.append(f"Value is not divisible by {num}")
                    break

        if prime:
            if not value == 1:
                for num in range(2, int(value/2)+1):
                    if value % num == 0:
                        mistakes.append(f"Value is not prime number because it is divisble by {num}")
                        break
            else:
                mistakes.append(f"One is not a prime number")

        return self._report_mistakes(value, terminate, mistakes)


    def float(self, value:float, terminate:bool = False, int_allowed:bool = True, max:int = None, min:int = None,
            none_allowed:bool = False, divisible_by:list = None) -> bool:

        mistakes = []

        var_type = [float, int] if int_allowed else [float]
        result = self._check_none_and_type(value, var_type, none_allowed, terminate)

        if not result == "CONTINUE":
                return result
        if max:
            mistakes.append(f"Value is big (maximum {max}") if value > max else None

        if min:
            mistakes.append(f"Value is low (minimum {max}") if value < min else None

        if divisible_by:
            value = Decimal(str(value))
            for num in divisible_by:
                num = Decimal(str(num))
                if not value % num == 0:
                    mistakes.append(f"Value is not divisible by {num}")
                    break

        return self._report_mistakes(value, terminate, mistakes)


    def complex(self, value:complex, terminate:bool = False, none_allowed:bool = False):
        result = self._check_none_and_type(value, complex, none_allowed, terminate)

        if not result == "CONTINUE":
            return result

        return self._report_mistakes(value, terminate, mistakes=[])


    # SEQUENCE TYPES
    def list(self, value:list, terminate:bool = False, max_len:int = None, min_len:int = None,
            none_allowed:bool = False, forbidden:list = None, allowed:list = None) -> bool:

        forbidden = [] if forbidden is None else forbidden
        mistakes = []

        result = self._check_none_and_type(value, list, none_allowed, terminate)
        if not result == "CONTINUE":
            return result

        if max_len:
            mistakes.append(f"List is too long (maximum {max_len}") if len(value) > max_len else None

        if min_len:
            mistakes.append(f"List is too short (minimum {max_len}") if len(value) < min_len else None
   
        if forbidden:
            for item in value:
                if item in forbidden:
                    mistakes.append(f"List contains forbidden value: {item}")
                    break

        if allowed:
            for item in value:
                if item not in allowed:
                    mistakes.append(f"Value in checked list not found in allowed words!")
                    break

        return self._report_mistakes(value, terminate, mistakes)


    def tuple(self, value:tuple, terminate:bool = False, max_len:int = None, min_len:int = None,
            none_allowed:bool = False, forbidden:list = None, allowed:list = None) -> bool:

        forbidden = [] if forbidden is None else forbidden
        mistakes = []

        result = self._check_none_and_type(value, tuple, none_allowed, terminate)
        if not result == "CONTINUE":
            return result

        if max_len:
            mistakes.append(f"Tuple is too long (maximum {max_len}") if len(value) > max_len else None

        if min_len:
            mistakes.append(f"Tuple is too short (minimum {max_len}") if len(value) < min_len else None

        
        if forbidden:
            for item in value:
                if item in forbidden:
                    mistakes.append(f"Tuple contains forbidden value: {item}")
                    break

        if allowed:
            for item in value:
                if item not in allowed:
                    mistakes.append(f"Value in checked tuple not found in allowed words!")
                    break

        return self._report_mistakes(value, terminate, mistakes)


    def range(self, value:range, terminate:bool = False, none_allowed:bool = False):

        result = self._check_none_and_type(value, range, none_allowed, terminate)
        if not result == "CONTINUE":
            return result

        return self._report_mistakes(value, terminate, mistakes=[])


    # MAPPING TYPES
    def dict(self, value:dict, terminate:bool = False, max_len:int = None, min_len:int = None,
            none_allowed:bool = False, forbidden_keys:list = None, forbidden_values:list = None) -> bool:


        forbidden_keys = [] if forbidden_keys is None else forbidden_keys
        forbidden_values = [] if forbidden_values is None else forbidden_values
        mistakes = []

        result = self._check_none_and_type(value, dict, none_allowed, terminate)
        if not result == "CONTINUE":
            return result

        if max_len:
            mistakes.append(f"Dictionary is too long (maximum {max_len}") if len(value) > max_len else None

        if min_len:
            mistakes.append(f"Dictionary is too short (minimum {max_len}") if len(value) < min_len else None

        
        for key, key_value in value.items():
            mistakes.append(f"Found forbidden key <{key}>") if key in forbidden_keys else None
            mistakes.append(f"Found forbidden value <{key}>") if key_value in forbidden_values else None

        return self._report_mistakes(value, terminate, mistakes)


    # SET TYPES
    def set(self, value:set, terminate:bool = False, max_len:int = None, min_len:int = None,
            none_allowed:bool = False, forbidden:list = None, allowed:list = None) -> bool:

        forbidden = [] if forbidden is None else forbidden
        mistakes = []

        result = self._check_none_and_type(value, set, none_allowed, terminate)
        if not result == "CONTINUE":
            return result

        if max_len:
            mistakes.append(f"Set is too long (maximum {max_len}") if len(value) > max_len else None

        if min_len:
            mistakes.append(f"Set is too short (minimum {max_len}") if len(value) < min_len else None

        
        if forbidden:
            for item in value:
                if item in forbidden:
                    mistakes.append(f"Set contains forbidden value: {item}")
                    break

        if allowed:
            for item in value:
                if item not in allowed:
                    mistakes.append(f"Value in checked set not found in allowed words!")
                    break

        return self._report_mistakes(value, terminate, mistakes)


    def frozenset(self, value:frozenset, terminate:bool = False, max_len:int = None, min_len:int = None,
        none_allowed:bool = False, forbidden:list = None, allowed:list = None) -> bool:

        forbidden = [] if forbidden is None else forbidden
        mistakes = []

        result = self._check_none_and_type(value, frozenset, none_allowed, terminate)
        if not result == "CONTINUE":
            return result

        if max_len:
            mistakes.append(f"Frozenset is too long (maximum {max_len}") if len(value) > max_len else None

        if min_len:
            mistakes.append(f"Frozenset is too short (minimum {max_len}") if len(value) < min_len else None

        if forbidden:
            for item in value:
                if item in forbidden:
                    mistakes.append(f"Frozenset contains forbidden value: {item}")
                    break
        if allowed:
            for item in value:
                if item not in allowed:
                    mistakes.append(f"Value in checked frozenset not found in allowed words!")
                    break

        return self._report_mistakes(value, terminate, mistakes)


    # BOOLEAN TYPE
    def bool(self, value:bool, terminate:bool = False, none_allowed:bool = False) -> bool:

        result = self._check_none_and_type(value, bool, none_allowed, terminate)
        if not result == "CONTINUE":
            return result
        
        return self._report_mistakes(value, terminate, mistakes=[])


    # BINARY TYPES
    def bytes(self):
        self._log.error("This method is not implemented yet!", NotImplementedError)

    def bytearray(self):
        self._log.error("This method is not implemented yet!", NotImplementedError)

    def memoryview(self):
        self._log.error("This method is not implemented yet!", NotImplementedError)

    # SPECIAL TYPES
    def class_check(self):
        self._log.error("This method is not implemented yet!", NotImplementedError)

    def func(self):
        self._log.error("This method is not implemented yet!", NotImplementedError)
    
    def error(self):
        self._log.error("This method is not implemented yet!", NotImplementedError)

    
    # PANDAS TYPES
    def pd_DataFrame(self):
        self._log.error("This method is not implemented yet!", NotImplementedError)

    def pd_Series(self):
        self._log.error("This method is not implemented yet!", NotImplementedError)


    # NUMPY TYPES
    def np_array(self):
        self._log.error("This method is not implemented yet!", NotImplementedError)


    def _check_none_and_type(self, value, var_type, none_allowed:bool, terminate:bool):
            
        if value is None:
            if not none_allowed:
                msg=f"Value is None but should be {var_type} instead!"
                self._log.error(msg, ValueError) if terminate else self._log.debug(msg)
                return False
            else:
                return True

        var_type = [var_type] if not isinstance(var_type, list) else var_type
        type_found = False
        for item in var_type:
            if isinstance(value, item):
                type_found = True
                break

        if not type_found:
            msg = f"Input <{value}> is not in allowed types: {var_type}! Its type is: {type(value)}!"
            self._log.error(msg, ValueError) if terminate else self._log.debug(msg)
            return False

        return "CONTINUE"


    def _report_mistakes(self, value, terminate, mistakes) -> bool:

        if mistakes:
            msg = f"Variable: <{value}>, type {type(value)} check failed due to: <{list(mistakes)}>!"
            self._log.error(msg, ValueError) if terminate else self._log.debug(msg)
            return False
        else:
            return True


VarValidator = VariableValidator()