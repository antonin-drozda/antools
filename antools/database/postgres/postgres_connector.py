"""
POSTGRESQL CONNECTOR CLASS

@ author: Antonín Drozda
@ organization: Freelancer
@ project: Anton's Tools
@ date: 25/03/2021

Connector used for communicating with PostgreSQL database.
"""

# %% FILE METADATA
__title__ = "POSTGRESQL CONNECTOR CLASS"
__author__ = "Antonín Drozda"
__organization__ = "Freelancer"
__project__ = "Anton's Tools"
__date__ = "25/03/2021"

# %% LIBRARY IMPORT
import psycopg2
import pandas as pd
from sqlalchemy import create_engine 

# %% FILE IMPORT
from antools.logging import logger

# %% INPUTS

# %% CLASSES
class PostgreSQLConnector():
    """ Connector used for communication with PostgreSQL database
    
    ...

    Attributes
    ----------
    database : str
        Name of the database
    user : str,
        Name of the user
    password : str
        Password for database connection
    server : str
        Server name (default 'localhost')
    port : str or int
        Port for connection
    _is_connected : bool
        Boolean value storing info about PostgreSQLConnector connection
    _conn_PSYCOPG : class
        Connection using <psycopg2> library
    _conn_SQLALCH : class
        Connection using <sqlalchemy> library        
    _cursor_PSYCOPG : class
        Cursor used for executing queries


    Methods
    -------
    _check_inputs(self)
        Check validity of class inputs
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
    
    def __init__(self, database:str, user:str, password:str,
                     server:str = 'localhost', port:str or int = '5432'):
        
        self.database = database
        self.user = user
        self.password = password
        self.server = server
        self.port = port
    
        self._check_inputs()
        self._is_connected = False
        self.connect()
        
    
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

            
        # check if database is string
        if not isinstance (self.database, str): 
            raise ValueError(f"PostgreSQLConnector obtained invalid variable: <database> = <{self.database}>. It must be a string!")

        # check if user is string
        if not isinstance (self.user, str): 
            raise ValueError(f"PostgreSQLConnector obtained invalid variable: <user> = <{self.user}>. It must be a string!")

        # check if password is string
        if not isinstance (self.password, str): 
            raise ValueError("PostgreSQLConnector obtained invalid variable: <password> = <XXX>. It must be a string!")

        # check if server is string
        if not isinstance (self.server, str): 
            raise ValueError(f"PostgreSQLConnector obtained invalid variable: <server> = <{self.server}>. It must be a string!")

        # check if port is can be integer
            try:
                self.port = int(self.port)
            except ValueError:
                raise ValueError(f"PostgreSQLConnector obtained invalid variable: <port> = <{self.port}>. It cannot be transformed into integer!")
                
                
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
        
        if not self._is_connected:
            self._conn_PSYCOPG = self._connect_with_PSYCOPG()
            self._conn_SQLACH = self._connect_with_SQLALCH()        

            if self._conn_PSYCOPG and self._conn_SQLACH:
                self._is_connected = True

            logger.info(f"Connection to the <{self.database}> database was sucessful!")
            
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
            self.conn_PSYCOPG = psycopg2.connect(host=self.server, 
                                        port=self.port, 
                                        database=self.database,
                                        user=self.user,
                                        password=self.password)
               
            self.conn_PSYCOPG.autocommit = True
            self.cursor_PSYCOPG = self.conn_PSYCOPG.cursor()  
            return self.conn_PSYCOPG
            
        except Exception:
            self._is_connected = False
            self.conn_PSYCOPG = None
            logger.exception(f"Connection to the <{self.database}> database was not sucessful!", terminate=True)      

    
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
            self._sqlalch_engine = create_engine(f"postgresql://{self.user}:{self.password}@{self.server}:{self.port}/{self.database}",
                                    connect_args={'connect_timeout': 3})
            self.conn_SQLALCH = self._sqlalch_engine.connect()
            return self.conn_SQLALCH
            
        except Exception:
            self._is_connected = False
            self.conn_SQLALCH = None
            logger.exception(f"Connection to the <{self.database}> database was not sucessful!", terminate=True)      

            
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
            logger.debug(f"<{self.database}> database was disconnected!")
            
        return self.is_connected

            
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
        
        if not self._is_connected:
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
        
        if not self._is_connected:
            self.connect()   
        try:
            df = pd.read_sql(query, con=self._conn_PSYCOPG)
            
            # get dataframe info
            df_memory = round(df.memory_usage(deep=True).sum()/(1024)**2, 5)
            df_info = f"Downloaded table has {df.shape[0]} rows, {df.shape[1]} columns and takes {df_memory} MB of free space."
            logger.info(f"DataFrame from following query has been executed: \n <{query}>! \n {df_info}")    
            
            if df.empty:
                logger.warning("DataFrame is empty!")
            
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
            If fail_terminate == True and DataFrame was not saved
        ValueError
            If if_exists == fail and table already exists
        """         
        
        if not self._is_connected:
            self.connect()          

        try:
            df.to_sql(name=table, schema=schema, con=self._sqlalch_engine, if_exists=if_exists, method="multi")
            logger.info(f"DataFrame has been saved into {schema}.{table} in {self.database} database!")            
            return True
            
        except Exception:
            logger.exception(f"Unfortunately, it was not possible to save the dataframe! \n {df}", terminate=err_raise)
            return False
        
# %% NOTES

