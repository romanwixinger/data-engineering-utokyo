# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 18:05:39 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Simple recorders to track the result of the SSDAnalysis, ImageAnalysis and the
parameter inputs. 
"""

import sys
sys.path.insert(0,'..')

import numpy as np
import pandas as pd

from recorders.recorder import Recorder


class SSDResultsRecorder(Recorder):
    """ Tracks the result file of the SSD Analysis. 
    """
    def __init__(self, filepath: str, always_update: bool=False): 
        super(SSDResultsRecorder, self).__init__(
            filepath=filepath, 
            has_metadata=False, 
            always_update=always_update
            )
        
    def _harmonize_time(self):
        self._table_df["timestamp"] = self._table_df["timestamp_ns"]
        self._timestamp_to_datetimes(self._table_df)
        

class ImageResultsRecorder(Recorder): 
    """ Tracks the result file of the ImageAnalysis. 
    """
    
    def __init__(self, filepath: str, always_update: bool=False): 
        super(ImageResultsRecorder, self).__init__(
            filepath=filepath, 
            has_metadata=False, 
            always_update=always_update
            )
    
    def _harmonize_time(self): 
        self._table_df["timestamp"] = self._table_df["datetime"].apply(pd.Timestamp).values.astype(np.int64)


class ParameterRecorder(Recorder): 
    """ Tracks the parameter settings of each cycle. 
    """
    
    def __init__(self, filepath: str, always_update: bool=False): 
        super(ParameterRecorder, self).__init__(
            filepath=filepath, 
            has_metadata=False, 
            always_update=always_update
            )
        
    def _harmonize_time(self):
        self._table_df["datetime"] = pd.to_datetime(self._table_df["Time"])
        self._table_df["datetime_μs"] = self._table_df["datetime"].apply(lambda s: str(s) +".000000")
        self._table_df["datetime_ms"] = self._table_df["datetime"].apply(lambda s: str(s)+".000")
        self._table_df["timestamp"] = self._table_df["datetime"].values.astype(np.int64)