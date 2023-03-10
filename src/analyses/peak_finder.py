# -*- coding: utf-8 -*-
"""Finds peaks in the SSD pulse data.
"""

import sys
sys.path.insert(0,'../..')  # Set src as top-level

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.analyses.peak import Peak
        
    
class PeakFinder(object): 
    """ Class for finding peaks in the SSD data, which come from the release
        of many atoms by heating the Yttrium. 
    """
    
    def __init__(self, recorder, plot_filename: str=""): 
        self.recorder = recorder
        self.peaks = []
        
        # Settings
        self.window_size = 800              # [1]
        self.min_new_pulses = 500           # [1]
        self.min_distance = 3.0e10          # [ns]
        self.look_left = 1e9                # [ns]
        self.look_right = 3e9               # [ns]
        self.search_radius = 6e9            # [ns]
        self.discard_rate = 5               # [int] 
        self.min_pulses_for_peak = 6        # [int]
    
        # Bookkeeping 
        self.processed_up_to = 0            # [ns]
        self.max_peaks_per_run = 20         # [1]
        self.max_pulses_per_run = 360*1000  # [1]
        
        # Background calculation
        self.start_timestamp = None         # [ns]
        self.nr_of_pulses = 0               # [1]
        self.background = 0                 # [1/ns]
    
    def get_new_peaks(self, df) -> list: 
        """ Loads the new data, estimates the background, finds the peaks and
            returns them. 
        """
        new_df = self._get_new_data(df)
        self._calculate_new_background(new_df)
        peak_timestamps, metadata = self._find_peaks(new_df) 
        peaks = self._generate_peaks(new_df, peak_timestamps)
        self.peaks += peaks
        return peaks, metadata
            
    def _get_new_data(self, df) -> pd.DataFrame: 
        """ Returns the part of the data which has not been processed yet. 
        """
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
        
    def _find_peaks(self, new_df: pd.DataFrame) -> list:
        """ Uses a sliding window approach to find times (peaks) in which many
            signals were recorded. Returns the peaks as a list of timestamps. 
        """
        
        # Input validation
        timestamps = new_df["timestamp"]
        n = len(timestamps)
        if n <= self.min_new_pulses: 
            return [], {}
        
        # Sliding window 
        time_diffs = [fast - slow for slow, fast in zip(timestamps, timestamps[self.window_size:])] # [ns]
        pulse_rates = [self.window_size / time_diff for time_diff in time_diffs]                     # [1/ns]
    
        # Find peaks as timestamps
        peak_timestamps = self._find_peaks_in_1d_array(pulse_rates, timestamps[:-self.window_size])
        
        # Optimize their position
        peak_timestamps = self._optimize_position(new_df, peak_timestamps)
        
        # Verify peaks
        peak_timestamps = [ts for ts in peak_timestamps if self._is_peak(new_df, ts)]
        
        # Plot peaks
        metadata = {
            "timestamps": timestamps[:-self.window_size],
            "pulse_rates": pulse_rates,
            "peak_timestamps": peak_timestamps
            }
        
        return peak_timestamps, metadata
        
    def _find_peaks_in_1d_array(self, array: list, timestamps: list): 
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
        peaks_found = 1
        for x, ts in zip(array_sorted[1:], timestamps_sorted[1:]):
            if all((abs(ts - peak_ts) > self.min_distance for peak_ts in peak_timestamps)): 
                peaks_found += 1
                peaks.append(x)
                peak_timestamps.append(ts)
                if peaks_found == self.max_peaks_per_run: 
                    break
                
        return peak_timestamps
    
    def _optimize_position(self, df: pd.DataFrame, peak_timestamps: list) -> list: 
        optimized_peaks = []
        for ts in peak_timestamps: 
            search_df = df[(df.timestamp >= ts-self.search_radius)\
                      & (df.timestamp <= ts+self.search_radius)]
            peak_ts = self._find_maximum(search_df)
            optimized_peaks.append(peak_ts)
        return optimized_peaks
    
    def _find_maximum(self, df) -> float:
        """ Generates a histogram of the timestamps with 50 bins. Returns the
            timestamp of the left side of the bin with the highest count. 
        """
        
        # Input validation
        min_val = min(df["timestamp"])
        max_val = max(df["timestamp"])
        if min_val == max_val: 
            return min_val
        
        # Settings
        nbins = 100
        
        # Calculate histogram 
        hist, bin_edges = np.histogram(df["timestamp"], bins=nbins)
        
        # Find timestamp with max hist count
        max_index = np.argmax(hist)    
        peak_ts = bin_edges[max_index] + (max_val-min_val)/nbins/2.0
        return int(peak_ts)
    
    def _generate_peaks(self, df: pd.DataFrame, peak_timestamps: list) -> list:
        """
        Takes the new data and a list of the timestamps of the new peaks, and
        builds a list of the Peak instances. 
        """
        
        peaks = []
        for ts in peak_timestamps:
            events = self._get_data_near_peak(df, ts, self.look_left, self.look_right)["timestamp"]
            peak = Peak(
                timestamp=ts, 
                events=events,
                background=self.background
                )
            peaks.append(peak)
        return peaks
    
    def _get_data_near_peak(self, df: pd.DataFrame, ts: int, left: int, right: int): 
        """ Returns all rows of df with timestamp in [ts-left, ts+right]. 
        """
        return df[(df.timestamp >= ts-left) & (df.timestamp <= ts+right)]
    
    def _is_peak(self, df: pd.DataFrame, ts): 
        """ Returns if the peak has more pulses than the background would. 
        """
        
        df1 = self._get_data_near_peak(df, ts, self.look_left, self.look_right)
        time_diff = np.max(df1["timestamp"]) - np.min(df1["timestamp"])
        exp_background = time_diff * self.background
        obs_pulses = len(df1.index)
        return obs_pulses >= exp_background + self.min_pulses_for_peak
        
        
            
