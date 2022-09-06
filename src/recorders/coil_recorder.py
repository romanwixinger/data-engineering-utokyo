# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 11:04:41 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Coil Recorder: The current of the MOT coil is controlled by a relay switch. 
This text file is the log of the relay switch. 
"""


import sys
sys.path.insert(0,'..')

import numpy as np
import pandas as pd

from recorders.recorder import Recorder


class CoilRecorder(Recorder): 
       
    def __init__(self, filepath: str):
        super(CoilRecorder, self).__init__(filepath, False)
    
    def _load_new_data(self): 
        df = pd.read_csv(filepath_or_buffer=self.filepath, delimiter="	", skiprows=self.read_data_lines)
        self.read_data_lines += len(df.index)
        return df
    
    def _harmonize_time(self): 
        self._table_df["datetime_μs"] = self._table_df["Time"].apply(lambda s: s+"000")
        self._table_df["datetime_ms"] = self._table_df["Time"]
        self._table_df["datetime"] = self._table_df["Time"].apply(lambda s: s[:-4])
        self._table_df["timestamp"] = self._table_df["Time"].apply(pd.Timestamp).values.astype(np.int64)
        
        # Create sub tables
        self._data_df = self._table_df
        self._metadata_df = pd.DataFrame()
        return 