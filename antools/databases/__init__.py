"""
DATABASES

@ author: Antonín Drozda
@ organization: Freelancer
@ project: Anton's Tools
@ date: 27/02/2021

"""

# %% FILE METADATA
__title__ = "DATABASES"
__author__ = "Antonín Drozda"
__organization__ = "Freelancer"
__project__ = "Anton's Tools"
__date__ = "27/02/2021"

# %% IMPORT FILES
import os
import sys

antools_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not antools_folder in sys.path:
    sys.path.append(antools_folder)

# %% FILES IMPORT   
from databases.postgres.postgres_connector import PostgreSQLConnector