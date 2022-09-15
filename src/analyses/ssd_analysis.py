# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 09:42:32 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

SSD Analysis -> Visualizes the pulses and peaks in the pulses. 

Note: The SSDAnalysis works with the SSDParser instead of the usual SSDRecorder,
which means that each time we perform ssd_analysis.run(), only the next 
10^5 pulses are analyzed. Using the SSDRecorder is not recommended, as it would
load to many pulses for the analysis. 

One can use the Runner to conveniently process the full data in real time. 
This allows us to get visualizations for all peaks. 
"""

import sys
sys.path.insert(0,'..')

import matplotlib.pyplot as plt
import pandas as pd

from recorders.ssd_recorder import SSDParser
from analyses.analysis import Analysis
from analyses.peak_finder import PeakFinder
            

class SSDAnalysis(Analysis): 
    
    def __init__(self, filepath: str, 
                 image_src: str="../../plots/",  
                 image_extension: str=".png"):
        super(SSDAnalysis, self).__init__(
            recorder=SSDParser(filepath), 
            filepath=filepath, 
            name="SSD Analysis",
            image_src=image_src, 
            image_extension=image_extension
            ) 
        self.peaks = []
        self.peak_finder = PeakFinder(self.recorder)
        self.peak_nr = 0
        self.run_nr = 0
    
    def _run_analysis(self, df: pd.DataFrame):
        # 2D Histogram of PulsHeight vs Timestamp [Full view]
        fig = self._plot_2d_hist(
            df=df,
            x_column="timestamp",
            y_column="PulseHeight"
            )
        self.save(fig, "SSD_Hist2D")
        fig.show()
        
        # Find peaks
        peaks, metadata = self.peak_finder.get_new_peaks(df)
        if not peaks: 
            return
        
        # 1D Histogram of Peaks [Full view]
        fig = self._plot_overview(metadata)
        self.run_nr += 1
        fig.savefig(fname=f"../../plots/Overview_all_peaks_{self.run_nr}.png")
        plt.show()
        
        # 1D Histogram of all Peaks [Zoomed view]
        for peak in peaks:
            self.peak_nr += 1
            peak.plot(self.image_src + f"Peak_{self.peak_nr}" + self.image_extension)
    
        return
    
    def _plot_overview(self, metadata):
        timestamps = metadata["timestamps"]
        pulse_rates = metadata["pulse_rates"]
        peak_timestamps = metadata["peak_timestamps"]
        
        fig, ax = plt.subplots(figsize=(10, 7))
        plt.plot(timestamps, pulse_rates)
        for ts in peak_timestamps: 
            plt.axvline(x=ts, color='r', ls='--', lw=1)
        return fig
 
    
if __name__ == '__main__': 
    
    ssd_analysis = SSDAnalysis(
        filepath="../../data/20220829/-20220829-144945-Slot1-In1.csv",
        image_src="../../plots/",
        image_extension=".png"
        )
    ssd_analysis.run()

