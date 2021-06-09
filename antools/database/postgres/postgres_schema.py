# -*- coding: utf-8 -*-
"""
POSTGRESQL SCHEMA CLASS

Class representing Postgre SQL Schema
"""

# %% LIBRARY IMPORT

# %% FILE IMPORT
from antools.logging import get_logger
from antools.shared import TypeValidator
from antools.database import SQLSchema

# %% CLASSES
class PostgreSQLSchema(SQLSchema):
    
    def __init__(self, schema):
        self.schema = schema

# %% NOTES