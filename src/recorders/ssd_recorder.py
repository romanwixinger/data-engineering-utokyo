# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 17:18:01 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

SSD Recorder: Applicable for data from the WE7000 DAQ for the SSD2. 
The PMT current from the MOT will be obtained like this in our next experiment.
"""

import sys
sys.path.insert(0,'..')

import csv
import numpy as np
import pandas as pd

from recorders.recorder import Recorder
from constants import loc


class SSDRecorder(Recorder): 
    """ Class for data engineering of the SSD2 data. """

    def __init__(self, filepath: str=loc.ssd):
        super(SSDRecorder, self).__init__(filepath, True)
        self.nr_meta_data_rows = 37

    def _load_new_data(self) -> pd.DataFrame: 
        """ Just load the new part. """
        df = pd.read_csv(filepath_or_buffer=self.filepath, 
                         skiprows=self.nr_meta_data_rows + self.read_data_lines, 
                         header=0, 
                         names=["TraceName", "Time_x", "PulseHeight"])        
        self.read_data_lines += len(df.index)
        return df
        
    def _load_metadata(self): 
        """ Overwrite the metadata with the new version. """
        with open(self.filepath, newline='') as f:
            reader = csv.reader(f)
            metadata = list(reader)[:(self.nr_meta_data_rows + 1)]
            metadata =  metadata[:3] +  metadata[4:]
            columns = [line[0] for line in metadata]
            row = [line[1] for line in metadata]
            return pd.DataFrame(data=[row], columns=columns)
                
    def _harmonize_time(self): 
        """ Convert the relative time and start time to the real time. """
        
        def harmonize_table(df: pd.DataFrame) -> pd.DataFrame: 
            # Start time
            helper_df = pd.DataFrame()
            helper_df["start_datetime_str"] = df["//StartDate"].apply(lambda s: s.replace("/", "-")) + " " + df["//StartTime"]
            helper_df["start_datetime"] = pd.to_datetime(helper_df["start_datetime_str"]) 

            # Conversion parameter: Time_x * rel_time_to_ns = rel. time in ns
            time_resolution = df['//TimeResolution'][0]
            rel_time_to_ns = {
                '1.000000e-009': 1e-0,
                '1.000000e-006': 1e+3,
                '1.000000e-003': 1e+6
            }[time_resolution]

            # Real time
            helper_df["relative_time_ns"] = df["Time_x"] * rel_time_to_ns
            helper_df["start_ns"] = helper_df.start_datetime.values.astype(np.int64)
            helper_df["timestamp"] = helper_df["start_ns"] + helper_df["relative_time_ns"]

            # Add datetimes
            df["timestamp"] = helper_df["timestamp"]
            self._timestamp_to_datetimes(df)
            return df
        
        self._table_df = harmonize_table(self._table_df)
        self._data_df = self._table_df[self._data_df.columns]