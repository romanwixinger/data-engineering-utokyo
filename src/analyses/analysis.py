# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 09:43:50 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)


Base class for analyses. 
"""


from abc import abstractmethod


class Analysis(object): 
    """ Class for analyzing relationsships between experimental parameters and measurements. 
    """
    
    def __init__(self, recorder, filepath, name): 
        self.recorder = recorder(filepath)
        self.name = name
        self.last_updated = 0
        
    @abstractmethod
    def run(self): 
        pass
    
    @abstractmethod
    def save(self): 
        pass