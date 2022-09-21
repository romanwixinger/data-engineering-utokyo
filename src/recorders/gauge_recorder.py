# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 11:09:40 2022


@author: Roman Wixinger (roman.wixinger@gmail.com)

Gauge Recorder. 
"""

import sys
sys.path.insert(0,'..')

import numpy as np
import pandas as pd

from recorders.recorder import Recorder


class GaugeRecorder(Recorder): 
    
    def __init__(self, filepath: str, always_update: bool=False):
        super(GaugeRecorder, self).__init__(
            filepath=filepath, 
            has_metadata=False, 
            delimiter=",",
            always_update=always_update
            )
        
    def _load_initial_data(self): 
        return pd.read_csv(
            filepath_or_buffer=self.filepath, 
            header=0, 
            names=["Timestamp", "Rb disp.", "Neut.","Surf. Ref.","NC1","NC2","NC3"]
            )  
    
    def _harmonize_time(self): 
        self._table_df["datetime"] = pd.to_datetime(self._table_df["Timestamp"])
        self._table_df["timestamp"] = self._table_df["datetime"].values.astype(np.int64)

