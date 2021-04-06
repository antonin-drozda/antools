"""
DATABASES

@ author: Antonín Drozda
@ organization: Freelancer
@ project: Anton's Tools
@ date: 25/03/2021

"""

# %% FILE METADATA
__title__ = "DATABASES"
__author__ = "Antonín Drozda"
__organization__ = "Freelancer"
__project__ = "Anton's Tools"
__date__ = "25/03/2021"

# %% FILE IMPORT

# template(abstract)
from antools.database.abstract import SQLDatabase, SQLSchema, SQLTable

# postgres
from antools.database.postgres import PostgreSQLDatabase, PostgreSQLSchema, PostgreSQLTable
