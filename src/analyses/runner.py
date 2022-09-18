# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 13:46:16 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Runner for a collection of Analyses. 
"""

import sys
sys.path.insert(0,'..')

import time

from analyses.ssd_analysis import SSDAnalysis
from analyses.image_analysis import ImageAnalysis
from analyses.mkdir import create_folders


class Runner(object): 
    
    def __init__(self, analyses): 
        self.analyses = analyses
        
    def run(self, cycles: int=100, period_s: int=5): 
        last = time.time()
        start = time.time()
        for i in range(cycles):
            if time.time() < self.next_execution(start, period_s, i): 
                time.sleep(self.next_execution(start, period_s, i) - time.time())
                
            for analyses in self.analyses: 
                analyses.run()
                
            print("Time between executations:", "%.2f" % round(time.time() - last, 2), "s")
            last = time.time()
                
        return 
    
    def next_execution(self, start, period_s, i):
        return start + period_s * i
        
    
if __name__ == '__main__': 
    
    date = "20220918"
    starttime = "125158"
    
    # Input 
    ssd_file = f"W:/WEDATA/data/-{date}-{starttime}-Slot1-In1.csv"
    image_folder = "W:/mot_data/"
    match = f".*{date}.*cmos_.*.csv"
    
    # Output 
    plot_path = f"../../../plots/{date}_{starttime}/"
    result_path = f"../../../results/{date}_{starttime}/"
    
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
                    min_signal=6e6)
        ][1:])
    
    runner.run(cycles=3*12*60, period_s=5)
