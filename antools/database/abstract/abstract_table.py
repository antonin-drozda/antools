"""
ABSTRACT TABLE CLASS

@ author: Antonín Drozda
@ organization: Freelancer
@ project: Anton's Tools
@ date: 06/04/2021

Class used for generating SQL queries for PostgreSQL Database Class
"""

# %% FILE METADATA
__title__ = "ABSTRACT TABLE CLASS"
__author__ = "Antonín Drozda"
__organization__ = "Freelancer"
__project__ = "Anton's Tools"
__date__ = "06/04/2021"

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


