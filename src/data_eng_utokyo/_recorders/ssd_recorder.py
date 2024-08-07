# -*- coding: utf-8 -*-
"""Records the SSD data.

Applicable for data from the WE7000 DAQ for the SSD2. The PMT current from the MOT will be obtained like this in our
next experiment.
"""

import csv
import numpy as np
import pandas as pd

from .recorder import Recorder


class SSDRecorder(Recorder): 
    """Records all the SSD2 data at once.

    Note:
        * In most cases, there is too much data incoming at once. In this case, we recommend to use the SSDParser, which
            reads the data in chunks.
    """

    def __init__(self, filepath: str, always_update: bool=False, lines_per_update: int=1e5):
        super(SSDRecorder, self).__init__(
            filepath=filepath, 
            has_metadata=True, 
            always_update=always_update,
            )
        self.nr_meta_data_rows = 37
        self.lines_per_update = lines_per_update
        self.loaded_everything = False
        
    def is_up_to_date(self) -> bool:
        return all((
            self.last_updated == self._get_mod_time(),
            self.loaded_everything
            ))
            
    def _load_initial_data(self) -> pd.DataFrame: 
        return self._load_new_data()

    def _load_new_data(self) -> pd.DataFrame: 
        """ Just load the new part. """
        df = pd.read_csv(
            filepath_or_buffer=self.filepath, 
            skiprows=self.nr_meta_data_rows + self.read_data_lines, 
            header=0, 
            nrows=self.lines_per_update, 
            names=["TraceName", "Time_x", "PulseHeight"]
            )     
        nrows = len(df.index)
        self.loaded_everything = nrows < self.lines_per_update
        return df

    def _load_metadata(self): 
        """ Overwrite the metadata with the new version. """
        with open(self.filepath, newline='') as f:
            reader = csv.reader(f)
            metadata = []
            for i in range(self.nr_meta_data_rows + 1):
                metadata.append(next(reader))
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
        
        
class SSDParser(SSDRecorder): 
    """Records the SSD data in chunks.

    Acts as a parser in the sense that it forgets about the old data upon reloading. This keeps the table size small.
    """
    
    def _update_data(self):
        new_data_df = self._load_new_data()
        self.read_data_lines += len(new_data_df.index)
        if len(new_data_df.index) > 0: 
            self._data_df = new_data_df
    
        
        
