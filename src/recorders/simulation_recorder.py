# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 14:08:56 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

The Simulation Recorder can be used for simulating how the system would behave 
for a recorder which generates a certain amount of data from the csv file. 
The main goal is to benchmarks the analysis system by simulating a recorder 
which creates big amounts of data. 
"""

import sys
sys.path.insert(0,'..')


import pandas as pd
import time

from recorders.recorder import Recorder


class SimulationRecorder(Recorder): 
    """ Recorder which simulates reading a certain number of new lines each 
        period from a csv with a certain number of columns. 
    """
    
    def __init__(self, filepath: str, newlines_per_s: int, columns):
        super(SimulationRecorder, self).__init__(filepath, False)
        self.newlines_per_s = newlines_per_s
        self.rows = 5 * self.newlines_per_s
        self.columns = columns
        self._setup_csv() 
        self.last_load = time.time()
    
    def _load_new_data(self) -> pd.DataFrame:  
        time_diff = time.time() - self.last_load
        self.last_load = time.time()        
        nrows = int(time_diff * self.newlines_per_s)
        nrows = min(nrows, self.rows)
        nrows = max(nrows, 1)
        df = pd.read_csv(self.filepath, nrows=nrows)
        self.read_data_lines += len(df.index)
        print(len(df.index))
        return df
    
    def _load_metadata(self): 
        return None
    
    def _harmonize_time(self): 
        return
    
    def table_is_up_to_date(self) -> bool: 
        return False
    
    def _setup_csv(self): 
        """ Generates a big csv file on init, such that we can perform a real
            read operation in the other methods. 
        """
        data=[i for i in range(self.rows)]
    
        dfs = [pd.DataFrame(data=data, columns=[f"col_{j}"]) for j in range(self.columns)]
        dfs = dfs + [pd.DataFrame(data=[time.time() for i in range(self.rows)], columns=["timestamp"])]
        df = pd.concat(dfs, axis=1)
        df.to_csv(self.filepath)
        return
      