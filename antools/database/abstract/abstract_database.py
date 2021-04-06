"""
ABSTRACT DATABASE CLASS

@ author: Antonín Drozda
@ organization: Freelancer
@ project: Anton's Tools
@ date: 06/04/2021

Connector used for communicating with PostgreSQL database.
"""

# %% FILE METADATA
__title__ = "ABSTRACT DATABASE CLASS"
__author__ = "Antonín Drozda"
__organization__ = "Freelancer"
__project__ = "Anton's Tools"
__date__ = "06/04/2021"

# %% LIBRARY IMPORT
from abc import ABC, ABCMeta, abstractclassmethod
import pandas as pd

# %% FILE IMPORT

# %% INPUTS

# %% CLASSES

class SQLDatabase(ABC):
    """ Abstract class for SQLDatabase Type classes """
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
    def connect(self) -> bool:  
        pass

    @abstractclassmethod           
    def disconnect(self) -> bool:  
        pass
    
    @abstractclassmethod
    def execute_query(self, query:str, err_raise:bool = True) -> bool:
        pass
    
    @abstractclassmethod
    def load_dataframe(self, query:str, err_raise:bool = True) -> pd.DataFrame:
        pass
    
    @abstractclassmethod   
    def save_dataframe(self, df:pd.DataFrame, table:str, schema:str = None, if_exists:str = "fail", err_raise:bool = True) -> bool:
        pass
        
# %% NOTES
