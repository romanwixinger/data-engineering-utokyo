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
    
    def __init__(self, filepath: str): 
        super(PMTAnalysis, self).__init__(PMTRecorder, filepath, "PMT Analysis") 
    
    def run(self): 
        df = self.recorder.get_table()
        self._2d_hist_coil_on(df)
        self._2d_hist_coil_off(df)
        self._plot_1d_hist(x_column="timestamp", x_bin_nr=100) 
        return
    
    def _2d_hist_coil_on(self, df: pd.DataFrame): 
        df_coil_on = self._query_coil_on(df)
        self._plot_2d_hist(
            df=df_coil_on,
            setting="Coil on",
            x_column="timestamp", 
            y_column="PMT Current (A)", 
            x_bin_nr=500, 
            y_bin_nr=500,
            x_min_percentile=5.0,
            x_max_percentile=95.0,
            y_min_percentile=5.0,
            y_max_percentile=95.0
            )
        return

    def _2d_hist_coil_off(self, df: pd.DataFrame): 
        df_coil_off = self._query_coil_off(df)
        self._plot_2d_hist(
            df=df_coil_off,
            setting="Coil off",
            x_column="timestamp", 
            y_column="PMT Current (A)", 
            x_bin_nr=500, 
            y_bin_nr=500,
            x_min_percentile=5.0,
            x_max_percentile=95.0,
            y_min_percentile=5.0,
            y_max_percentile=95.0
            )
        return
    
    def _query_coil_off(self, df: pd.DataFrame): 
        return df[df["Coil (1:ON 0:OFF)"] == 0]
    
    def _query_coil_on(self, df: pd.DataFrame): 
        return df[df["Coil (1:ON 0:OFF)"] == 1]
    
    
if __name__ == '__main__': 
    
    pmt_analysis = PMTAnalysis(filepath = "../../data/sample/all_data.csv")
    pmt_analysis.run()
