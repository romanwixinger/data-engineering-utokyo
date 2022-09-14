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
        
        # Prepare parameters
        bins = 50
        nx = np.linspace(np.min(self.events), np.max(self.events), bins)
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 7))
        plt.hist(self.events, bins=(nx))
       
        # Add references to timestamp
        plt.axvline(self.timestamp, color='k', linestyle='dashed', linewidth=1)
        min_ylim, max_ylim = plt.ylim()
        plt.text(self.timestamp + 1e8, max_ylim*0.9, 'Peak timestamp')
        
        # Add reference regarding background
        background = self.background * (max(self.events) - min(self.events)) / bins
        min_xlim, max_xlim = plt.xlim()
        plt.axhline(background, color='k', linestyle='dashed', linewidth=1)
        plt.text(min_xlim + (max_xlim - min_xlim)*0.6, background * 0.95 + max_ylim * 0.05, 'Background')
        
        # Add descriptions
        plt.title("Histogram of peak.")
        fig.savefig(fname=url)
        plt.show()

        return 