# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 17:26:25 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)


PMT Recorder 

"""


import sys
sys.path.insert(0,'..')

import numpy as np
import pandas as pd

from recorder import Recorder
from constants import Locations as loc


class PMTRecorder(Recorder): 
    
    def __init__(self, filepath: str=location+"all_data.csv", has_metadata: bool=False):
        super(PMTRecorder, self).__init__(filepath, has_metadata)
    
    def _load_new_data(self): 
        
        # First time 
        if self.read_data_lines == 0: 
            df = pd.read_csv(filepath_or_buffer=self.filepath, skiprows=self.read_data_lines)
            df = df.drop(["Unnamed: 5"], axis=1)

        # Later time 
        else: 
            df = pd.read_csv(
                filepath_or_buffer=self.filepath, 
                skiprows=self.read_data_lines, 
                names=self._data_df.columns
            )
        self.read_data_lines += len(df.index)
        return df
    
    def _harmonize_time(self):
        
        # Harmonize table
        self._table_df["datetime_μs"] = self._table_df["Time"].apply(lambda s: s+"000")
        self._table_df["datetime_ms"] = self._table_df["Time"]
        self._table_df["datetime"] = self._table_df["Time"].apply(lambda s: s[:-4])
        self._table_df["timestamp"] = self._table_df["Time"].apply(pd.Timestamp).values.astype(np.int64)
        
        # Create sub tables
        self._data_df = self._table_df
        self._metadata_df = pd.DataFrame()

        return 