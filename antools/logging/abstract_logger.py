# -*- coding: utf-8 -*-
"""
ABSTRACT LOGGER
"""

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