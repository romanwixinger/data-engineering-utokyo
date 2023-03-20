# -*- coding: utf-8 -*-
"""Analyses the PMT data provided by the PMTRecorder.
"""

import pandas as pd

from .._recorders.pmt_recorder import PMTRecorder
from .analysis import Analysis, ResultParameter


class PMTAnalysis(Analysis): 
    
    def __init__(self, 
                 recorder: PMTRecorder,
                 result_param: ResultParameter): 
        super(PMTAnalysis, self).__init__(
            recorder=recorder,
            name="PMT Analysis",
            result_param=result_param
            )
    
    def _run_analysis(self, df): 
        self._2d_hist_coil_on(df)
        self._2d_hist_coil_off(df)
        fig = self._plot_1d_hist(x_column="timestamp", bin_nr=100) 
        self._save_fig(fig, "PMT_Hist1D")
        return
        
    def _2d_hist_coil_on(self, df: pd.DataFrame): 
        df_coil_on = self._query_coil_on(df)
        fig = self._plot_2d_hist(
            df=df_coil_on,
            x_column="timestamp", 
            y_column="PMT Current (A)", 
            title_addition="Coil on"
            )
        self._save_fig(fig, "PMT_Hist2D_Coil_on")
        return

    def _2d_hist_coil_off(self, df: pd.DataFrame): 
        df_coil_off = self._query_coil_off(df)
        fig = self._plot_2d_hist(
            df=df_coil_off,
            x_column="timestamp", 
            y_column="PMT Current (A)", 
            title_addition="Coil off"
            )
        self._save_fig(fig, "PMT_Hist2D_Coil_off")
        return
    
    def _query_coil_off(self, df: pd.DataFrame): 
        return df[df["Coil (1:ON 0:OFF)"] == 0]
    
    def _query_coil_on(self, df: pd.DataFrame): 
        return df[df["Coil (1:ON 0:OFF)"] == 1]
    
    
if __name__ == '__main__': 
    
    pmt_recorder = PMTRecorder(filepath ="../../../data/sample/all_data.csv")
    result_param = ResultParameter(image_src="", 
                                   image_extension=".png",
                                   result_filepath="../../results/"+"pmt_analysis_results.csv",)
    pmt_analysis = PMTAnalysis(recorder=pmt_recorder, result_param=result_param)
    pmt_analysis.run()
