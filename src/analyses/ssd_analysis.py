# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 09:42:32 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

SSD Analysis -> Histogram
"""

import sys
sys.path.insert(0,'..')

from recorders.ssd_recorder import SSDRecorder
from analyses.analysis import Analysis
    

class SSDAnalysis(Analysis): 
    
    def __init__(self, filepath: str): 
        super(SSDAnalysis, self).__init__(SSDRecorder, filepath, "SSD Analysis") 
    
    def run(self): 
        df = self.recorder.get_table()
        
        self._plot_2d_hist(
            df=df, 
            setting="",
            x_column="timestamp", 
            y_column="PulseHeight", 
            x_bin_nr=100, 
            y_bin_nr=100
            )
        self._plot_1d_hist(x_column="timestamp", x_bin_nr=100) 
        return

    
if __name__ == '__main__': 
    
    ssd_analysis = SSDAnalysis(filepath = "../../data/sample/-20220314-100806-Slot1-In2.csv")
    ssd_analysis.run()
