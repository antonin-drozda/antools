"""
ABSTRACT SCHEMA CLASS

@ author: Antonín Drozda
@ organization: Freelancer
@ project: Anton's Tools
@ date: 06/04/2021

Class representing Postgre SQL Schema
"""

# %% FILE METADATA
__title__ = "ABSTRACT SCHEMA CLASS"
__author__ = "Antonín Drozda"
__organization__ = "Freelancer"
__project__ = "Anton's Tools"
__date__ = "06/04/2021"

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