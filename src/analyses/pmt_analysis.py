# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 12:19:39 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

PMT Analysis. 
"""


import sys
sys.path.insert(0,'..')

import pandas as pd

from recorders.pmt_recorder import PMTRecorder
from analyses.analysis import Analysis


class PMTAnalysis(Analysis): 
    
    def __init__(self, filepath: str,
                 image_src: str="../../plots/",  
                 image_extension: str=".png"): 
        super(PMTAnalysis, self).__init__(
            recorder=PMTRecorder(filepath), 
            filepath=filepath, 
            name="PMT Analysis",
            image_src=image_src, 
            image_extension=image_extension
            )
    
    def _run_analysis(self, df): 
        self._2d_hist_coil_on(df)
        self._2d_hist_coil_off(df)
        fig = self._plot_1d_hist(x_column="timestamp", bin_nr=100) 
        self.save(fig, "PMT_Hist1D")
        return
        
    def _2d_hist_coil_on(self, df: pd.DataFrame): 
        df_coil_on = self._query_coil_on(df)
        fig = self._plot_2d_hist(
            df=df_coil_on,
            x_column="timestamp", 
            y_column="PMT Current (A)", 
            title_addition="Coil on"
            )
        self.save(fig, "PMT_Hist2D_Coil_on")
        return

    def _2d_hist_coil_off(self, df: pd.DataFrame): 
        df_coil_off = self._query_coil_off(df)
        fig = self._plot_2d_hist(
            df=df_coil_off,
            x_column="timestamp", 
            y_column="PMT Current (A)", 
            title_addition="Coil off"
            )
        self.save(fig, "PMT_Hist2D_Coil_off")
        return
    
    def _query_coil_off(self, df: pd.DataFrame): 
        return df[df["Coil (1:ON 0:OFF)"] == 0]
    
    def _query_coil_on(self, df: pd.DataFrame): 
        return df[df["Coil (1:ON 0:OFF)"] == 1]
    
    
if __name__ == '__main__': 
    
    pmt_analysis = PMTAnalysis(filepath = "../../data/sample/all_data.csv")
    pmt_analysis.run()
