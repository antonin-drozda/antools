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

# %% FILE IMPORT
from antools.logging import logger
from antools.shared import TypeValidator
import pandas as pd
# %% INPUTS

# %% CLASSES
class PostgreSQLTable():
    """ Connector used for communication with PostgreSQL Table
    
    ...

    Attributes
    ----------
    table : str
        Name of the table
    schema : str or object
        Name of the schema
    database : str
        Instance of PostgreSQLDatabase Class if not only sql queries should be generated

    Methods
    -------
    _check_inputs(self)
        Check validity of class inputs
    create(self)
        NOT IMPLEMENTED YET
    select(self)
        NOT FINISHED YET
    update(self)
        NOT IMPLEMENTED YET
    save_dataframe(self)
        NOT IMPLEMENTED YET
    delete(self)
        NOT IMPLEMENTED YET
    info(self)
        NOT IMPLEMENTED YET
       
    Raises
    --------   
    ValueError
        If any inputs does not correspond to its intended data type.
    SystemExit
        TO BE FINISHED
        
    Examples
    --------   
    None
    
    Notes
    --------       
    @ author:  Antonín Drozda (https://github.com/antonin-drozda)
    @ created: 30/03/2021   
    
    """    
    
    def __init__(self, table, schema:str or object = None, database:object = None):
        self.table = table
        self.schema = schema
        self.database = database
        self._check_inputs()
        self.full_name = self.schema + "." + self.table if self.schema else self.table
    
    def _check_inputs(self):
        """Check validity of class inputs
        
        Parameters
        ----------
        None
        
        Raises
        ----------
        ValueError
            If any inputs does not correspond to its intended data type.
            
        """
        
        # check inputs from constructor
        valid, reason = TypeValidator.str(self.table, reason=True)
        None if valid else logger.wrong_input(self, "table", self.table, reason)    
        
        valid, reason = TypeValidator.str(self.schema, none_allowed=True, reason=True)
        if not valid:
            valid, reason = TypeValidator.object(self.schema, class_name="PostgreSQLSchema", reason=True)    
            self.schema = self.schema.schema if valid else logger.wrong_input(self, "schema", self.schema, "NOT AN <PostgreSQLSchema> OBJECT OR STRING")
        
        valid, reason = TypeValidator.object(self.database, class_name="PostgreSQLDatabase", reason=True)      
        self.database = None if not valid else self.database
        logger.warning(f"{self.__class__.__name__} was NOT initialized with valid conn to Database. It will generates only SQL queries!") if not self.database else None           
        
                
    def create(self):
        """ Creates table in Postgres Database or generates SQL query for it"""
        raise NotImplementedError("<{self.__class__.__name__}> cannot be created yet!")
    
    
    def select(self, columns:list or dict = {}, where:str = None) -> pd.DataFrame or str:
        """ Creates table in Postgres Database or generates SQL query for it
        
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
            logger.wrong_input(self, "columns", columns, "NOT READABLE VARIABLE FOR SQL SELECT COLUMNS QUERY")
        
        
        # where statement
        where = '' if not where else 'WHERE ' + where
        
        query = f'''SELECT {selected_columns} \nFROM {self.full_name}\n{where} ''' 
        self._reconnect()
        
        if self.database:
            try:
                df = self.database.load_dataframe(query)
                return df
            except Exception as err:
                logger.error(f"DataFrame could not be loaded from {self.full_name} due to: \n{err}")
        else:
            return query

        
    def update(self):
        """ Updates table in Postgres Database or generates SQL query for it"""
        raise NotImplementedError("<{self.__class__.__name__}> cannot be updated yet!")
    
    
    def save_dataframe(self, df, if_exists:str = "fail", err_raise:bool = True) -> bool:
        """ Saves Dataframe in Postgres Database or generates SQL query for it
        
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
        
        if not self.database:
            logger.error(f"DataFrame can't be saved because <{self.__class__.__name__}> has no valid database connection!")
            
        # check data
        valid, reason = TypeValidator.object(df, class_name="DataFrame", reason=True)
        None if valid else logger.wrong_input(self, "df", df, reason)

        None if if_exists in ["fail", "replace", "append"] else logger.wrong_input(self, "if_exists", if_exists, 'NOT IN AVAILABLE OPTIONS ["fail", "replace", "append"]')
        
        valid, reason = TypeValidator.bool(err_raise, reason=True)
        None if valid else logger.wrong_input(self, "err_raise", err_raise, reason)     
                
        self._reconnect()  

        try:
            df.to_sql(name=self.table, schema=self.schema, con=self.database._sqlalch_engine, if_exists=if_exists, method="multi")
            logger.info(f"DataFrame has been saved into {self.full_name} in {self.database} database!")            
            return True
            
        except Exception as err:
            logger.exception(f"Unfortunately, it was not possible to save the dataframe due to: \n{err}", terminate=err_raise)
            return False 
    
    def delete(self):
        """ Delete table in Postgres Database or generates SQL query for it"""
        raise NotImplementedError("<{self.__class__.__name__}> cannot be deleted yet!")
    
    def info(self):
        """ Get info of table in Postgres Database or generates SQL query for it"""
        raise NotImplementedError("<{self.__class__.__name__}> cannot get info yet!")

    def _reconnect(self):
         """ Reconnects to the database if available """
         self.database.connect() if self.database else None
        
# %% NOTES


