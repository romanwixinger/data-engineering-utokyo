# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 12:31:11 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Script to execute the analyses. 
"""

import sys
sys.path.insert(0,'..')

from datetime import datetime

from analyses.ssd_analysis import SSDAnalysis
from analyses.image_analysis import ImageAnalysis
from analyses.mkdir import create_folders
from analyses.runner import Runner


if __name__ == '__main__': 
    
    # Input 
    ssd_file = "../../data/20220829/-20220829-144945-Slot1-In1.csv"
    image_folder = "C:\\Users\\roman\\Desktop\\Research_UTokyo\\Data\\mot"
    match = ".*ccd_detuning.*.xlsx"
    
    # Output 
    plot_path = "../../plots/20220829/"
    result_path = "../../results/20220829/"
    
    # Make dirs
    create_folders(plot_path, result_path)
        
    runner = Runner(analyses=[
        SSDAnalysis(
            filepath=ssd_file ,
            image_src=plot_path + "ssd/",
            image_extension=".png",
            result_filepath=result_path+"ssd_analysis_results.csv"
            ),
        ImageAnalysis(filepath=image_folder, 
                    match=match, 
                    image_src=plot_path+"image/",
                    result_filepath=result_path+"image_analysis_results.csv",
                    min_signal=6e6,
                    time_interval=(datetime(2000, 1, 1, 12, 0, 0), 
                                   datetime(2030, 1, 1, 12, 0, 0)))
        ][1:])
    
    runner.run(cycles=3*12*60, period_s=5)
