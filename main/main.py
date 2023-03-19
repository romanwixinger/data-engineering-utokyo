# -*- coding: utf-8 -*-
"""Executes the analyses.
"""


from datetime import datetime

from src.utilities.camera_constants import c_ccd, c_cmos_Fr_20220918
from src.recorders.ssd_recorder import SSDRecorder
from src.recorders.file_recorder import FileRecorder
from src.analyses.analysis import ResultParameter
from src.analyses.ssd_analysis import SSDAnalysis
from src.analyses.image_analysis import ImageAnalysis
from src.analyses.mkdir import create_folders
from src.analyses.runner import Runner
from src.analyses.fit_mot_number import MOTMLE


if __name__ == '__main__': 
    
    # Input 
    ssd_file = "../data/20220829/-20220829-144945-Slot1-In1.csv"
    image_folder = "../data/beamtime/mot_data/" # "C:\\Users\\roman\\Desktop\\Research_UTokyo\\Data\\mot"
    match = ".*cmos.*.csv" # ".*ccd_detuning.*.xlsx"
    c = c_cmos_Fr_20220918
    min_signal = 95000
    time_interval = (
        datetime(2000, 1, 1, 12, 0, 0), 
        datetime(2030, 1, 1, 12, 0, 0)
        )
    use_n_reference_images = 10
    dead_pixel_percentile = 5.0 # [%], must between 0 and 100
    
    # Output 
    plot_path = "../plots/beamtime/"  # "../plots/20220829/"
    result_path = "../results/beamtime/"  # "../results/20220829/"
    
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
