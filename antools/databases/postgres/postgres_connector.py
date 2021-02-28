"""
POSTGRESQL CONNECTOR CLASS

@ author: Antonín Drozda
@ organization: Freelancer
@ project: Anton's Tools
@ date: 27/02/2021

Connector used for communicating with PostgreSQL database.
"""

# %% FILE METADATA
__title__ = "POSTGRESQL CONNECTOR CLASS"
__author__ = "Antonín Drozda"
__organization__ = "Freelancer"
__project__ = "Anton's Tools"
__date__ = "27/02/2021"

# %% LIBRARY IMPORT
import psycopg2
import pandas as pd
import os
from sqlalchemy import create_engine
from configparser import ConfigParser 

# %% FILE IMPORT

# %% INPUTS

# %% CLASSES
class PostgreSQLConnector:
    """ Connector used for communication with PostgreSQL database
    
    ...

    Attributes
    ----------
    db_username : str
        Username credential for database connection
    db_password : str
        Password used for database connection
    _ini_file : str
        Path to the .ini file where db_name, hostname, and port is stored
    _ini_db_section : str
        Name of the section in <_ini_file> for relevant database
    _config_reader : class
        Class used for reading .ini files
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
    _read_properties(self)
        Read database properties from <_ini_file>
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
    @ created: 27/02/2021
    
    """
    s
    def __init__(self, db_username:str, db_password:str, ini_file:str, ini_db_section:str):
        """
        ...
        
        Parameters
        ----------
        db_username : str
            Username credential for database connection
        db_password : str
            Password used for database connection
        ini_file : str
            Path to the .ini file where db_name, hostname, and port is stored
        ini_db_section : str
            Name of the section in <_ini_file> for relevant database            
        """        
        self.db_username = db_username
        self.db_password = db_password       
        self._ini_file = ini_file
        self._ini_db_section = ini_db_section
        
        # automatically reads properties from <_.ini_file>
        self._config_reader = ConfigParser()             
        self._read_properties()
        self._is_connected = False 
         
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
        
        # check if db_username is string
        if not isinstance (self.db_username, str): 
            raise ValueError(f"PostgreSQLConnector obtained invalid variable: <db_username> = <{self.db_username}>. It must be a string!")

        # check if db_username is string
        if not isinstance (self.db_password, str): 
            raise ValueError(f"PostgreSQLConnector obtained invalid variable: <db_password> = <{self.db_password}>. It must be a string!")
            
        # check if file exist
        if not os.path.isfile(self._ini_file):   
            raise ValueError(f"PostgreSQLConnector obtained invalid variable: <ini_file> = <{self._ini_file}>.It must be system path to the .ini file!")
            
        
        # check if file type is .ini
        if not self._ini_file.endswith(".ini"):
            raise ValueError(f"PostgreSQLConnector obtained invalid variable: <ini_file> = <{self._ini_file}>. It must be system path to the .ini file!")
        
        # read file
        self._config_reader.read(self._ini_file)
        
        # check if sections exist
        if not self._ini_db_section in self._config_reader.sections():
            raise ValueError(f"PostgreSQLConnector obtained invalid variable: <ini_db_section> = <{self._ini_db_section}>. It must be valid section in .ini file!")
        
    def _read_properties(self):
        """Check validity of class inputs
        
        Parameters
        ----------
        None
        
        Raises
        ----------
        KeyError
            If ConfigReader cannot obtain some of the database credentials
            If ini file does not contain db_hostname, db_port or db_name
            
        """        
        # checks if inputs are vald before reading ini file
        self._check_inputs()
        
        # try to read properties
        try:
            self.db_hostname = self._config_reader.get(self._ini_db_section, 'hostname')
            self.db_port = self._config_reader.get(self._ini_db_section, 'port')
            self.db_name = self._config_reader.get(self._ini_db_section, 'database')
            
        except:
            raise KeyError(f"File <{self._ini_file}> for connecting to PostgreSQL database does not contains mandatory parameters<{self._ini_section}>!")

    
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
            self.conn_PSYCOPG = psycopg2.connect(host=self.db_hostname, 
                                        port=self.db_port, 
                                        database=self.db_name,
                                        user=self.db_username,
                                        password=self.db_password)
               
            self.conn_PSYCOPG.autocommit = True
            self.cursor_PSYCOPG = self.conn_PSYCOPG.cursor()  
            return self.conn_PSYCOPG
            
        except:
            self._is_connected = False
            self.conn_PSYCOPG = None
            raise SystemExit(f"PostgreSQLConnector was unable to connect to <{self.db_name}> database!")            
            
    
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
            self._sqlalch_engine = create_engine(f"postgresql://{self.db_username}:{self.db_password}@{self.db_hostname}:{self.db_port}/{self.db_name}",
                                    connect_args={'connect_timeout': 3})
            self.conn_SQLALCH = self._sqlalch_engine.connect()
            return self.conn_SQLALCH
            
        except:
            self._is_connected = False
            self.conn_SQLALCH = None
            raise SystemExit(f"PostgreSQLConnector was unable to connect to <{self.db_name}> database!")
            
            

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
            return True
        except:
            if err_raise:
                raise SystemExit(f"Query could not be executed! \n '{query}'")
            else:
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
            # df_memory = round(df.memory_usage(deep=True).sum()/(1024)**2, 5)
            # df_info = f"Downloaded table has {df.shape[0]} rows, {df.shape[1]} columns and takes {df_memory} MB of free space."
            
            return df

        except:
            if err_raise:
                raise SystemExit(f"DataFrame could not be loaded from following query! \n '{query}'")
            else:
                return False


    def save_dataframe(self, df:pd.DataFrame, db_table:str, db_schema:str = None, if_exists:str = "fail", err_raise:bool = True) -> bool:
        """ Executes query in the database 
        
        Parameters
        ----------
        df : pd.DataFrame
            DataFrame which should be saved in the database
        db_table : str
            Name of the table where DataFrame should be saved
        db_schema : str, optional
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
            df.to_sql(name=db_table, schema=db_schema, con=self._sqlalch_engine, if_exists=if_exists, method="multi")
            return True
        except:
            if err_raise:
                raise SystemExit(f"Unfortunately, it was not possible to save the dataframe!  \n {df}")
            else:
                return False

# %% NOTES
