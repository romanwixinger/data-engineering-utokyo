# -*- coding: utf-8 -*-
"""Runs a collection of analyses on the J5 computer.
"""


from datetime import datetime

from .ssd_analysis import SSDAnalysisWrapper
from .image_analysis import ImageAnalysis
from .mkdir import create_folders
from .runner import Runner


if __name__=="_ _main_ _":
    
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

