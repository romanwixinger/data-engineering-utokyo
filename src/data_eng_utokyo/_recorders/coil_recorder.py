# -*- coding: utf-8 -*-
"""Tracks the whether the current of the MOT coil is on or off.

The current of the MOT coil is controlled by a relay switch. This text file is 
the log of the relay switch. 
"""

import numpy as np
import pandas as pd

from .recorder import Recorder


class CoilRecorder(Recorder): 
    """Tracks the whether the current of the MOT coil is on or off.
    
    Args: 
        filepath (str): Path to the text file.
        
    Attributes:
        filepath (str): Path to the text file.
        always_update (bool): Should the recorder always check for new data.
    """
       
    def __init__(self, filepath: str, always_update: bool=False):
        super(CoilRecorder, self).__init__(
            filepath=filepath, 
            has_metadata=False, 
            delimiter="	",
            always_update=always_update
            )
    
    def _harmonize_time(self): 
        """Reads the time from the text file and adds it to the table.
        """
        self._table_df["datetime"] = self._table_df["Time"]
        self._table_df["timestamp"] = self._table_df["Time"].apply(pd.Timestamp).values.astype(np.int64)
