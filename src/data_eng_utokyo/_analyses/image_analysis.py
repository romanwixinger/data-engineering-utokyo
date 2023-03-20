# -*- coding: utf-8 -*-
"""Takes images from the CCD camera and generates plot and reports from these images.

The plots contain 2D gaussian fits which tell us the MOT number and the power. The reports are then a collection of
results as a table.
"""

import pandas as pd

from .._recorders.file_recorder import FileRecorder, FileParser
from .analysis import Analysis, ResultParameter
    
    
class ImageAnalysis(Analysis):
    """Takes a recorder with image files and an analysis function and creates plots and reports.

    Args:
        recorder (Recorder): Recorder which contains the filepaths of the images.
        perform_analysis (callable): Analysis function that is applied on each image.
        result_param (ResultRecorder): Object which tells how the plot should be formated.
        time_interval (tuple): Tuple of start and endtime. Just files in this interval will be processed.
        min_signal (int): Images with sum of pixels less than this threshold will be ignored.

    Example:
        .. code:: python

            from data_eng_utokyo.recorder import FileRecorder
            from data_eng_utokyo.analyses import MOTMLE, ResultParameter, ImageAnalysis
            from data_eng_utokyo.constants import c_ccd

            perform_analysis = MOTMLE(
                c=c_ccd,
                references=[],
                do_subtract_dead_pixels=False,
            ).perform_analysis

            result_param = ResultParameter(
                image_src="../../../plots/20220829/image/",
                image_extension=".png",
                result_filepath="../../results/20220829/"+"image_analysis_results.csv",
            )
            file_recorder = FileRecorder(
                filepath="C:\\Users\\roman\\Desktop\\Research_UTokyo\\Data\\mot\\",
                match=".*ccd_.*.xlsx",
            )
            image_analysis = ImageAnalysis(
                recorder=file_recorder,
                perform_analysis=perform_analysis,
                result_param=result_param,
                )
            enriched_df = image_analysis.run()

    Attributes:
        self.was_run_before (bool): Flag.
    """
    
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
        """Tells if the analysis was already run with the most recent data available.

        In the beginning, the recorder might be up-to-date, but the analysis was not run yet. This method helps us deal
        with such cases.

        Returns:
            Bool whether the analysis is already up to date with the data or not.
        """
        return all((
            self.was_run_before,
            self.recorder.is_up_to_date(),
            self.last_updated == self.recorder.last_updated
            ))
        
    def _query_df(self, df: pd.DataFrame) -> pd.DataFrame():
        """Gets the rows of the dataframe which have a time in the interval provided in self.time_interval.

        Returns:
            Sliced pandas dataframe.
        """
        if self.time_interval is None:
            return df
        start = self.time_interval[0]
        stop = self.time_interval[1]
        return df[(start <= df.datetime) & (df.datetime <= stop)]
        
    def _run_analysis(self, df: pd.DataFrame): 
        """Runs the fit_mot_number algorithm on all images, saves the images and saves the fit result in a new table.

        Args:
            df: Dataframe with the data as provided by the recorder.

        Returns:
            Enriched dataframe with additional columns representing the results of the analysis.
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
        """Add the statistics generated in the analysis to the dataframe.

        Takes the table from the ImageRecorder and the statistics generated by the fit_mot_data function. Combines the
        two in an enriched dataframe.

        Args:
            df (pd.DataFrame): Initial dataframe as provided by the recorder.
            statistics_list: List of results (statistics lookups). Each item has a 1:1 corresponding to a row of the df.

        Returns:
            Dataframe enriched with the statistics.
        """
        columns = list(df.columns) 
        new_columns = ["A", "A_unc", "sigma_x", "sigma_x_unc", "sigma_y", 
                       "sigma_y_unc", "mu_x", "mu_x_unc", "mu_y", "mu_y_unc", 
                       "C", "C_unc", "X-squared", "p-value", "R^2", "signal_sum"]
        enriched_rows = [list(row) + [(stat[col] if stat["fit_successful"] else None) for col in new_columns] + [stat["fit_successful"]]\
                         for (i, row), stat in zip(df.iterrows(), statistics_list)]
        return pd.DataFrame(data=enriched_rows, columns=columns + new_columns + ["fit_successful"])
