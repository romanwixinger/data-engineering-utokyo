# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 12:31:11 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Script to execute the analyses. 
"""

import sys
sys.path.insert(0,'..')

from datetime import datetime

from constants.mot_constants import c_ccd
from recorders.ssd_recorder import SSDRecorder
from recorders.file_recorder import FileRecorder
from analyses.analysis import ResultParameter
from analyses.ssd_analysis import SSDAnalysis
from analyses.image_analysis import ImageAnalysis
from analyses.mkdir import create_folders
from analyses.runner import Runner
from analyses.fit_mot_number import MOTMLE


if __name__ == '__main__': 
    
    # Input 
    ssd_file = "../data/20220829/-20220829-144945-Slot1-In1.csv"
    image_folder = "C:\\Users\\roman\\Desktop\\Research_UTokyo\\Data\\mot"
    match = ".*ccd_detuning.*.xlsx"
    c = c_ccd
    min_signal = 0
    time_interval = (
        datetime(2000, 1, 1, 12, 0, 0), 
        datetime(2030, 1, 1, 12, 0, 0)
        )
    use_n_reference_images = 4
    dead_pixel_ratio = 1.0 / 5.0
    
    # Output 
    plot_path = "../plots/20220829/"
    result_path = "../results/20220829/"
    
    # Make dirs
    create_folders(plot_path, result_path)
    
    # Setup result parameters
    result_param_ssd = ResultParameter(
        image_src=plot_path+"ssd/",
        image_extension=".png",
        result_filepath=result_path+"ssd_analysis_results.csv"
        )
    result_param_image = ResultParameter(
        image_src=plot_path+"image/",
        image_extension=".png",
        result_filepath=result_path+"image_analysis_results.csv"
        )
    
    # Setup recorders
    ssd_recorder = SSDRecorder(filepath=ssd_file)
    image_recorder = FileRecorder(
        filepath=image_folder,
        match=match 
        )
    
    # Setup analyses
    reference_image_filepaths = image_recorder.get_table().head(use_n_reference_images)["filepath"]
    perform_analysis = MOTMLE(c=c, 
                              references=reference_image_filepaths,
                              do_subtract_dead_pixels=True,
                              dead_pixel_ratio=dead_pixel_ratio).perform_analysis
    ssd_analysis = SSDAnalysis(
        recorder=ssd_recorder,
        result_param=result_param_ssd
        )
    image_analysis = ImageAnalysis(
        recorder=image_recorder,
        perform_analysis=perform_analysis, 
        result_param=result_param_image,
        min_signal=min_signal,
        time_interval=time_interval
        )
        
    # Setup runner
    runner = Runner(analyses=[image_analysis])
    runner.run(cycles=3*12*60, period_s=5)
