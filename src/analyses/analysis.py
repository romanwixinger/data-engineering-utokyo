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


class Analysis(object): 
    """ Class for analyzing relationsships between experimental parameters and measurements. 
    """
    
    image_src = "../../plots/"
    image_extension = ".png"
    
    def __init__(self, recorder, filepath, name): 
        self.recorder = recorder(filepath)
        self.filepath = filepath
        self.name = name
        self.last_updated = 0
        
    def run(self): 
        if self.is_up_to_date():
            return
        df = self.recorder.get_table()
        self.last_updated = self.recorder.last_updated
        self._run_analysis(df)
        return
    
    def save(self, fig, filename): 
        fig.savefig(fname = self.image_src + filename + self.image_extension)
        
    def is_up_to_date(self): 
        return all((
            self.recorder.table_is_up_to_date(),
            self.last_updated == self.recorder.last_updated
            ))
    
    @classmethod
    def _run_analysis(self): 
        """ Methods which executes the plotting and saving. 
        """
        pass
    
    def _plot_2d_hist(self,
                      df: pd.DataFrame,
                      setting: str, 
                      x_column: str, 
                      y_column: str, 
                      x_bin_nr: int=100, 
                      y_bin_nr: int=100, 
                      x_min_percentile: float=0.0, 
                      x_max_percentile: float=100.0,
                      y_min_percentile: float=0.0, 
                      y_max_percentile: float=100.0
                      ):
        """
        Plots the data from the recorder as 2D histogram. The x_bin_nr and 
        y_bin_nr specifies how many bins we want to have in each direction.
        The y_min_p (y_max_p) percentile specifies the percentile of the lower
        and upper limit of the array. In case of 0.0 (1.0), the full array is
        used and y_min = min(y), y_max = max(y). 
        """
        
        # Load data
        x = df[x_column]
        y = df[y_column]
        
        # Prepare parameters
        x_min = np.min(x)
        x_max = np.max(x)
        x_min = np.percentile(x, x_min_percentile)
        x_max = np.percentile(x, x_max_percentile)
        y_min = np.percentile(y, y_min_percentile)
        y_max = np.percentile(y, y_max_percentile)
        nx = np.linspace(x_min, x_max,  x_bin_nr)
        ny = np.linspace(y_min, y_max, y_bin_nr)
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 7))
        plt.hist2d(x, y, bins=(nx, ny), range=None, density=False, weights=None, cmin=None, cmax=None)
        
        # Add descriptions
        plt.title(f"2D Histogram of {y_column} against {x_column}" + (f": {setting}." if setting else "."))
        ax.set_xlabel(x_column) 
        ax.set_ylabel(y_column) 
        
        return fig
    
    def _plot_1d_hist(self, x_column: str, x_bin_nr: int=100): 
        
        # Load data
        ssd_df = self.recorder.get_table()
        x = ssd_df[x_column]
        
        # Prepare parameters
        x_min = np.min(x)
        x_max = np.max(x)
        nx = np.linspace(x_min, x_max, x_bin_nr)
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 7))
        plt.hist(x, bins=(nx))
        
        # Add descriptions
        plt.title(f"Histogram of {x_column}.")
        ax.set_xlabel(x_column) 

        return fig
