# -*- coding: utf-8 -*-
"""
ABSTRACT TABLE CLASS

Class used for generating SQL queries for PostgreSQL Database Class
"""

# %% LIBRARY IMPORT
from abc import ABC, ABCMeta, abstractclassmethod

# %% FILE IMPORT
import pandas as pd

# %% INPUTS

# %% CLASSES
class SQLTable(ABC):
    """ Abstract class for SQLTable Type classes """
    __metaclass__ = ABCMeta
    
    @abstractclassmethod
    def __init__(self):
        pass
    
    @abstractclassmethod
    def __str__(self):
        pass
    
    @abstractclassmethod
    def __repr__(self):
        pass
    
    @abstractclassmethod            
    def create(self):
        pass
    
    @abstractclassmethod
    def select(self) -> pd.DataFrame:
        pass
    
    @abstractclassmethod
    def update(self) -> bool:
        pass
    
    @abstractclassmethod
    def delete(self) -> bool:
        pass
    
    @abstractclassmethod
    def save_dataframe(self, df, if_exists:str = "fail", err_raise:bool = True) -> bool:
        pass
 
      
# %% NOTES


