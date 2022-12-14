# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 13:31:02 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Image Analysis: Takes images from the CCD camera and generates plot and reports
from these images. The plots contain 2D gaussian fits which tell us the MOT 
number and the power. The reports are then a collection of results as a table. 
"""

import sys
sys.path.insert(0,'../..')  # Set src as top-level

import pandas as pd

from src.recorders.file_recorder import FileRecorder, FileParser
from src.analyses.fit_mot_number import MOTMLE
from src.analyses.analysis import Analysis, ResultParameter
    
    
class ImageAnalysis(Analysis): 
    
    def __init__(self,
                 recorder: FileRecorder or FileParser,
                 perform_analysis: callable, 
                 result_param: ResultParameter,
                 time_interval: tuple=None,
                 min_signal: int=0):
        super(ImageAnalysis, self).__init__(
            name="Image Analysis",
            recorder=recorder, 
            result_param=result_param
            ) 
        self.perform_analysis = perform_analysis
        self.time_interval = time_interval
        self.min_signal = min_signal
        self.was_run_before = False
        
    def is_up_to_date(self): 
        """ In the beginning, the recorder might be up-to-date, but the
            analysis was not run yet.
        """
        return all((
            self.was_run_before,
            self.recorder.is_up_to_date(),
            self.last_updated == self.recorder.last_updated
            ))
        
    def _query_df(self, df: pd.DataFrame) -> pd.DataFrame(): 
            """ Narrows down the rows to the one in the time interval. 
            """
            if self.time_interval is None: 
                return df
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
            time = str(row["datetime"])
            target = self.image_src + filename + self.image_extension
            statistics = self.perform_analysis(source=source, 
                                               target=target, 
                                               mode="mot number", 
                                               min_signal=self.min_signal, 
                                               time=time)
            statistics_list.append(statistics)
            
        # Enrich dataframe with results
        enriched_df = self._enrich_df_with_statistics(df, statistics_list)
        
        # Save the result
        self._save_results(enriched_df)
        self.was_run_before = True
        return enriched_df
    
    def _enrich_df_with_statistics(self, df: pd.DataFrame, statistics_list: list) -> pd.DataFrame: 
        """ Takes the table from the ImageRecorder and the statistics generated 
            by the fit_mot_data function. Combines the two in an enriched 
            dataframe. 
        """
        columns = list(df.columns) 
        new_columns = ["A", "A_unc", "sigma_x", "sigma_x_unc", "sigma_y", 
                       "sigma_y_unc", "mu_x", "mu_x_unc", "mu_y", "mu_y_unc", 
                       "C", "C_unc", "X-squared", "p-value", "R^2", "signal_sum"]
        enriched_rows = [list(row) + [(stat[col] if stat["fit_successful"] else None) for col in new_columns] + [stat["fit_successful"]]\
                         for (i, row), stat in zip(df.iterrows(), statistics_list)]
        return pd.DataFrame(data=enriched_rows, columns=columns + new_columns + ["fit_successful"])
    
    
if __name__=="__main__": 
    
    from src.constants.mot_constants import c_ccd
    perform_analysis = MOTMLE(c=c_ccd, 
                              references=[], 
                              do_subtract_dead_pixels=False).perform_analysis

    result_param = ResultParameter(
        image_src="../../plots/20220829/image/",
        image_extension=".png",
        result_filepath="../../results/20220829/"+"image_analysis_results.csv"
        )
    file_recorder = FileRecorder(
        filepath="C:\\Users\\roman\\Desktop\\Research_UTokyo\\Data\\mot\\",
        match=".*ccd_.*.xlsx"
        )
    image_analysis = ImageAnalysis(
        recorder=file_recorder,
        perform_analysis=perform_analysis, 
        result_param=result_param
        )
    enriched_df = image_analysis.run()
    