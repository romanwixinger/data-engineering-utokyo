# -*- coding: utf-8 -*-
"""Records the PMT signal.

PMT stands for photo multiplier tube.
"""

import numpy as np
import pandas as pd

from .recorder import Recorder


class PMTRecorder(Recorder): 
    
    def __init__(self, 
                 filepath: str, 
                 has_metadata: bool=False, 
                 always_update: bool=False):
        super(PMTRecorder, self).__init__(
            filepath=filepath, 
            has_metadata=has_metadata, 
            delimiter=",",
            always_update=always_update
            )
        
    def _load_initial_data(self): 
        df = pd.read_csv(filepath_or_buffer=self.filepath)
        return df.drop(["Unnamed: 5"], axis=1)
    
    def _harmonize_time(self):
        self._table_df["datetime"] = self._table_df["Time"]
        self._table_df["timestamp"] = self._table_df["Time"].apply(pd.Timestamp).values.astype(np.int64)
