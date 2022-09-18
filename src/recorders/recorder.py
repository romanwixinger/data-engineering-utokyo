# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 17:08:58 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Base class for creating real-time representation of csv files as pandas tables.
To use the class, just overwrite the three abstractmethods according to the 
csv table which you want to map to a real-time recorder object. 
"""

import sys
sys.path.insert(0,'..')

import os
import pandas as pd
import time
import datetime
from abc import abstractmethod


class Recorder(object): 
    """ Base class for mapping a csv file to a pandas dataframe in real-time when it changes. 
    """
    
    def __init__(self, 
                 filepath: str, 
                 has_metadata: bool=True, 
                 delimiter: str=",", 
                 always_update: bool=False,
                 encoding="utf-8"): 
        
        # Settings
        self.filepath = filepath
        self.has_metadata = has_metadata
        self.delimiter = delimiter
        self.always_update = always_update
        self.encoding = encoding
        
        # Tracking
        self.read_data_lines = 0
        self.last_updated = 0
        
        # Dataframes 
        self._table_df = None     # Data x Metadata
        self._data_df = None      # Data
        self._metadata_df = None  # Metadata
        self._data_columns = []

    def get_table(self) -> pd.DataFrame: 
        self._update()
        self.last_updated = self._get_mod_time()
        return self._table_df
    
    def get_data(self) -> pd.DataFrame: 
        self._update_data()
        self.data_last_updated = self._get_mod_time()
        return self._data_df
    
    def get_metadata(self) -> pd.DataFrame:
        self._metadata_df = self._load_metadata() if self.has_metadata else pd.DataFrame()
        return self._metadata_df
    
    def is_up_to_date(self) -> bool:
        return self.last_updated == self._get_mod_time()
    
    def _get_mod_time(self): 
        return time.ctime(os.path.getmtime(self.filepath))
    
    def _update(self): 
        if self.is_up_to_date() and not self.always_update: 
            return 
        
        # Merge with metadata
        self._data_df = self.get_data()
        if self.has_metadata: 
            self._metadata_df = self.get_metadata()
            self._table_df = self._data_df.merge(self._metadata_df, how='cross')
        else: 
            self._table_df = self._data_df
            
        # Order 
        self._harmonize_time()
        self.last_updated = self._get_mod_time()
        
    def _update_data(self):
        """ Updates self._data_df and self.data_last_updated incrementally. Makes use of _load_new_data(). 
        """
        
        # Case first loading 
        if self.read_data_lines == 0: 
            self._data_df = self._load_initial_data()
            self._data_columns = list(self._data_df.columns) 
            self.read_data_lines += len(self._data_df.index)
            return 
        
        # Case reloading
        new_data_df = self._load_new_data()
        self.read_data_lines += len(new_data_df.index)
        if len(new_data_df.index) == 0: 
            return

        # Concatenate old and new
        self._data_df = pd.concat(
            [self._data_df, new_data_df],
            axis=0,
            join="outer",
            ignore_index=True,
            copy=True
        )
    
    def _timestamp_to_datetimes(self, df: pd.DataFrame): 
        """ Takes a pandas dataframe with a timestamp column (int) and also adds date datetime, datetime_ms, datetime_μs. 
        """
        # Conversion functions
        conversion_to_datetime_μs = lambda x: datetime.datetime.fromtimestamp(x/1000000000).strftime('%Y-%m-%d %H:%M:%S.%f')
        conversion_to_datetime_ms = lambda x: datetime.datetime.fromtimestamp(x/1000000000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        conversion_to_datetime = lambda x: datetime.datetime.fromtimestamp(x/1000000000).strftime('%Y-%m-%d %H:%M:%S')

        # Apply conversions
        df["datetime_μs"] = df["timestamp"].apply(conversion_to_datetime_μs)
        df["datetime_ms"] = df["timestamp"].apply(conversion_to_datetime_ms)
        df["datetime"] = df["timestamp"].apply(conversion_to_datetime)
    
    @abstractmethod
    def _load_initial_data(self) -> pd.DataFrame: 
        """ Returns all data up to now and defines the data columns. 
        """
        return pd.read_csv(
            filepath_or_buffer=self.filepath, 
            delimiter=self.delimiter,
            encoding=self.encoding
            )
    
    @abstractmethod
    def _load_new_data(self) -> pd.DataFrame: 
        """ Returns the rows which have not been loaded so far. 
        """
        return pd.read_csv(
            filepath_or_buffer=self.filepath, 
            skiprows=self.read_data_lines,
            header=0,
            names=self._data_columns,
            encoding=self.encoding
            )
    
    @abstractmethod
    def _load_metadata(self) -> pd.DataFrame: 
        """ Reloads all metadata. 
        """
        pass
    
    @abstractmethod
    def _harmonize_time(self): 
        if "ctime" in self._table_df.columns: 
            self._table_df["timestamp"] = self._table_df["ctime"].apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S.%f'))
            self._table_df["datetime"] =  self._table_df["timestamp"].apply(pd.Timestamp)
            self._table_df["datetime_μs"] = self._table_df["datetime"]
            self._table_df["datetime_ms"] = self._table_df["datetime"].apply(lambda s: str(s)[:-3])
        else: 
            raise Exception("Recorder failed to harmonize time. Either provide a ctime column or override this method.")