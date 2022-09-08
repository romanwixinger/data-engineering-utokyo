# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 11:11:54 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Laser recorder.
"""

import sys
sys.path.insert(0,'..')

import numpy as np
import pandas as pd
import csv

from recorders.recorder import Recorder


class LaserRecorder(Recorder): 
    
    def __init__(self, filepath: str, always_update: bool=False): 
        super(LaserRecorder, self).__init__(
            filepath=filepath, 
            has_metadata=True,
            always_update=always_update
            )
        
    def _load_initial_data(self):
        df = pd.read_csv(
            filepath_or_buffer=self.filepath, 
            skiprows=119,
            delimiter="	"
            )
        df = self._aggregate_laser_rows(df)
        self.read_data_lines += 5 * len(df.index)
        return df
    
    def _load_new_data(self): 
        df = pd.read_csv(
            filepath_or_buffer=self.filepath, 
            skiprows=119+self.read_data_lines,
            delimiter="	",
            header=0,
            names=self._data_columns
            )
        df = self._aggregate_laser_rows(df)
        self.read_data_lines += 5 * len(df.index)
        return df

    def _aggregate_laser_rows(self, original_df: pd.DataFrame): 
        """ Originally, one measurement of the six laser wavelengths is distributed over six rows. We aggregate 
            these rows into one row. The only tradeoff is that we have to approximate the time with the time
            of the last measurement. 
        """
        
        time_column = 'Time  [ms]'
        laser_columns = original_df.columns[1:]
        
        row_lookup = {}
        row_list = []
        
        for index, row in original_df.iterrows():
            column_index = pd.Series.first_valid_index(row[1:])
            row_lookup[column_index] = row[column_index]
            # Count if all 6 lasers have been measured
            if len(row_lookup) == 6:     
                item = [row[time_column]] + [row_lookup[col] for col in laser_columns]
                row_list.append(item)
                row_lookup = {}

        df = pd.DataFrame(data=row_list, columns=original_df.columns)
        return df
        
    def _load_metadata(self):     
        with open(self.filepath, newline='', encoding="cp932") as f:
            reader = csv.reader(f, delimiter="	")
            metadata_list = list(reader)[:119]
            
            # Title
            title_column = ["Title"]
            title_row = [metadata_list[0][0]]
            
            # General info
            gi_columns = [m[0] for m in metadata_list[1:7]]
            gi_rows = [self._combine(m[1:]) for m in metadata_list[1:7]]
            
            # General settings
            gs_columns = [m[0] for m in metadata_list[9:20]]
            gs_rows = [self._combine(m[1:]) for m in metadata_list[9:20]]

            # Frames 1-6
            frame_columns = (
                [m[0] for m in metadata_list[22:36]]
                + [m[0] for m in metadata_list[38:52]]
                + [m[0] for m in metadata_list[54:68]]
                + [m[0] for m in metadata_list[70:84]]
                + [m[0] for m in metadata_list[86:100]]
                + [m[0] for m in metadata_list[102:116]]
            )
            
            frame_rows = (
                [self._combine(m[1:]) for m in metadata_list[22:36]]
                + [self._combine(m[1:]) for m in metadata_list[38:52]]
                + [self._combine(m[1:]) for m in metadata_list[54:68]]
                + [self._combine(m[1:]) for m in metadata_list[70:84]]
                + [self._combine(m[1:]) for m in metadata_list[86:100]]
                + [self._combine(m[1:]) for m in metadata_list[102:116]]
            )
            
            columns = title_column + gi_columns + gs_columns + frame_columns
            row = title_row + gi_rows + gs_rows + frame_rows
            return pd.DataFrame(data=[row], columns=columns)
    
    def _combine(self, entries: list): 
        """ If entries has length 1, then it returns the entry. 
            Otherwise, it converts the list to a comma separated string. 
        """
        if len(entries) == 0: 
            return None
        
        if len(entries) == 1: 
            return entries[0]
        
        return ",".join(entries)
    
    def _harmonize_time(self):

        # Convert 15.03.2022, 08:46:39.387 to 15-03-2022 08:46:39.387
        helper_df = pd.DataFrame()
        helper_df["StartTime"] = self._table_df["StartTime"].apply(lambda s: s.replace(",", "").replace(".", "-", 2))
        
        # Calculate absolute time based on relative time
        helper_df["start_datetime"] = pd.to_datetime(helper_df["StartTime"])
        helper_df["start_timestamp"] = helper_df["start_datetime"].values.astype(np.int64)
        helper_df["timestamp"] = helper_df["start_timestamp"] + self._table_df["Time  [ms]"] * 1e3
        
        # Add datetimes
        self._table_df["timestamp"] = helper_df["timestamp"]
        self._timestamp_to_datetimes(self._table_df)
        
        return