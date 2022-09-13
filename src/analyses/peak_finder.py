# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 12:32:22 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Finds peaks in the SSD pulse data. 
"""

import sys
sys.path.insert(0,'..')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from analyses.peak import Peak
        
    
class PeakFinder(object): 
    """ Class for finding peaks in the SSD data, which come from the release
        of many atoms by heating the Yttrium. 
    """
    
    def __init__(self, recorder, plot_filename: str=""): 
        self.recorder = recorder
        self.peaks = []
        
        # Settings
        self.window_size = 500              # [1]
        self.min_new_pulses = 1600          # [1]
        self.min_distance = 3.0e10          # [ns]
        self.look_backward_from_peak = 1e9  # [ns]
        self.look_forward_from_peak = 3e9   # [ns]
        self.discard_rate = 12              # [int] 
    
        # Bookkeeping 
        self.processed_up_to = 0    # [ns]
        
        # Background calculation
        self.start_timestamp = None # [ns]
        self.nr_of_pulses = 0       # [1]
        self.background = 0         # [1/ns]
    
    def get_new_peaks(self) -> list[Peak]: 
        """ Loads the new data, estimates the background, finds the peaks and
            returns them. 
        """
        new_df = self._load_new_data()
        self._calculate_new_background(new_df)
        peak_timestamps = self._find_peaks(new_df) 
        peaks = self._generate_peaks(new_df, peak_timestamps)
        self.peaks += peaks
        return peaks
            
    def _load_new_data(self) -> pd.DataFrame: 
        """ Load the part of the data which has not been processed yet. 
        """
        df = self.recorder.get_table()
        new_df = df[df.timestamp >= self.processed_up_to]
        if self.start_timestamp is None: 
            self.start_timestamp = np.min(new_df.timestamp)
        self.processed_up_to = np.max(new_df.timestamp)
        return new_df

    def _calculate_new_background(self, new_df: pd.DataFrame):
        """ Update the estimation of the background based on the new data. 
        """
        self.nr_of_pulses += len(new_df.index)
        self.start_timestamp = min(new_df) if self.start_timestamp is None else self.start_timestamp
        assert self.processed_up_to > self.start_timestamp, "Beginning should be before the end."
        self.background = self.nr_of_pulses / (self.processed_up_to - self.start_timestamp)
        
    def _find_peaks(self, new_df: pd.DataFrame) -> list[int]:
        """ Uses a sliding window approach to find times (peaks) in which many
            signals were recorded. Returns the peaks as a list of timestamps. 
        """
        
        # Input validation
        timestamps = new_df["timestamp"]
        n = len(timestamps)
        if n <= self.min_new_pulses: 
            return []
        
        # Sliding window 
        time_diffs = [fast - slow for slow, fast in zip(timestamps, timestamps[self.window_size:])] # [ns]
        pulse_rates = [self.window_size / time_diff for time_diff in time_diffs]                     # [1/ns]
    
        # Find peaks as timestamps
        peak_timestamps = self._find_peaks_in_1d_array(pulse_rates, timestamps[:-self.window_size])
        
        # Plot peaks
        fig, ax = plt.subplots(figsize=(10, 7))
        plt.plot(timestamps[:-self.window_size], pulse_rates)
        for ts in peak_timestamps: 
            plt.axvline(x=ts, color='r', ls='--', lw=1)
        fig.savefig(fname="Overview_all_new_peaks.png")
        plt.show()
        
        return peak_timestamps
        
    def _find_peaks_in_1d_array(self, array: list[float], timestamps: list[int]): 
        """ Takes the array and finds local maxima which have at least a 
            certain time difference. 
        """
        
        assert(len(array) == len(timestamps))
        
        # Sort arrays together according the the first array in descending order
        array_sorted, timestamps_sorted = zip(*sorted(
            zip(array, timestamps), key=lambda x: x[0], reverse=True)
            )
        
        # Throw away the small values, as they cannot be peaks
        n = len(array_sorted)
        array_sorted = array_sorted[:n//self.discard_rate]
        timestamps_sorted = timestamps_sorted[:n//self.discard_rate]
        
        # Build list of maxima
        peaks = [array_sorted[0]]
        peak_timestamps = [timestamps_sorted[0]]
        for x, ts in zip(array_sorted[1:], timestamps_sorted[1:]):
            if all((abs(ts - peak_ts) > self.min_distance for peak_ts in peak_timestamps)): 
                peaks.append(x)
                peak_timestamps.append(ts)
                
        return peak_timestamps
    
    def _generate_peaks(self, df: pd.DataFrame, peak_timestamps: list[int]) -> list[Peak]:
        """
        Takes the new data and a list of the timestamps of the new peaks, and
        builds a list of the Peak instances. 
        """
        
        peaks = []
        for ts in peak_timestamps:
            events = df[(df.timestamp >= ts-self.look_backward_from_peak)\
                      & (df.timestamp <= ts+self.look_forward_from_peak)]["timestamp"]
            peak = Peak(
                timestamp=ts, 
                events=events,
                background=self.background
                )
            peaks.append(peak)
        return peaks
            