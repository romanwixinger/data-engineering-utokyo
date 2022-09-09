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

from recorders.recorder import Recorder


class PMTRecorder(Recorder): 
    
    def __init__(self, 
                 filepath: str, 
                 has_metadata: bool=False, 
                 always_update: bool=False):
        super(PMTRecorder, self).__init__(
            filepath=filepath, 
            has_metadata=has_metadata, 
            delimiter=",",
            always_update=always_update
            )
        
    def _load_initial_data(self): 
        df = pd.read_csv(filepath_or_buffer=self.filepath)
        return df.drop(["Unnamed: 5"], axis=1)
    
    def _harmonize_time(self):
        self._table_df["datetime_μs"] = self._table_df["Time"].apply(lambda s: s+"000")
        self._table_df["datetime_ms"] = self._table_df["Time"]
        self._table_df["datetime"] = self._table_df["Time"].apply(lambda s: s[:-4])
        self._table_df["timestamp"] = self._table_df["Time"].apply(pd.Timestamp).values.astype(np.int64)
