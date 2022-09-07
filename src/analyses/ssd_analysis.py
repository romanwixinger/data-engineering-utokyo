# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 09:42:32 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

SSD Analysis -> Histogram
"""

import sys
sys.path.insert(0,'..')

import numpy as np
import matplotlib.pyplot as plt

from constants import loc
from recorders.ssd_recorder import SSDRecorder
from analyses.analysis import Analysis
    

class SSDAnalysis(Analysis): 
    
    def __init__(self, filepath: str): 
        super(SSDAnalysis, self).__init__(SSDRecorder, filepath, "SSD Analysis") 
    
    def run(self): 
        self._plot_2d_hist()
    
    def _plot_2d_hist(self): 
        # Load data
        ssd_df = self.recorder.get_table()
        x = ssd_df["timestamp"]
        y = ssd_df["PulseHeight"]
        
        # Prepare parameters
        x_min = np.min(x)
        x_max = np.max(x)
        y_min = np.min(y)
        y_max = np.max(y)
        nx = np.linspace(x_min, x_max, len(x) // 50)
        ny = np.linspace(y_min, y_max, 100)
        
        print(nx)
        print(ny)
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 7))
        plt.hist2d(x, y, bins=(nx, ny), range=None, density=False, weights=None, cmin=None, cmax=None)
        
        # Add descriptions
        plt.title("2D Histogram of PulseHeight against Time.")
        ax.set_xlabel('Time') 
        ax.set_ylabel('PulseHeight') 

        return 
    
    
ssd_analysis = SSDAnalysis(filepath = "../../data/sample/-20220314-100806-Slot1-In2.csv")
ssd_analysis.run()
