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
    
    def __init__(self, filepath: str, has_metadata: bool=True): 
        # Settings
        self.filepath = filepath
        self.has_metadata = has_metadata
        
        # Tracking
        self.read_data_lines = 0
        self.last_updated = 0
        self.data_last_updated = 0
        self.metadata_last_updated = 0
        
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
        if not self.has_metadata: 
            return pd.DataFrame()
        self._update_metadata()
        self.metadata_last_updated = self._get_mod_time()
        self.metadata_columns = list(self._metadata_df.columns) if self._metadata_df is not None else []
        return self._metadata_df
    
    def table_is_up_to_date(self) -> bool:
        return self.last_updated == self._get_mod_time()
    
    def data_is_up_to_date(self) -> bool: 
        return self.data_last_updated == self._get_mod_time()
    
    def metadata_is_up_to_date(self) -> bool: 
        return self.metadata_last_updated == self._get_mod_time()
    
    def _update(self): 
        if self.table_is_up_to_date(): 
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
        self._table_df = self._table_df.sort_values(by="timestamp")
        self.last_updated = self._get_mod_time()
        
    def _get_mod_time(self): 
        return time.ctime(os.path.getmtime(self.filepath))
        
    def _update_data(self):
        """ Updates self._data_df and self.data_last_updated incrementally. Makes use of _load_new_data(). 
        """
        
        # Case first loading 
        if self.read_data_lines == 0: 
            self._data_df = self._load_new_data()
            return 
        
        # Case reloading
        new_data_df = self._load_new_data()
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
        return
    
    def _update_metadata(self): 
        self._metadata_df = self._load_metadata() if not self.metadata_is_up_to_date() else self._metadata_df
        return
    
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

        return
    
    @abstractmethod
    def _load_new_data(self) -> pd.DataFrame: 
        """ Returns the rows which have not been loaded so far. 
        """
    
        pass
    
    @abstractmethod
    def _load_metadata(self) -> pd.DataFrame: 
        """ Returns the current version of the metadata by reloading everything. 
        """
        pass
    
    @abstractmethod
    def _harmonize_time(self): 
        pass