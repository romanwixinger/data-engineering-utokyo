# -*- coding: utf-8 -*-
"""Records the log of the IR heater output percentage for target heating.
"""

import numpy as np
import pandas as pd
import csv

from .recorder import Recorder


class HeaterRecorder(Recorder): 
    """ Class for data engineering of the heater data. """
    
    def __init__(self, filepath: str, always_update: bool=False):
        super(HeaterRecorder, self).__init__(
            filepath=filepath, 
            has_metadata=True,
            delimiter=",",
            always_update=always_update
            )
        self.nr_meta_data_rows = 6
        
    def _load_initial_data(self) -> pd.DataFrame: 
        return pd.read_csv(
            filepath_or_buffer=self.filepath, 
            skiprows=self.nr_meta_data_rows - 1, 
            header=0, 
            names=["Date", "Time", "Unknown", "TargetPercentage", "MeasuredPercentage"],
            encoding='Shift-JIS',
            delimiter=self.delimiter
            )
    
    def _load_new_data(self) -> pd.DataFrame: 
        """ Returns the rows which have not been loaded so far. 
        """
        return pd.read_csv(
            filepath_or_buffer=self.filepath, 
            skiprows=self.nr_meta_data_rows + self.read_data_lines - 1, 
            header=0, 
            names=["Date", "Time", "Unknown", "TargetPercentage", "MeasuredPercentage"],
            encoding='Shift-JIS',
            delimiter=self.delimiter
            )
    
    def _load_metadata(self): 
        with open(self.filepath, newline='', encoding="Shift-JIS") as f:
            reader = csv.reader(f)
            metadata_list = list(reader)[:self.nr_meta_data_rows]
            columns = [m[0] for m in metadata_list]
            row = [metadata_list[i][1] for i in range(2)] +  [f"{metadata_list[i][3]},{metadata_list[i][4]}" for i in range(2, 6)]
            return pd.DataFrame(data=[row], columns=columns)
    
    def _harmonize_time(self): 
        self._table_df["datetime"] = self._table_df["Date"].apply(lambda s: s.replace("/", "-")) + " " + self._table_df["Time"]
        self._table_df["timestamp"] = self._table_df["datetime"].apply(pd.Timestamp).values.astype(np.int64)
