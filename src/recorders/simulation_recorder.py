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

from recorders.recorder import Recorder


class SimulationRecorder(Recorder): 
    
    
    def __init__(self, filepath: str):
        super(SimulationRecorder, self).__init__(filepath, True)
    
    def _load_new_data(self) -> pd.DataFrame:  
        pass
    
    def _load_metadata(self): 
        pass
    
    def _harmonize_time(self): 
        pass