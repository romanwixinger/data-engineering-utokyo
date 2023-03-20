# -*- coding: utf-8 -*-
"""Records the HeatTimeLog.
"""

import numpy as np
import pandas as pd

from .recorder import Recorder


class HeatTimeRecorder(Recorder): 
       
    def __init__(self, filepath: str, day: str="2022-09-18-"):
        super(HeatTimeRecorder, self).__init__(
            filepath=filepath, 
            has_metadata=False, 
            delimiter="\t",
            always_update=False
            )
        self.day = day
        
    def _load_initial_data(self) -> pd.DataFrame: 
        """ Returns all data up to now and defines the data columns. 
        """
        return pd.read_csv(self.filepath, delimiter="\t", names=["Time", "VoltageDurationPower", "Coil"])
        
    def _load_new_data(self) -> pd.DataFrame: 
        """ Returns the rows which have not been loaded so far. 
        """
        return
    
    def _harmonize_time(self): 
        self._table_df["datetime"] = self._table_df["Time"].apply(lambda s: self.day + s).apply(pd.Timestamp)
        self._table_df["timestamp"] = self._table_df["Time"].apply(pd.Timestamp).values.astype(np.int64)


    
    
    
