# -*- coding: utf-8 -*-
"""
ABSTRACT SCHEMA CLASS
"""

# %% LIBRARY IMPORT
from abc import ABC, ABCMeta, abstractclassmethod

# %% FILE IMPORT

# %% INPUTS

# %% CLASSES
class SQLSchema(ABC):
    """ Abstract class for SQLSchema Type classes """
    __metaclass__ = ABCMeta
    
    @abstractclassmethod
    def __init__(self):
        pass

# %% NOTES