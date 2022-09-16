# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 12:36:16 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Analyses the half-life time of the peaks in the SSD pulse data and
plots the region around the peaks as histogram. 
"""


import sys
sys.path.insert(0,'..')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt

from constants import plotting_params
plt.rcParams.update(plotting_params)


class Peak(object): 
    """ Class for storing peaks of the SSD data and doing some data analysis
        on them. 
    """
    
    def __init__(self, timestamp: int, events: list, background: float):
        self.timestamp = timestamp
        self.events = events
        self.height = 0
        self.half_life_time = 0
        self.background = background
    
    def estimate(self): 
        """ Fits the height, half-life time and background as a simple 
            exponential decay with a constant offset. 
        """
        pass
    
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
        print(ts_list)
        timestamps_list = self._ts_ns_to_timestamp(ts_list)
        ax.xaxis.set_ticks(timestamps_list)
        xfmt = md.DateFormatter('%H:%M:%S')
        ax.xaxis.set_major_formatter(xfmt)
        plt.xticks(rotation=25)
        
        # Add descriptions
        plt.title("Histogram of SSD pulses around the peak.")
        plt.xlabel("Time")
        plt.ylabel("Pulses [1]")
        fig.savefig(fname=url)
        plt.show()

        return 
    
    def _ts_ns_to_timestamp(self, ts_list: list[int]): 
        if type(ts_list) == int: 
            ts = ts_list
            return dt.datetime.fromtimestamp(ts / 1000000000)
        return [dt.datetime.fromtimestamp(ts / 1000000000) for ts in ts_list]