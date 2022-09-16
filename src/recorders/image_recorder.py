# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 16:35:17 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Keeps track of the available image data from the SSD and the corresponding 
metadata. 
"""


import sys
sys.path.insert(0,'..')

import os
import pandas as pd
from datetime import datetime
from pathlib import Path

from recorders.recorder import Recorder
from analyses.path_helper import PathHelper 


class ImageRecorder(Recorder): 
    
    def __init__(self, filepath: str, always_update: bool=False, match: str=".*ccd_detuning.*.xlsx"):
        super(ImageRecorder, self).__init__(
            filepath=filepath, 
            has_metadata=False, 
            always_update=always_update
            )
        self.match = match
        self.filepath_set = set()

    def _load_initial_data(self) -> pd.DataFrame: 
        """ Returns all data (filepath and metadata of images) which are new. 
        """
        # Generate filepaths and add them to loaded
        filepaths = PathHelper.get_filepaths(folder=self.filepath, match=self.match)
        new_filepaths = set(filepaths) - self.filepath_set
        self.filepath_set = self.filepath_set | new_filepaths
        
        # Load metadata and create table
        columns = ["filename", "filename_with_extension", "filepath", "mtime", "ctime"]
        funcs = [lambda x: Path(x).stem, 
                os.path.basename, 
                 lambda x: x, 
                 os.path.getmtime, 
                 os.path.getctime]
        rows = [list(func(path) for func in funcs) for path in new_filepaths]
        return pd.DataFrame(data=rows, columns=columns)
        
    def _load_new_data(self) -> pd.DataFrame: 
        """ Returns all data (filepath and metadata of images) which are new. 
        """

        return self._load_initial_data()
        
    def _load_metadata(self) -> pd.DataFrame: 
        """ Reloads all metadata. 
        """
        return pd.DataFrame()
    
    def _harmonize_time(self): 
        self._table_df["timestamp"] = self._table_df["ctime"].apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S.%f'))
        self._table_df["datetime"] =  self._table_df["timestamp"].apply(pd.Timestamp)
        self._table_df["datetime_μs"] = self._table_df["datetime"]
        self._table_df["datetime_ms"] = self._table_df["datetime"].apply(lambda s: str(s)[:-3])
       
    
if __name__ == '__main__': 
    
    # Settings
    folder = "C:\\Users\\roman\\Desktop\\Research_UTokyo\\Data\\mot"
    match = ".*ccd_detuning.*.xlsx"
    
    image_recorder = ImageRecorder(filepath=folder, match=match)
    df = image_recorder.get_table()
    for col in df.columns: 
        print(col, df[col])
    
