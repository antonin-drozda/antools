"""
PROGRESS BAR CLASS

@ author: Antonín Drozda
@ organization: Freelancer
@ project: Anton's Tools
@ date: 25/03/2021

PROGRESS BAR FOR SHOWING PROGRESS
"""

# %% FILE METADATA
__title__ = "PROGRESS BAR CLASS"
__author__ = "Antonín Drozda"
__organization__ = "Freelancer"
__project__ = "Anton's Tools"
__date__ = "30/03/2021"

# %% LIBRARY IMPORT

# %% FILE IMPORT
from antools.logging import logger
from antools.shared import TypeValidator

# %% INPUTS

# %% CLASSES

class ProgressBar():
    """ Class for showing progress in for loop
        ...
        
        Attributes
        ----------
        prefix:
            String shown before progress bar (default PROGRESS)
        suffix:
            String shown after progress bar (default completed)
        decimals:
            Number of decimal shown in float showing scale 0-100
        length:
            Length of progress bar
        fill:
            Character which will shown already done part
        
    
            
        Methods
        -------
        start(self, total:int) -> print
            Initializing Bar with total number of loops to be made
        update(self, update:int) -> print
            Updates progress of progress bar        
        _print_bar(self, total:int) -> print
            Prints current state of Progress Bar
            
        Raises
        --------   
        None   
            
        Notes
        --------       
        @ author:  Antonín Drozda (https://github.com/antonin-drozda)
        @ created: 30/03/2021
        
        """    
        
    def __init__(self, prefix:str='PROGRESS', suffix:str='completed', decimals:int=1, length:int=25, fill:str='█'):
        """
        ...
        
        Parameters
        ----------
        prefix:
            String shown before progress bar (default PROGRESS)
        suffix:
            String shown after progress bar (default completed)
        decimals:
            Number of decimal shown in float showing scale 0-100
        length:
            Length of progress bar
        fill:
            Character which will shown already done part
            
        """
        
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.length = length
        self.fill = fill
        
        self.iteration = 0
        self.total = 0
        
        # check inputs from constructor
        valid, reason = TypeValidator.str(self.prefix, reason=True)
        None if valid else logger.wrong_input(self, "prefix", self.prefix, reason)
    
        valid, reason = TypeValidator.str(self.suffix, reason=True)
        None if valid else logger.wrong_input(self, "suffix", self.suffix, reason)

        valid, reason = TypeValidator.int(self.decimals, reason=True)
        None if valid else logger.wrong_input(self, "decimals", self.decimals, reason)
        
        valid, reason = TypeValidator.int(self.length, reason=True)
        None if valid else logger.wrong_input(self, "length", self.length, reason)

        valid, reason = TypeValidator.str(self.fill, reason=True)
        None if valid else logger.wrong_input(self, "fill", self.fill, reason)

    
    def __str__(self):
        return f"{self.iteration}/{self.total}"
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.iteration}/{self.total})"
        
    def start(self, total:int) -> print:
        """ Initializing Bar with total number of loops to be made """

        # check inputs from constructor
        valid, reason = TypeValidator.int(total, reason=True)
        None if valid else logger.wrong_input(self, "total", total, reason)
        
        # prints bar at 0%
        self.total = total
        self.iteration = 0
        print("\n")
        self._print_bar()
        
    
    def update(self, update:int=1) -> print:
        """ Updates progress of progress bar """

        # check inputs from constructor
        valid, reason = TypeValidator.int(update, reason=True)
        None if valid else logger.wrong_input(self, "update", update, reason)
        
        # update bar, not allow over 100%
        self.iteration += update
        self.finished = True if self.iteration >= self.total else False
        if self.finished:
            self.iteration = self.total
        self._print_bar()
        
    def _print_bar(self) -> print:
        """ Prints current state of Progress Bar """
        
        percent = ("{0:." + str(self.decimals) + "f}").format(100 * (self.iteration / float(self.total)))
        filledLength = int(self.length * self.iteration // self.total)
        bar = self.fill * filledLength + '-' * (self.length - filledLength)
        print(f'\r{self.prefix}: |{bar}| {percent}% {self.suffix}', end = "\r") 
