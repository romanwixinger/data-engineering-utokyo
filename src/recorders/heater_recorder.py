# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 11:06:02 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Log of the IR heater output percentage for target heating. 
"""


import sys
sys.path.insert(0,'..')

import numpy as np
import pandas as pd
import csv

from recorders.recorder import Recorder


class HeaterRecorder(Recorder): 
    """ Class for data engineering of the heater data. """
    
    def __init__(self, filepath: str):
        super(HeaterRecorder, self).__init__(filepath, True)
        self.nr_meta_data_rows = 6
    
    def _load_new_data(self) -> pd.DataFrame:  
        df = pd.read_csv(filepath_or_buffer=self.filepath, 
                                 skiprows=self.nr_meta_data_rows+self.read_data_lines-1, 
                                 header=0, 
                                 names=["Date", "Time", "Unknown", "TargetPercentage", "MeasuredPercentage"],
                                 encoding="utf-8")
        self.read_data_lines += len(df.index)
        return df
    
    def _load_metadata(self): 
        with open(self.filepath, newline='', encoding="utf-8") as f:
            reader = csv.reader(f)
            metadata_list = list(reader)[:self.nr_meta_data_rows]
            columns = [m[0] for m in metadata_list]
            row = [metadata_list[i][1] for i in range(2)] +  [f"{metadata_list[i][3]},{metadata_list[i][4]}" for i in range(2, 6)]
            return pd.DataFrame(data=[row], columns=columns)
    
    def _harmonize_time(self): 
        self._table_df["datetime"] = self._table_df["Date"].apply(lambda s: s.replace("/", "-")) + " " + self._table_df["Time"]
        self._table_df["datetime_μs"] = self._table_df["datetime"].apply(lambda s: s+".000000")
        self._table_df["datetime_ms"] = self._table_df["datetime"].apply(lambda s: s+".000")
        self._table_df["timestamp"] = self._table_df["datetime_ms"].apply(pd.Timestamp).values.astype(np.int64)
        
        # Create sub tables
        self._data_df = self._table_df[list(self._data_df.columns) + ["datetime", "datetime_μs", "datetime_ms", "timestamp"]]
        self._metadata_df = self._table_df[list(self._metadata_df.columns)]
        
        return