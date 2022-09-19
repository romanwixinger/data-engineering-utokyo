# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 13:31:02 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Image Analysis: Takes images from the CCD camera and generates plot and reports
from these images. The plots contain 2D gaussian fits which tell us the MOT 
number and the power. The reports are then a collection of results as a table. 
"""

import sys
sys.path.insert(0,'..')

from datetime import datetime
import pandas as pd
import os

from recorders.image_recorder import ImageParser
from fit_mot_number import perform_analysis
from analyses.analysis import Analysis
    
    
class ImageAnalysis(Analysis): 
    
    def __init__(self, filepath: str, 
                 image_src: str="../../plots/",  
                 image_extension: str=".png",
                 match: str=".*ccd_detuning.*.xlsx",
                 result_filepath: str="",
                 min_signal: int=0,
                 time_interval: tuple=(datetime(2000, 1, 1, 12, 0, 0), 
                                       datetime(2030, 1, 1, 12, 0, 0))):
        super(ImageAnalysis, self).__init__(
            recorder=ImageParser(filepath, match=match), 
            filepath=filepath, 
            name="Image Analysis",
            image_src=image_src, 
            image_extension=image_extension,
            result_filepath=result_filepath
            ) 
        self.time_interval = time_interval
        self.min_signal = min_signal
        
    def _query_df(self, df: pd.DataFrame) -> pd.DataFrame(): 
            """ Narrows down the rows to the one in the time interval. 
            """
            start = self.time_interval[0]
            stop = self.time_interval[1]
            return df[(start <= df.datetime) & (df.datetime <= stop)]
        
    def _run_analysis(self, df: pd.DataFrame): 
        """ Runs the fit_mot_number algorithm on all images, saves the images
            and saves the fit result in a new table. 
        """
        
        statistics_list = []
        
        # Fit and plot
        for i, row in df.iterrows(): 
            source = row["filepath"]
            filename = row["filename"]
            target = self.image_src + filename + self.image_extension
            statistics = perform_analysis(source=source, target=target, mode="mot number", min_signal=self.min_signal)
            statistics_list.append(statistics)
            
        # Enrich dataframe with results
        enriched_df = self._enrich_df_with_statistics(df, statistics_list)
        
        # Save the result
        self.save_results(enriched_df)
        return enriched_df
    
    def _enrich_df_with_statistics(self, df: pd.DataFrame, statistics_list: list[dict]) -> pd.DataFrame: 
        """ Takes the table from the ImageRecorder and the statistics generated 
            by the fit_mot_data function. Combines the two in an enriched 
            dataframe. 
        """
        columns = list(df.columns) 
        new_columns = ["A", "A_unc", "sigma_x", "sigma_x_unc", "sigma_y", 
                       "sigma_y_unc", "mu_x", "mu_x_unc", "mu_y", "mu_y_unc", 
                       "C", "C_unc", "X-squared", "p-value", "R^2"]
        enriched_rows = [list(row) + [(stat[col] if stat["fit_successful"] else None) for col in new_columns] + [stat["fit_successful"]]\
                         for (i, row), stat in zip(df.iterrows(), statistics_list)]
        return pd.DataFrame(data=enriched_rows, columns=columns + new_columns + ["fit_successful"])
    
    
if __name__=="__main__": 
    
    image_analysis = ImageAnalysis(filepath="C:\\Users\\roman\\Desktop\\Research_UTokyo\\Data\\mot", 
                                   match=".*ccd_.*.xlsx", 
                                   image_src="../../plots/20220829/images/",
                                   result_filepath="../../results/20220829/"+"image_analysis_results.csv",
                                   min_signal=1e8)
    enriched_df = image_analysis.run()
    