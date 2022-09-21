# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 16:35:17 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Keeps track of the available files. Use cases include the image data from the 
CMOS camera and the SSD data. 
"""


import sys
sys.path.insert(0,'..')

import os
import pandas as pd
from datetime import datetime
from pathlib import Path

from recorders.recorder import Recorder
from analyses.path_helper import PathHelper 


class FileRecorder(Recorder): 
    
    def __init__(self, filepath: str, always_update: bool=False, match: str=""):
        super(FileRecorder, self).__init__(
            filepath=filepath, 
            has_metadata=False, 
            always_update=always_update
            )
        self.match = match
        self.filepath_set = set()

    def _load_initial_data(self) -> pd.DataFrame: 
        """ Returns all data (filepath and metadata of images) which are new. 
        """
        return self._load_new_data()
        
    def _load_new_data(self) -> pd.DataFrame: 
        """ Returns all data (filepath and metadata of images) which are new. 
        """

        # Generate filepaths and add them to loaded
        filepaths = PathHelper.get_filepaths(folder=self.filepath, match=self.match)
        new_filepaths = set(filepaths) - self.filepath_set
        
        # Check if we have new filepaths (should always be the case!)
        if len(new_filepaths) == 0: 
            print("Do not call this function if there is no need for it!")
            return pd.DataFrame()
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
    
    def _load_metadata(self) -> pd.DataFrame: 
        """ Reloads all metadata. 
        """
        return pd.DataFrame()
    
    def _harmonize_time(self): 
        self._table_df["timestamp"] = self._table_df["ctime"].apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S.%f'))
        self._table_df["datetime"] =  self._table_df["timestamp"].apply(pd.Timestamp)
       
        
class FileParser(FileRecorder):
    """ Like the ImageRecorder but on each evaluation of get_table(), 
        the parser forgets the old data and just returns the new one. 
    """
    
    def _update_data(self):
        new_data_df = self._load_new_data()
        self.read_data_lines += len(new_data_df.index)
        self._data_df = new_data_df
        self.last_updated = self._get_mod_time()
        
    def is_up_to_date(self) -> bool:
        all_filepaths = PathHelper.get_filepaths(folder=self.filepath, match=self.match)
        return len(self.filepath_set) == len(all_filepaths) 

    
if __name__ == '__main__': 
    
    # Settings
    folder = "C:\\Users\\roman\\Desktop\\Research_UTokyo\\Data\\mot"
    match = ".*ccd_detuning.*.xlsx"
    
    image_recorder = FileParser(filepath=folder, match=match)
    df = image_recorder.get_table()
    for col in df.columns: 
        print(col, df[col])
    
