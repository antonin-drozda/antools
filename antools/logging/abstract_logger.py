"""
ABSTRACT LOGGER

@ author: Antonín Drozda
@ organization: Freelancer
@ project: Anton's Tools
@ date: 20/04/2021

ABSTRACT LOGGER.
"""

# %% FILE METADATA
__title__ = "ABSTRACT LOGGER"
__author__ = "Antonín Drozda"
__organization__ = "Freelancer"
__project__ = "Anton's Tools"
__date__ = "20/04/2021"

# %% LIBRARY IMPORT
import abc

# %% FILE IMPORT

# %% CLASSES
class AbstractLogger(metaclass = abc.ABCMeta):
    """ Abstract class for Loggers """
    
    @abc.abstractmethod    
    def __init__(self):
      pass
  
    @abc.abstractmethod
    def debug(self):
        pass
    
    @abc.abstractmethod
    def info(self):
        pass
    
    @abc.abstractmethod
    def warning(self):
        pass
    
    @abc.abstractmethod
    def critical(self):
        pass
    
    @abc.abstractmethod
    def error(self):
        pass    
    
    @abc.abstractmethod
    def exception(self):
        pass
    
    @abc.abstractmethod
    def wrong_input(self):
        pass