# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 17:24:48 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Representation of a recorder as histogram. 
"""

import sys
sys.path.insert(0,'..')

import pandas as pd

from recorders.ssd_recorder import SSDRecorder


class SSDRepresentation(): 
    
    def __init__(self, ssd_recorder: SSDRecorder): 
        self.ssd_recorder = ssd_recorder
    
    def get_hist_rep(self) -> pd.DataFrame: 
        ssd_df = self.ssd_recorder.get_table()
        nr_of_channels = ssd_df["//Gain"][0]
        
        # Groupby timestamp and PulseHeight (channel)
        grouped = ssd_df.groupby(by=["datetime", "PulseHeight"])
        df = grouped.agg({"TraceName": 'count'}).rename({"TraceName": "PulseCount"}, axis=1)
        df = df.unstack(level='PulseHeight').fillna(0, downcast="infer")
        
        # Fix column names
        df.columns = df.columns.to_flat_index()
        df.columns = [str(col[1]) for col in df.columns.values]
            
        return df
    
    def get_time_aggregated_hist_rep(self) -> pd.DataFrame: 
        df = self.get_hist_rep() 
        df_sum = df.sum()
        df = pd.DataFrame(data=[df_sum.values], columns=df_sum.index.values)
        return df
    
    def get_channel_aggregated_hist_rep(self) -> pd.DataFrame: 
        """ TODO: Implement aggregation over all channels. 
        """
        
        df = self.get_hist_rep()
        df_channel = df.sum(axis=1, min_count=1).to_frame()
        return df_channel