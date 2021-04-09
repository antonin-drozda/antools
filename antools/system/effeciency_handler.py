"""
EFFICIENCY HANDLER

@ author: Antonín Drozda
@ organization: Freelancer
@ project: Anton's Tools
@ date: 09/04/2021

Logger.
"""

# %% FILE METADATA
__title__ = "EFFICIENCY HANDLER"
__author__ = "Antonín Drozda"
__organization__ = "Freelancer"
__project__ = "Anton's Tools"
__date__ = "09/04/2021"

# %% LIBRARY IMPORT
import psutil
import time
import pandas as pd

# %% FILE IMPORT
from antools.logging import logger

# %% INPUTS

# %% CLASSES

class EffeciencyHandler():
    """ Handler used for comparing logical approaches of solution requirements fo memory/time usage
    
    ...
    
    Attributes
    ----------
    TIME_COL : str
        Name of the time column      
    RAM_COL : str
        Name of the RAM column
    stats: str
        Dictionary staring process data
    curr_process: str
        Process which is currently being executed
        
     Methods
    -------
    __call__(self):
        Returns get_stats method
    start(self, process:str or int)
        Starts measuring new process
    finish(self, print_results:bool = True)
        Finish measuring of current process
    get_stats(self) -> pd.DataFrame
        Returns pd.DataFrame with all processed and its data
    _get_time_memory(self)
        Returns current time and current RAM usage
        
    Raises
    --------   
    Value Error
        If any inputs does not correspond to its intended data type.
    SystemExit
        Custom user fault    
        
    Notes
    --------       
    @ author:  Antonín Drozda (https://github.com/antonin-drozda)
    @ created: 09/04/2021
    
    """
    TIME_COL = "Time (secs)"
    RAM_COL = "RAM (MB)"
    curr_process = None
    stats = {}  
    
    def __repr__(self):
        return f"{self.__class__.__name__}({list(self.stats)})"
    
    
    def __call__(self):
        """ Returns get_stats method """
        return self.get_stats() if self.stats else "NO PROCESS"


    def start(self, process:str or int):
        """ Starts measuring new process """
        
        process = str(process)
        
        # automatically finish previous aproach
        if self.curr_process:
            self.finish()
            
        self.curr_process = process
        self.stats[self.curr_process] = {}
        self.start_time, self.start_memory = self._get_time_memory()
             
        
    def finish(self, print_results:bool = True):
        """ Finish measuring of current process """
        
        if not self.curr_process:
            logger.error("Process has not yet started!")

        end_time, end_memory = self._get_time_memory()
        time_diff = round(end_time - self.start_time, 4)
        memory_diff = round(end_memory - self.start_memory, 4)
        
        memory_diff = 0 if memory_diff < 0 else memory_diff
        
        self.stats[self.curr_process][self.TIME_COL] = time_diff 
        self.stats[self.curr_process][self.RAM_COL] = memory_diff
        
        if print_results:
            print(f"Process <{self.curr_process}> took {time_diff} seconds to execute!")
            print(f"Memory usage was {memory_diff} MB!")
            
        self.curr_process = None


    def get_stats(self) -> pd.DataFrame:
        """ Returns pd.DataFrame with all processed and its data """
        
        # automaticall finish previous process
        if self.curr_process:
            self.finish()
            
        df = pd.DataFrame(data=self.stats).transpose().sort_values(by=[self.TIME_COL], ascending=True)
        mins_dict = df.idxmin().to_dict()
        
        for column, column_result in zip([self.TIME_COL, self.RAM_COL], ["Time Efficiency (%)", "RAM Efficiency (%)"]):
            min_value = df.loc[mins_dict[column]][column]
            df[column_result] = round(100/(df[column]/min_value), 2)
        
        return df
    
    
    def _get_time_memory(self):
        curr_time = time.time()
        curr_ram = (psutil.virtual_memory().used) / 1000000
        return curr_time, curr_ram

# %% NOTES