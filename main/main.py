# -*- coding: utf-8 -*-
"""Executes the analyses.
"""


from datetime import datetime

from data_eng_utokyo.constants import c_cmos_Fr_20220918
from data_eng_utokyo.recorders import (
    SSDRecorder,
    FileRecorder,
)
from data_eng_utokyo.analyses import (
    ResultParameter,
    SSDAnalysis,
    ImageAnalysis,
    Runner,
    MOTMLE,
)
from data_eng_utokyo.utilities import create_folders


if __name__ == '__main__': 
    
    # Input 
    ssd_file = "data/20220829/-20220829-144945-Slot1-In1.csv"
    image_folder = "data/beamtime/mot_data/"
    match = ".*cmos.*.csv"
    c = c_cmos_Fr_20220918
    min_signal = 95000
    time_interval = (
        datetime(2000, 1, 1, 12, 0, 0), 
        datetime(2030, 1, 1, 12, 0, 0)
        )
    use_n_reference_images = 10
    dead_pixel_percentile = 5.0  # [%], must between 0 and 100
    
    # Output 
    plot_path = "plots/beamtime/"
    result_path = "results/beamtime/"
    
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
                              dead_pixel_percentile=dead_pixel_percentile).perform_analysis
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
