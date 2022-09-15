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

import pandas as pd
import os

from recorders.image_recorder import ImageRecorder
from fit_mot_number import perform_analysis
from analyses.analysis import Analysis
    
    
class ImageAnalysis(Analysis): 
    
    def __init__(self, filepath: str, 
                 image_src: str="../../plots/",  
                 image_extension: str=".png",
                 match: str=".*ccd_detuning.*.xlsx"):
        super(ImageAnalysis, self).__init__(
            recorder=ImageRecorder(filepath, match=match), 
            filepath=filepath, 
            name="Image Analysis",
            image_src=image_src, 
            image_extension=image_extension
            ) 
        
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
            statistics = perform_analysis(source=source, target=target, mode="mot number")
            statistics_list.append(statistics)
            
        # Enrich dataframe with results
        enriched_df = self._enrich_df_with_statistics(df, statistics_list)
        
        # Save the result
        self._save_df(enriched_df)
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
    
    def _save_df(self, df): 
        """ Save the enriched dataframe to an analysis subfolder. 
        """
        os.makedirs(f'{folder}/analysis', exist_ok=True)  
        df.to_csv(f'{folder}/analysis/result.csv')  
    
if __name__=="__main__": 
    
    folder = "C:\\Users\\roman\\Desktop\\Research_UTokyo\\Data\\mot"
    match = ".*ccd_.*.xlsx"
    image_src = "../../plots/images/"
    
    image_analysis = ImageAnalysis(filepath=folder, 
                                   match=match, 
                                   image_src=image_src)
    enriched_df = image_analysis.run()
    