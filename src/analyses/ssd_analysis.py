# -*- coding: utf-8 -*-
"""SSD Analysis -> Visualizes the pulses and peaks in the pulses.

Note: The SSDAnalysis works with the SSDParser instead of the usual SSDRecorder,
which means that each time we perform ssd_analysis.run(), only the next 
10^5 pulses are analyzed. Using the SSDRecorder is not recommended, as it would
load to many pulses for the analysis. 

One can use the Runner to conveniently process the full data in real time. 
This allows us to get visualizations for all peaks. 
"""

import sys
sys.path.insert(0,'../..')  # Set src as top-level

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md
import pandas as pd
import datetime as dt
import queue

import src.constants.constants as c
from src.recorders.ssd_recorder import SSDRecorder, SSDParser
from src.recorders.file_recorder import FileParser
from src.analyses.analysis import Analysis, ResultParameter
from src.analyses.peak_finder import PeakFinder
from src.analyses.mkdir import mkdir_if_not_exist


plt.rcParams.update(c.plotting_params)
            

class SSDAnalysis(Analysis): 
    
    def __init__(self, 
                 recorder: SSDRecorder or SSDParser,
                 result_param: ResultParameter):
        super(SSDAnalysis, self).__init__(
            recorder=recorder, 
            name="SSD Analysis",
            result_param=result_param
            ) 
        self.peak_finder = PeakFinder(self.recorder)
        self.peak_nr = 0
        self.run_nr = 0
        self.result_df = None
    
    def _run_analysis(self, df: pd.DataFrame):
        # 2D Histogram of PulsHeight vs Timestamp [Full view]
        fig = self._plot_2d_hist(
            df=df,
            x_column="timestamp",
            y_column="PulseHeight"
            )
        self._save_fig(fig, f"SSD_Overview_2D_{self.run_nr}")
        fig.show()
        
        # Find peaks
        peaks, metadata = self.peak_finder.get_new_peaks(df)
        if not peaks: 
            return
        
        # 1D Histogram of Peaks [Full view]
        fig = self._plot_overview(metadata)
        self.run_nr += 1
        self._save_fig(fig, f"SSD_Overview_1D_{self.run_nr}")
        plt.show()
        
        # 1D Histogram of all Peaks [Zoomed view]
        for peak in peaks:
            self.peak_nr += 1
            peak.plot(self.image_src + f"SSD_Peak_{self.peak_nr}" + self.image_extension)
            
        # Combine new results to df
        new_result_df = self._get_new_result_df(peaks)
        
        # Save or append the new results to csv
        self._save_results(new_result_df)
        
        # Update the result df with the new results
        self._update_result_df(new_result_df)
            
        # Perform analysis on result df
        self._analyze_results()
    
        return self.result_df
    
    def _plot_overview(self, metadata):
        # Extract data
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
    
    def _ts_ns_to_timestamp(self, ts_list: list): 
        return [dt.datetime.fromtimestamp(ts // 1000000000) for ts in ts_list]
    
    def _get_new_result_df(self, peaks: list): 
        assert peaks, "In _SSDAnalysis._get_new_result_df() the input was None."
        peak_dfs = [peak.as_dataframe() for peak in peaks]
        return pd.concat(peak_dfs , ignore_index=True)
    
    def _update_result_df(self, new_result_df): 
        """ Updates the result table adding new peaks and results the part which
        """
        assert new_result_df is not None, "In _SSDAnalysis._update_result_df() the input was None."
        if self.result_df is None: 
            self.result_df = new_result_df
            return
        self.result_df = pd.concat([self.result_df, new_result_df], ignore_index=True)
        return 
            
    def _analyze_results(self): 
        pass
    
    
class SSDAnalysisWrapper(object):
    """Wrapper for the SSD Analysis.

    Solves the problem that we have many ssd csv file and not just one. 
    Keeps track of the csv files that match a certain pattern in a certain 
    timespan and applies the SSDAnalysis on them 1 by 1. 
    
    Implements the same public methods as the Analysis class, such that it can
    be used in Runner. 
    """
    
    def __init__(self, 
                 folder: str="", 
                 result_path: str="", 
                 plot_path: str="",
                 image_extension: str="",
                 match: str="",
                 time_interval: tuple=(
                     dt.datetime(2000, 1, 1, 12, 0, 0), 
                     dt.datetime(2030, 1, 1, 12, 0, 0)
                     )): 
        self.filepath_recorder = FileParser(
            filepath=folder, 
            match=match
            )
        self.result_path = result_path
        self.plot_path = plot_path
        self.image_extension = image_extension
        self.time_interval = time_interval
        self.filepath_queue = queue.Queue()
        self.active_analysis = None

    def run(self): 
        # Case: There is an active analysis
        if self.active_analysis is not None: 
            self.active_analysis.run()
            if self.active_analysis.is_up_to_date():
                self.active_analysis = None
                
        # Case: We start a new analysis
        self._update()
        if self.filepath_queue.empty(): 
            return
        
        # Get filepath 
        filepath = self.filepath_queue.get()
        
        # Create parameters and folders
        image_extension=self.image_extension
        result_filepath = self.result_path
        image_src= self.plot_path + f"{os.path.basename(filepath)}/" + "ssd/"
        mkdir_if_not_exist(self.plot_path)
        mkdir_if_not_exist(self.plot_path + f"{os.path.basename(filepath)}/")
        mkdir_if_not_exist(image_src)
        
        # Run analysis
        result_param = ResultParameter(
            image_src=image_src, 
            image_extension=image_extension,
            result_filepath=result_filepath+"ssd_analysis_results.csv"
            )
        self.active_analysis = SSDAnalysis(
            recorder=SSDParser(filepath),
            result_param=result_param
            )
        self.active_analysis.run()
        
    def is_up_to_date(self): 
        return self.filepath_queue.empty() and self.active_analysis == None
    
    def _update(self): 
        self._add_to_queue()
        
    def _add_to_queue(self): 
        # Check if necessary
        if self.filepath_recorder.is_up_to_date(): 
            return
        
        # Load new filepaths
        df = self.filepath_recorder.get_table()
        
        # Select filepaths from the right time
        start = self.time_interval[0]
        stop = self.time_interval[1]
        df = df[(start <= df.datetime) & (df.datetime <= stop)]
        
        # Stop if there are no new filepaths
        if len(df.index) == 0: 
            return 
        
        # Add filepaths to queue
        for filepath in df["filepath"]: 
            self.filepath_queue.put(filepath)
    
    
if __name__ == '__main__': 
    
    """
    ssd_analysis = SSDAnalysis(
        filepath="../../data/sample/-20220314-100806-Slot1-In2.csv",
        image_src="../../plots/20220314/ssd/",
        image_extension=".png",
        result_filepath="../../results/20220314/"+"ssd_analysis_results.csv"
        )
    ssd_analysis.run()
    """
    
    ssd_wrapper = SSDAnalysisWrapper(
        folder="../../data/sample/", 
        result_path="../../results/20220314/"+"ssd_analysis_results.csv",
        plot_path="../../plots/20220829/",
        image_extension=".png",
        match=".*Slot.*.csv",
        time_interval=(
            dt.datetime(2000, 1, 1, 12, 0, 0), 
            dt.datetime(2030, 1, 1, 12, 0, 0)
        ))
    ssd_wrapper.run()
    ssd_wrapper.run()
