"""
POSTGRESQL TABLE CLASS

@ author: Antonín Drozda
@ organization: Freelancer
@ project: Anton's Tools
@ date: 28/03/2021

Class used for generating SQL queries for PostgreSQL Database Class
"""

# %% FILE METADATA
__title__ = "POSTGRESQL TABLE CLASS"
__author__ = "Antonín Drozda"
__organization__ = "Freelancer"
__project__ = "Anton's Tools"
__date__ = "28/03/2021"

# %% LIBRARY IMPORT
import pandas as pd

# %% FILE IMPORT
from antools.logging import get_logger
from antools.database import SQLTable
from antools.shared import TypeValidator

# %% INPUTS

# %% CLASSES
class PostgreSQLTable(SQLTable):
    """ Connector used for communication with PostgreSQLTable
    
    ...

    Attributes
    ----------
    _table : str
        Name of the table
    _schema : str or object
        Name of the schema
    _database : object
        Instance of PostgreSQLDatabase Class if not only sql queries should be generated
    _full_name : str
        Combination of _schema._table

    Methods
    -------
    create(self)
        NOT IMPLEMENTED YET
    select(self)
        IN PROCESS
    update(self)
        NOT IMPLEMENTED YET
    delete(self)
        NOT IMPLEMENTED YET
    save_dataframe(self)
        NOT IMPLEMENTED YET
    info(self)
        Returns detailed info about the table
       
    Raises
    --------   
    ValueError
        If any inputs does not correspond to its intended data type.
    SystemExit
        IN PROCESS
        
    Examples
    --------   
    None
    
    Notes
    --------       
    @ author:  Antonín Drozda (https://github.com/antonin-drozda)
    @ created: 30/03/2021   
    
    """    
    
    def __init__(self, table, schema:str or object = None, database:object = None):
        self._table = table
        self._schema = schema
        self._database = database
        
        self._logger = get_logger()
        # check table
        valid, reason = TypeValidator.str(self._table, reason=True)
        None if valid else self._logger.wrong_input(self, "table", self._table, reason)    
        
        # check schema
        valid, reason = TypeValidator.str(self._schema, none_allowed=True, reason=True)
        if not valid:
            valid, reason = TypeValidator.object(self._schema, class_name="PostgreSQLSchema", reason=True)    
            self._schema = self._schema.schema if valid else self._logger.wrong_input(self, "schema", self._schema, "NOT AN <PostgreSQLSchema> OBJECT OR STRING")
        
        # check database
        valid, reason = TypeValidator.object(self._database, class_name="PostgreSQLDatabase", reason=True)
        None if valid else self._logger.wrong_input(self, "database", self._database, reason)
        
        self._full_name = self._schema + "." + self._table if self._schema else self._table
        

    def __str__(self):   
        return f"{self._full_name}"
    
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name={self._full_name}, database={self._database._database})"
    
    
    def create(self):
        """ Creates table in PostgreSQLDatabase"""
        raise NotImplementedError("<{self.__class__.__name__}> cannot be created yet!")
    
    
    def select(self, columns:list or dict = {}, where:str = None) -> pd.DataFrame:
        """ Creates table in PostgreSQLDatabase
        
        Parameters
        ----------
        columns : list or dict
            List of columns or dict of columns (key - dtb name, value intended name) of columns to be selected), default {}
        where : bool, optional
            String representing 'WHERE string' part in SQL query
            
        Returns
        ----------
        DataFrame
        
        Raises
        ----------
        SystemExit
            If dataframe could not be loaded or sql query is not valid 
            
        """
                
        # select columns
        if not columns:
            selected_columns = '*' if not columns else ''

        elif isinstance(columns, list):
            selected_columns = ', '.join(str(e) for e in columns)
        
        elif isinstance(columns, dict):
            selected_columns = ''
            for key, value in columns.items():
                splitter = ', ' if (list(columns))[-1] != key else ''
                selected_columns += key + ' AS ' + value + splitter
        else:
            self._logger.wrong_input(self, "columns", columns, "NOT READABLE VARIABLE FOR SQL SELECT COLUMNS QUERY")
        
        
        # where statement
        where = '' if not where else 'WHERE ' + where
        
        query = f'''SELECT {selected_columns} \nFROM {self._full_name}\n{where} ''' 
        self._reconnect()
        
        try:
            return self._database.load_dataframe(query)            
        except Exception as err:
            self._logger.error(f"DataFrame could not be loaded from {self._full_name} due to: \n{err}")

        
    def update(self):
        """ Updates table in PostgreSQLDatabase"""
        raise NotImplementedError("<{self.__class__.__name__}> cannot be updated yet!")
    
    
    def save_dataframe(self, df, if_exists:str = "fail", err_raise:bool = True) -> bool:
        """ Saves Dataframe in PostgreSQLDatabase
        
        Parameters
        ----------
        df : pd.DataFrame
            DataFrame which should be saved in the database  
        if_exists : str, optional
            What should happen if table exists (options fail, append, replace [default fail])
            Fail - it won' t do anything
            Append - it will append rows at the end
            Replace - it will delete previous data and load new
        err_raise : bool, optional
            Raise SystemExit if DataFrame could not be saved (default True)
            
        Returns
        ----------
        Boolean value if DataFrame was saved or not
        
        Raises
        ----------
        SystemExit
            If err_raise == True and DataFrame was not saved
            If connection to the Database is not valid
            If DataFrame has different format than the table
            
        ValueError
            If if_exists == fail and table already exists
        """
                    
        # check data
        valid, reason = TypeValidator.object(df, class_name="DataFrame", reason=True)
        None if valid else self._logger.wrong_input(self, "df", df, reason)

        None if if_exists in ["fail", "replace", "append"] else self._logger.wrong_input(self, "if_exists", if_exists, 'NOT IN AVAILABLE OPTIONS ["fail", "replace", "append"]')
        
        valid, reason = TypeValidator.bool(err_raise, reason=True)
        None if valid else self._logger.wrong_input(self, "err_raise", err_raise, reason)     
                
        self._reconnect()  

        try:
            df.to_sql(name=self._table, schema=self._schema, con=self._database._sqlalch_engine, if_exists=if_exists, method="multi")
            self._logger.info(f"DataFrame has been saved into {self._full_name} in {self._database} database!")            
            return True
            
        except Exception as err:
            self._logger.exception(f"Unfortunately, it was not possible to save the dataframe due to: \n{err}", terminate=err_raise)
            return False 
    
    
    def delete(self):
        """ Delete table in PostgreSQLDatabase"""
        raise NotImplementedError("<{self.__class__.__name__}> cannot be deleted yet!")


    def info(self) -> dict:
        """ Returns detailed info about PostgreSQLTable """
        
        self._reconnect()
        sql_info = self._database.load_dataframe(f""" SELECT *
                                               FROM 
                                                   information_schema.columns
                                               WHERE 
                                                   table_name = '{self._table}'
                                               AND table_schema = '{self._schema}';""")
   
        
        no_rows = self._database.load_dataframe(f""" SELECT COUNT(*) FROM {self._full_name}; """).iloc[0][0]
                                           
        return {"database": self._database._database,
                "schema": self._schema,
                "name": self._table,
                "rows_no": no_rows,
                "columns": sql_info[["column_name", "data_type"]].set_index("column_name").to_dict()["data_type"],
                "full info": sql_info}
    
        
    def _reconnect(self):
         """ Reconnects to the PostgreSQLDatabase"""
         self._database.connect()
        
# %% NOTES


