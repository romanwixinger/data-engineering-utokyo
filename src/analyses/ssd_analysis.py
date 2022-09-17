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

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md
import pandas as pd
import datetime as dt

import constants as c
from recorders.ssd_recorder import SSDParser
from analyses.analysis import Analysis
from analyses.peak_finder import PeakFinder


plt.rcParams.update(c.plotting_params)
            

class SSDAnalysis(Analysis): 
    
    def __init__(self, filepath: str, 
                 image_src: str="../../plots/",  
                 image_extension: str=".png",
                 result_filepath: str="ssd_analysis_results.csv"):
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
        self.result_df = None
        self.result_filepath = result_filepath
    
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
            
        # Update result df
        new_result_df = self._get_new_result_df(peaks)
        self._update_result_df(new_result_df)
        
        # Save or append to csv file
        self._save(new_result_df)
            
        # Perform analysis on all results
        self._analyze_results()
    
        return self.result_df
    
    def _plot_overview(self, metadata):
        timestamps = metadata["timestamps"]
        pulse_rates = metadata["pulse_rates"] # Convert [1/ns] to [1/s]
        peak_timestamps = metadata["peak_timestamps"]
        
        # Convert units
        timestamps = self._ts_ns_to_timestamp(timestamps)
        peak_timestamps = self._ts_ns_to_timestamp(peak_timestamps)
        pulse_rates = [pr * 1e9 for pr in pulse_rates]  # Convert [1/ns] to [1/s]
        
        # Plot pulse rates
        fig, ax = plt.subplots(figsize=(10, 7))
        plt.plot(timestamps, pulse_rates, label="SSD pulses")
        
        # Plot peaks
        if len(peak_timestamps) > 0: 
            plt.axvline(x=peak_timestamps[0], color='r', ls='--', lw=1, label="Peak")
        if len(peak_timestamps) > 1: 
            for ts in peak_timestamps[1:]: 
                plt.axvline(x=ts, color='r', ls='--', lw=1)
        
        # Timestamp of x-axis
        minute = 60 * 1000000000 
        min_ts = np.min(metadata["timestamps"]) - (np.min(metadata["timestamps"]) % minute)
        max_ts = np.max(metadata["timestamps"]) - (np.max(metadata["timestamps"]) % minute)
        stepsize = minute * int((max_ts - min_ts) / minute / 15 + 1)
        ts_list = np.arange(min_ts, max_ts + 2 * minute, stepsize)
        timestamps_list = self._ts_ns_to_timestamp(ts_list)
        ax.xaxis.set_ticks(timestamps_list)
        xfmt = md.DateFormatter('%H:%M')
        ax.xaxis.set_major_formatter(xfmt)
        plt.xticks(rotation=25)
            
        # Add labels
        plt.title("Peaks in the pulse rate from the SSD")
        plt.xlabel("Time [H:M]")
        plt.ylabel("Pulse rate [Hz]")
        ax.legend()
        
        return fig
    
    def _ts_ns_to_timestamp(self, ts_list: list[int]): 
        return [dt.datetime.fromtimestamp(ts // 1000000000) for ts in ts_list]
    
    def _get_new_result_df(self, peaks: list): 
        if not peaks: 
            return None
        peak_dfs = [peak.as_dataframe() for peak in peaks]
        return pd.concat(peak_dfs , ignore_index=True)
    
    def _update_result_df(self, new_result_df): 
        """ Updates the result table adding new peaks and results the part which
        """
        if new_result_df is None:
            return 
        if self.result_df is None: 
            self.result_df = new_result_df
            return
        self.result_df = pd.concat([self.result_df, new_result_df], ignore_index=True)
        return self.result_df
    
    def _save(self, new_result_df: pd.DataFrame): 
        """ Create if not exists else append. """
        if os.path.exists(self.result_filepath): 
            new_result_df.to_csv(self.result_filepath, mode="a", index=False, header=False)
        else: 
            new_result_df.to_csv(self.result_filepath, mode="w", index=False, header=True)
            
    def _analyze_results(self): 
        pass
    
    
if __name__ == '__main__': 
    
    ssd_analysis = SSDAnalysis(
        filepath="../../data/20220829/-20220829-144945-Slot1-In1.csv",
        image_src="../../plots/",
        image_extension=".png"
        )
    ssd_analysis.run()

