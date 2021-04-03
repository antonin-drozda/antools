"""
POSTGRESQL SCHEMA CLASS

@ author: Antonín Drozda
@ organization: Freelancer
@ project: Anton's Tools
@ date: 28/03/2021

Class representing Postgre SQL Schema
"""

# %% FILE METADATA
__title__ = "POSTGRESQL SCHEMA CLASS"
__author__ = "Antonín Drozda"
__organization__ = "Freelancer"
__project__ = "Anton's Tools"
__date__ = "28/03/2021"

# %% LIBRARY IMPORT

# %% FILE IMPORT
from antools.logging import logger
from antools.shared import TypeValidator

# %% INPUTS

# %% CLASSES
class PostgreSQLSchema():
    
    def __init__(self, schema):
        self.schema = schema

# %% NOTES