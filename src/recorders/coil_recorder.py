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
       
    def __init__(self, filepath: str, always_update: bool=False):
        super(CoilRecorder, self).__init__(
            filepath=filepath, 
            has_metadata=False, 
            delimiter="	",
            always_update=always_update
            )
    
    def _harmonize_time(self): 
        self._table_df["datetime"] = self._table_df["Time"]
        self._table_df["timestamp"] = self._table_df["Time"].apply(pd.Timestamp).values.astype(np.int64)
