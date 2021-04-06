"""
POSTGRESQL DATABASE CLASS

@ author: Antonín Drozda
@ organization: Freelancer
@ project: Anton's Tools
@ date: 25/03/2021

Connector used for communicating with PostgreSQL database.
"""

# %% FILE METADATA
__title__ = "POSTGRESQL DATABASE CLASS"
__author__ = "Antonín Drozda"
__organization__ = "Freelancer"
__project__ = "Anton's Tools"
__date__ = "25/03/2021"

# %% LIBRARY IMPORT
import psycopg2
import pandas as pd
import time
from sqlalchemy import create_engine 

# %% FILE IMPORT
from antools.logging import logger
from antools.database import SQLDatabase
from antools.shared import TypeValidator

# %% INPUTS

# %% CLASSES
class PostgreSQLDatabase(SQLDatabase):
    """ Connector used for communication with PostgreSQL database
    
    ...

    Attributes
    ----------
    _database : str
        Name of the database
    _user : str
        Name of the user
    _password : str
        Password for database connection
    _server : str
        Server name (default 'localhost')
    _port : str or int
        Port for connection
    _database_type:
        Holds information of type of SQL database
    _is_connected : bool
        Boolean value storing info about PostgreSQLDatabase connection
    _conn_PSYCOPG : class
        Connection using <psycopg2> library
    _conn_SQLALCH : class
        Connection using <sqlalchemy> library        
    _cursor_PSYCOPG : class
        Cursor used for executing queries


    Methods
    -------
    connect(self) -> bool
        Connects to the database
    _connect_with_PSYCOPG(self)
        Connects to the database using psycopg2 library (part of connect funtion)
    _connect_with_SQLALCH(self)
        Connects to the database using sqlalchemy library (part of connect funtion)    
    disconnect(self) -> bool
        Disconnects from the database
    execute_query(self, query:str, err_raise:bool = True) -> bool
        Executes query in the database
    load_dataframe(self, query:str, err_raise:bool = True) -> pd.DataFrame
        Returns pd.DataFrame based on query execution       
    save_dataframe(self, df:pd.DataFrame, db_table:str, db_schema:str = None, if_exists:str = "fail", err_raise:bool = True) -> bool
        Saves pd.DataFrame in the database          
       
    Raises
    --------   
    ValueError
        If any inputs does not correspond to its intended data type.
    SystemExit
        When connection to the database is not possible
        When execute_query, load_dataframe or save_dataframe method was not executed and err_raise == True
        
    Examples
    --------   
    None
    
    Notes
    --------       
    @ author:  Antonín Drozda (https://github.com/antonin-drozda)
    @ created: 25/03/2021   
    
    """
    
    _database_type = 'postgres'
    _is_connected = False
    _connection_time = 0
    
    def __init__(self, database:str, user:str, password:str,
                     server:str = 'localhost', port:str or int = 5432):
        
        self._database = database
        self._user = user
        self._password = password
        self._server = server
        self._port = port

        # check inputs
        valid, reason = TypeValidator.str(self._database, reason=True)
        None if valid else logger.wrong_input(self, "database", self._database, reason) 
        
        valid, reason = TypeValidator.str(self._user, reason=True)
        None if valid else logger.wrong_input(self, "user", self._user, reason)            

        valid, reason = TypeValidator.str(self._password, reason=True)
        None if valid else logger.wrong_input(self, "password", "XXX", reason) 
        
        valid, reason = TypeValidator.str(self._server, reason=True)
        None if valid else logger.wrong_input(self, "server", self._server, reason) 

        # check if port is can be integer
        try:
            self._port = int(self._port)
        except ValueError:
            valid, reason = TypeValidator.int(self._port, reason=True)
            None if valid else logger.wrong_input(self, "port", self._port, reason)
        
        # automatically connect during initialization
        self.connect()
    
    
    def __str__(self):
        return f"{self.__class__.__name__}({self._database}, {self._server}, connected={self._is_connected})"
    
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self._database}, {self._server}, connected={self._is_connected})"
                
    
    def connect(self) -> bool:  
        """ Connects to the database          
        
        Parameters
        ----------
        None
        
        Returns
        ----------
        Boolean value of connection status
                
        Raises
        ----------
        SystemExit
            If it was not possible to connect with psycopg2 or sqlalchemy library
            
        """
        
        # reconnect if not connected or 120 seconds from last connection
        if not self._is_connected or (time.time() - self._connection_time) > 120:
            self._conn_PSYCOPG = self._connect_with_PSYCOPG()
            self._conn_SQLACH = self._connect_with_SQLALCH()  
            self._is_connected = True if self._conn_PSYCOPG and self._conn_SQLACH else False

            if self._is_connected:
                self._connection_time = time.time()
                logger.debug(f"{self.__class__.__name__} Connection to the <{self._database}> database was sucessful!")
            else:
                logger.error(f"{self.__class__.__name__} Connection to the <{self._database}> database was not sucessful!")

        return self._is_connected


    def _connect_with_PSYCOPG(self):
        """ Connects to the database using psycopg2 library         
        
        Parameters
        ----------
        None

        Returns
        ----------
        Connection with database using psycopg2 library     
          
        Raises
        ----------
        SystemExit
            If it was not possible to connect
        """
        try:
            self.conn_PSYCOPG = psycopg2.connect(host=self._server, 
                                        port=self._port, 
                                        database=self._database,
                                        user=self._user,
                                        password=self._password)
               
            self.conn_PSYCOPG.autocommit = True
            self.cursor_PSYCOPG = self.conn_PSYCOPG.cursor()  
            return self.conn_PSYCOPG
            
        except Exception:
            self._is_connected = False
            self.conn_PSYCOPG = None
            logger.exception(f"{self.__class__.__name__} Connection to the <{self._database}> database was not sucessful!", terminate=True)      

    
    def _connect_with_SQLALCH(self):
        """ Connects to the database using sqlalchemy library         
        
        Parameters
        ----------
        None

        Returns
        ----------
        Connection with database using sqlalchemy library     
          
        Raises
        ----------
        SystemExit
            If it was not possible to connect
        """
        try:
            self._sqlalch_engine = create_engine(f"postgresql://{self._user}:{self._password}@{self._server}:{self._port}/{self._database}",
                                    connect_args={'connect_timeout': 3})
            self.conn_SQLALCH = self._sqlalch_engine.connect()
            return self.conn_SQLALCH
            
        except Exception:
            self._is_connected = False
            self.conn_SQLALCH = None
            logger.exception(f"{self.__class__.__name__} Connection to the <{self._database}> database was not sucessful!", terminate=True)      

            
    def disconnect(self):
        """Disconnects from the database        
        
        Parameters
        ----------
        None
        
        Returns
        ----------
        Boolean value of connection status

        """
        if self._is_connected:
            self.conn_PSYCOPG.close()
            self.conn_SQLALCH.close()
            self._is_connected = False
            logger.debug(f"<{self._database}> database was disconnected!")
            
        return self._is_connected

            
    def execute_query(self, query:str, err_raise:bool = True) -> bool:
        """ Executes query in the database 
        
        Parameters
        ----------
        query : str
            SQL query which should be performed
        err_raise : bool, optional
            Raise SystemExit if SQL query was not performed (default True)
            
        Returns
        ----------
        Boolean value if query was performed or not
        
        Raises
        ----------
        SystemExit
            If err_raise == True and query was not performed      
        """
        
        # check data
        valid, reason = TypeValidator.str(query, reason=True)
        None if valid else logger.wrong_input(self, "query", query, reason)

        valid, reason = TypeValidator.bool(err_raise, reason=True)
        None if valid else logger.wrong_input(self, "err_raise", err_raise, reason)
        
        self.connect()
        
        try:
            self.cursor_PSYCOPG.execute(query)
            logger.debug(f"Following query has been executed: \n <{query}>!")
            return True
        
        except Exception:
            logger.exception(f"Following query could not been executed: \n <{query}>!", terminate=err_raise)
            return False
    
    
    def load_dataframe(self, query:str, err_raise:bool = True) -> pd.DataFrame:
        """ Executes query in the database 
        
        Parameters
        ----------
        query : str
            SQL query which should be performed
        err_raise : bool, optional
            Raise SystemExit if pd.DataFrame could not be loaded (default True)
            
        Returns
        ----------
        pd.DataFrame
        
        Raises
        ----------
        SystemExit
            If err_raise == True and query was not performed      
        """ 
        # check data
        valid, reason = TypeValidator.str(query, reason=True)
        None if valid else logger.wrong_input(self, "query", query, reason)

        valid, reason = TypeValidator.bool(err_raise, reason=True)
        None if valid else logger.wrong_input(self, "err_raise", err_raise, reason)
        
        self.connect()

        try:
            df = pd.read_sql(query, con=self._conn_PSYCOPG)
            
            # get dataframe info
            df_memory = round(df.memory_usage(deep=True).sum()/(1024)**2, 5)
            df_info = f"Downloaded table has {df.shape[0]} rows, {df.shape[1]} columns and takes {df_memory} MB of free space."
            logger.debug(f"DataFrame from following query has been executed: \n <{query}>! \n {df_info}")    
            logger.warning(f"DataFrame from query is empty!\n<{query}>") if df.empty else None
            return df

        except Exception:
            logger.exception(f"Following query has could not been executed: \n <{query}>!", terminate=err_raise)
            return False
        
        
    def save_dataframe(self, df:pd.DataFrame, table:str, schema:str = None, if_exists:str = "fail", err_raise:bool = True) -> bool:
        """ Executes query in the database 
        
        Parameters
        ----------
        df : pd.DataFrame
            DataFrame which should be saved in the database
        table : str
            Name of the table where DataFrame should be saved
        schema : str, optional
            Name of the schema where DataFrame should be saved (default None)   
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
        ValueError
            If if_exists == fail and table already exists
        """         
        
        # check data
        valid, reason = TypeValidator.object(df, class_name="DataFrame", reason=True)
        None if valid else logger.wrong_input(self, "df", df, reason)
        
        valid, reason = TypeValidator.str(table, reason=True)
        None if valid else logger.wrong_input(self, "table", table, reason)

        valid, reason = TypeValidator.str(schema, reason=True, none_allowed=True)
        None if valid else logger.wrong_input(self, "schema", schema, reason)

        None if if_exists in ["fail", "replace", "append"] else logger.wrong_input(self, "if_exists", if_exists, 'NOT IN AVAILABLE OPTIONS ["fail", "replace", "append"]')
        
        valid, reason = TypeValidator.bool(err_raise, reason=True)
        None if valid else logger.wrong_input(self, "err_raise", err_raise, reason)     
        
        self.connect()       

        try:
            df.to_sql(name=table, schema=schema, con=self._sqlalch_engine, if_exists=if_exists, method="multi")
            logger.info(f"DataFrame has been saved into {schema}.{table} in {self._database} database!")            
            return True
            
        except Exception:
            logger.exception(f"Unfortunately, it was not possible to save the dataframe! \n {df}", terminate=err_raise)
            return False
        
# %% NOTES
