# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 13:46:16 2022
@author: Roman Wixinger (roman.wixinger@gmail.com)


Runner for analyses on the J5 computer. 
"""

import sys
sys.path.insert(0,'../..')  # Set src as top-level

from datetime import datetime

from src.analyses.ssd_analysis import SSDAnalysisWrapper
from src.analyses.image_analysis import ImageAnalysis
from src.analyses.mkdir import create_folders
from src.analyses.runner import Runner
        
    
date = "20220918"
starttime = "090000"

# Input
ssd_folder = "W:/WEDATA/data/"
image_folder = "W:/mot_data/"
match = ".*cmos_.*.csv"
time_interval = (datetime(2022, 9, 18, 9, 0, 0), 
                 datetime(2022, 9, 18, 23, 59, 59))

# Output 
plot_path = f"W:/plots/{date}_{starttime}/"
result_path = f"W:/results/{date}_{starttime}/"

# Make dirs
create_folders(plot_path, result_path)
    
runner = Runner(analyses=[
    SSDAnalysisWrapper(
        folder=ssd_folder,
        image_src=plot_path,
        image_extension=".png",
        result_filepath=result_path
        ),
    ImageAnalysis(filepath=image_folder, 
                match=match, 
                image_src=plot_path+"image/",
                result_filepath=result_path+"image_analysis_results.csv",
                min_signal=6e6,
                time_interval=time_interval)
    ][1:])

runner.run(cycles=3*12*60, period_s=5)

