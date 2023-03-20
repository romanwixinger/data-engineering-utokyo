# -*- coding: utf-8 -*-
"""Keeps track of the available files with a specific filename format.

Use cases include the image data from the CMOS camera and the SSD data. 
"""

import os
import pandas as pd
from datetime import datetime
from pathlib import Path

from .recorder import Recorder
from .._utilities.path_helper import PathHelper


class FileRecorder(Recorder): 
    """Tracks the filenames which match a format in a specific folder.
        
    Args:
        filepath (str): Path to the folder in which the files are stored.
        always_update (bool): Should the recorder always check for new data.
        match (str): Regex with which the filenames are compared. Only matching
            strings are tracked.

    Attributes:
        filepath (str): Path to the folder in which the files are stored.
        always_update (bool): Should the recorder always check for new data.
        match (str): Regex with which the filenames are compared. Only matching
            strings are tracked.
        filepath_set (set): Set of filepaths that were found.
    """
    
    
    def __init__(self, filepath: str, always_update: bool=False, match: str=""):
        super(FileRecorder, self).__init__(
            filepath=filepath, 
            has_metadata=False, 
            always_update=always_update
            )
        self.match = match
        self.filepath_set = set()

    def _load_initial_data(self) -> pd.DataFrame: 
        """Gets all data (filepath and metadata of images).
        
        Returns: 
            Data as a pandas dataframe.
        """
        return self._load_new_data()
        
    def _load_new_data(self) -> pd.DataFrame: 
        """Gets all data (filepath and metadata of images) which are new. 
        
        Returns: 
            New data as a pandas dataframe.
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
        """Reloads all metadata. 
        
        Returns: 
            Empty dataframe. There is no metadata.
        """
        return pd.DataFrame()
    
    def _harmonize_time(self):
        """Reads the time and adds it to the table.
        """
        self._table_df["timestamp"] = self._table_df["ctime"].apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S.%f'))
        self._table_df["datetime"] =  self._table_df["timestamp"].apply(pd.Timestamp)
       
        
class FileParser(FileRecorder):
    """Works like the FileRecorder, but just returns new data each time.
    
    Note: 
        The parser forgets the old data and just returns the new one. It is 
        convenient when we want to laod many files in chunks. We can just call
        the FileParser multiple times, and each time it tells us which files
        we should load.
        
    Args:
        filepath (str): Path to the folder in which the files are stored.
        always_update (bool): Should the recorder always check for new data.
        match (str): Regex with which the filenames are compared. Only matching
            strings are tracked.

    Attributes:
        filepath (str): Path to the folder in which the files are stored.
        always_update (bool): Should the recorder always check for new data.
        match (str): Regex with which the filenames are compared. Only matching
            strings are tracked.
        filepath_set (set): Set of filepaths that were found.
    """
    
    def _update_data(self):
        """Loads new data.
        """
        new_data_df = self._load_new_data()
        self.read_data_lines += len(new_data_df.index)
        self._data_df = new_data_df
        self.last_updated = self._get_mod_time()
        
    def is_up_to_date(self) -> bool:
        """Returns whether all data has already been returned.
        """
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
    
