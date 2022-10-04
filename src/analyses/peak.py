# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 12:36:16 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Analyses the half-life time of the peaks in the SSD pulse data and
plots the region around the peaks as histogram. 
"""


import sys
sys.path.insert(0,'../..')  # Set src as top-level

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt
import math

from src.constants.constants import plotting_params
plt.rcParams.update(plotting_params)


class Peak(object): 
    """ Class for storing peaks of the SSD data and doing some data analysis
        on them. 
    """
    
    def __init__(self, timestamp: int, events: list, background: float):
        self.timestamp = timestamp      # [ns]
        self.events = events            # list(ns)
        self.pulses =  len(self.events) # [1]
        self.background = background    # Rate [1/ns]
        self.pulses_background = self.background * (max(self.events) - min(self.events))   # [1]
        self.pulses_peak = self.pulses - self.pulses_background                            # [1]      
        self.half_life_time = 0         # Estimated [ns]
        self.estimate()
    
    def estimate(self): 
        """ Calculates the half-life time. The result can be derived with MLE
            by adapting the reasoning from here: 
            https://math.stackexchange.com/questions/101481/calculating-maximum-likelihood-estimation-of-the-exponential-distribution-and-pr
        """
        # Query pulses after peak
        after_peak_events = [ts for ts in self.events if ts >= self.timestamp]
        
        # Lookup parameter for MLE.
        begin_ns = self.timestamp
        end_ns = max(after_peak_events)
        
        # n: Number of real events
        n_total = len(after_peak_events)
        n_bg = (end_ns - begin_ns) * self.background
        n = n_total - n_bg
        
        # sum_i x_i, i=1,..,n: Total time of the real events
        sum_total = sum((ts - begin_ns for ts in after_peak_events))
        sum_bg = n_bg * (end_ns - begin_ns) / 2
        sm = sum_total - sum_bg 
        
        lmbda = n / sm  # [1/ns]
        tau = 1/lmbda   # [ns]
        half_life_time = math.log(2) * tau  # [ns]
        print(f"The half-life time is: {1e-9 * half_life_time} s")
        self.half_life_time = half_life_time
        return
    
    def plot(self, url: str):
        """ Visualizes the data and fit and saves the image to the url. 
        """
        
        # Convert unit
        timestamp = self._ts_ns_to_timestamp(self.timestamp)
        timestamps = self._ts_ns_to_timestamp(self.events)
        
        # Prepare parameters
        bins = 50
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 7))
        plt.hist(timestamps, bins=bins)
        
        # Add references to timestamp
        plt.axvline(timestamp, color='k', linestyle='dashed', linewidth=1)
        min_xlim, max_xlim = plt.ylim()
        min_ylim, max_ylim = plt.ylim()
        plt.text(timestamp + dt.timedelta(milliseconds=100), 0.1 * min_ylim + 0.9 * max_ylim, 'Peak timestamp')

        # Add reference regarding background
        background = self.background * (max(self.events) - min(self.events)) / bins
        min_xlim, max_xlim = plt.xlim()
        plt.axhline(background, color='k', linestyle='dashed', linewidth=1)
        plt.text(min_xlim + (max_xlim - min_xlim)*0.8, background * 0.90 + max_ylim * 0.1, 'Background')
       
        # Timestamp of x-axis
        second = 1000000000 
        min_ts = np.min(self.events) - (np.min(self.events) % second)
        max_ts = np.max(self.events) - (np.max(self.events) % second)
        stepsize = second 
        ts_list = np.arange(min_ts, max_ts + 2 * second, stepsize)[1:-1]
        timestamps_list = self._ts_ns_to_timestamp(ts_list)
        ax.xaxis.set_ticks(timestamps_list)
        xfmt = md.DateFormatter('%M:%S')
        ax.xaxis.set_major_formatter(xfmt)
        plt.xticks(rotation=25)
        
        # Add descriptions
        plt.title("Histogram of SSD pulses around the peak.")
        plt.xlabel("Time [M:S]")
        plt.ylabel("Pulses [1]")
        fig.savefig(fname=url)
        plt.show()

        return 
    
    def _ts_ns_to_timestamp(self, ts_list: list[int]): 
        if type(ts_list) == int: 
            ts = ts_list
            return dt.datetime.fromtimestamp(ts / 1000000000)
        return [dt.datetime.fromtimestamp(ts / 1000000000) for ts in ts_list]

    def as_dataframe(self) -> pd.DataFrame:
        """ Return the pulse as pandas dataframe. 
        """
        dic = self.__dict__()
        columns = dic.keys()
        values = dic.values()
        return pd.DataFrame(data=[values], columns=columns)
    
    def __dict__(self): 
        """ Dict representation of a peak. 
        """
        
        return {
            "timestamp_ns": self.timestamp,
            "pulses_peak": self.pulses_peak, 
            "pulses_background": self.pulses_background,
            "half_life_time": self.half_life_time, 
            "background": self.background
            }
    
    
    