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
    
    def __init__(self, filepath: str):
        super(GaugeRecorder, self).__init__(filepath, False)
    
    def _load_new_data(self): 
        df = pd.read_csv(filepath_or_buffer=self.filepath, skiprows=self.read_data_lines)
        self.read_data_lines += len(df.index)
        return df
    
    def _harmonize_time(self): 
        self._table_df["datetime"] = pd.to_datetime(self._table_df["Timestamp"])
        self._table_df["datetime_μs"] = self._table_df["Timestamp"].apply(lambda s: s+".000000")
        self._table_df["datetime_ms"] = self._table_df["Timestamp"].apply(lambda s: s+".000")
        self._table_df["timestamp"] = self._table_df["datetime"].values.astype(np.int64)
        return 
