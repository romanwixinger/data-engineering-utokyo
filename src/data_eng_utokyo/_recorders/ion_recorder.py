# -*- coding: utf-8 -*-
"""Records the log of the Fr ion source.

On the first day of experiment, right after the end of primary beam check, just starting the Fr ion extraction.
The column "FC" is the current from either one of the faraday cups, or the sum of both. The columns "Center" and
"Surrounding" are the voltages applied to the mechanical relay switches that connects the faraday cups to the
picoammeter. For example, if "Center" = 24 and "Surrounding" = 0, the value at "FC" is the current observed on FC Center
in nA.

Todo:
    * Check the usage of abstractmethods.
"""

import numpy as np
import pandas as pd

from .recorder import Recorder


class IonRecorder(Recorder): 
    
    def __init__(self, filepath: str, always_update: bool=False):
        super(IonRecorder, self).__init__(
            filepath=filepath, 
            has_metadata=False, 
            always_update=always_update,
            encoding='Shift-JIS'
            )

    def _harmonize_time(self): 
        self._table_df["datetime"] = pd.to_datetime(self._table_df["Timestamp"])
        self._table_df["timestamp"] = self._table_df["datetime"].values.astype(np.int64)