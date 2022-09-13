# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 09:42:32 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

SSD Analysis -> Histogram
"""

import sys
sys.path.insert(0,'..')

import pandas as pd

from recorders.ssd_recorder import SSDRecorder
from analyses.analysis import Analysis
from analyses.peak_finder import PeakFinder
            

class SSDAnalysis(Analysis): 
    
    def __init__(self, filepath: str): 
        super(SSDAnalysis, self).__init__(SSDRecorder(filepath), filepath, "SSD Analysis") 
        self.peaks = []
        self.peak_finder = PeakFinder(self.recorder)
        self.peak_nr = 0
    
    def _run_analysis(self, df: pd.DataFrame):
        # 2D Histogram of PulsHeight vs Timestamp [Full view]
        fig = self._plot_2d_hist(
            df=df,
            x_column="timestamp",
            y_column="PulseHeight"
            )
        self.save(fig, "SSD_Hist2D")
        fig.show()
        
        # 1D Histogram of Peaks [Zoomed view]
        peaks = self.peak_finder.get_new_peaks()
        for peak in peaks:
            self.peak_nr += 1
            peak.plot(f"Peak_{self.peak_nr}.png")
        
        return
 
    
if __name__ == '__main__': 
    
    ssd_analysis = SSDAnalysis(filepath="../../data/20220829/-20220829-144945-Slot1-In1.csv")
    ssd_analysis.run()

