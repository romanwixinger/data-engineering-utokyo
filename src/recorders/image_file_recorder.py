# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 10:38:16 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Keeps track of the available image files online on Google Colab. This version
solves the problem that online the images have new creation times, so we cannot
rely on it. Instead, we look the timestamp up in the metadata file 
all_data.csv which is located in the next-higher folder. Then we match them 
according to the number. 
"""

import sys
sys.path.insert(0,'../..')  # Set src as top-level

import os
import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path

from src.recorders.recorder import Recorder
from src.analyses.path_helper import PathHelper 


class ImageFileRecorder(Recorder): 
    """ Variation of the FileRecorder which works online of Google Colab. 
        It just works for camera images (.csv), because they contain a metadata
        file (all_data.csv) in the next-higher folder. This metadata file 
        allows us to read of the timestamp. 
    """
    
    def __init__(self, filepath: str, always_update: bool=False, match: str=""):
        super(ImageFileRecorder, self).__init__(
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
        
        rows = []

        # Get the folder paths which contain the desired files
        folders = PathHelper.get_folders(folder=self.filepath, match=self.match)
        
        # Create a list of tuples (filepath, timestamp, ROI Sum,Coil (1:ON 0:OFF)) using the metadata
        for folder in folders: 
            
            # Create metadata lookup
            metadata_filepath = folder + "\\all_data.csv"
            assert os.path.isfile(metadata_filepath), f"Expected metadata file at {metadata_filepath}, but did not find it."
            metadata_df = Recorder(filepath=metadata_filepath,
                                   has_metadata=False).get_table()
            metadata_lookup = {
                row["No."]: [row["Time"], row["ROI Sum"], row["Coil (1:ON 0:OFF)"]]\
                    for index, row in metadata_df.iterrows()
                }
                
            # Get filepaths
            filepaths = PathHelper.get_filepaths(folder=folder, match=self.match)
            rows = rows + [
                [Path(fp).stem, fp, os.path.basename(fp)]\
                + metadata_lookup[self._filepath_to_nr(fp)]\
                for fp in filepaths
                ]
            
        # Construct df
        columns = ["filename", "filepath", "filename_with_extension", "Time", "ROI Sum", "Coil (1:ON 0:OFF)"]
        return pd.DataFrame(data=rows, columns=columns)
    
    def _load_metadata(self) -> pd.DataFrame: 
        """ Reloads all metadata. 
        """
        return pd.DataFrame()
    
    def _harmonize_time(self): 
        self._table_df["timestamp"] = self._table_df["Time"].apply(pd.Timestamp).values.astype(np.int64)
        self._table_df["datetime"] =  self._table_df["Time"].apply(pd.Timestamp)
        
        
    def _filepath_to_nr(self, fp: str): 
        """ Takes something of the form "...cmos_000043.csv" and returns 43."""
    
        nr_with_zeros = fp[-10:-4]
        nr = nr_with_zeros.lstrip("0")
        return int(nr)
    

if __name__ == '__main__': 
    
    # Settings
    folder = "C:\\Users\\roman\\Desktop\\Research_UTokyo\\Code\\data-engineering-utokyo\\data\\beamtime\\mot_data\\"
    match = ".*cmos.*.csv"
    
        
    image_file_recorder = ImageFileRecorder(filepath=folder, match=match)
    df = image_file_recorder.get_table()