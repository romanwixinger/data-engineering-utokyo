# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 11:03:58 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

When we already have a pandas dataframe and want to use it in the form of a 
recorder, for example in the ImageAnalysis for the camera data from the laser
room, then we use this static recorder. 
"""

import sys
sys.path.insert(0,'../..')  # Set src as top-level

import pandas as pd


class StaticRecorder(): 
    """ Represents a static pandas dataframe as a recorder. 
    """
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        
        # Public variables from Recorder. 
        self.filepath = None
        self.has_metadata = False
        self.delimiter = None
        self.always_update = False
        self.encoding = None
        self.read_data_lines = len(df.index)
        self.last_updated = 0
        
    def get_table(self) -> pd.DataFrame: 
        return self.df
    
    def get_data(self) -> pd.DataFrame: 
        return self.df
    
    def get_metadata(self) -> pd.DataFrame:
        return pd.DataFrame()
    
    def is_up_to_date(self) -> bool:
        return True
