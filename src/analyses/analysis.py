# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 09:43:50 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Base class for analyses. 
"""


from abc import abstractmethod
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


""" Class """
    

class Analysis(object): 
    """ Class for analyzing relationsships between experimental parameters and measurements. 
    """
        
    def __init__(self, 
                 recorder, 
                 filepath, 
                 name, 
                 image_src: str="../../plots/", 
                 image_extension: str=".png"): 
        self.recorder = recorder
        self.filepath = filepath
        self.name = name
        self.last_updated = 0
        self.image_src = image_src
        self.image_extension = ".png"
        
    def run(self): 
        if self.is_up_to_date():
            return
        df = self.recorder.get_table()
        self.last_updated = self.recorder.last_updated
        return self._run_analysis(df)
    
    def save(self, fig, filename): 
        fig.savefig(fname = self.image_src + filename + self.image_extension)
        
    def is_up_to_date(self): 
        return all((
            self.recorder.is_up_to_date(),
            self.last_updated == self.recorder.last_updated
            ))
    
    @abstractmethod
    def _run_analysis(self, df: pd.DataFrame): 
        """ Methods which executes the plotting and saving. 
        """
        pass
    
    def _plot_2d_hist(self,
                      df: pd.DataFrame,
                      x_column: str, 
                      y_column: str,
                      bin_nr: int=100,
                      title_addition: str="", 
                      ):
        """ Plots the data from the recorder as 2D histogram. 
        """
        
        x, y = df[x_column], df[y_column]
        
        # Prepare parameters
        nx = np.linspace(np.min(x), np.max(x), bin_nr)
        ny = np.linspace(np.min(y), np.max(y), bin_nr)
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 7))
        plt.hist2d(x, y, bins=(nx, ny), range=None, density=False, weights=None, cmin=None, cmax=None)
        
        # Add descriptions
        plt.title(f"2D Histogram of {y_column} against {x_column}" + (f": {title_addition}." if title_addition else "."))
        ax.set_xlabel(x_column) 
        ax.set_ylabel(y_column) 
        
        return fig
    
    def _plot_1d_hist(self, x_column: str, bin_nr: int=100): 
        
        # Load data
        ssd_df = self.recorder.get_table()
        x = ssd_df[x_column]
        
        # Prepare parameters
        nx = np.linspace(np.min(x), np.max(x), bin_nr)
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 7))
        plt.hist(x, bins=(nx))
        
        # Add descriptions
        plt.title(f"Histogram of {x_column}.")
        ax.set_xlabel(x_column) 

        return fig