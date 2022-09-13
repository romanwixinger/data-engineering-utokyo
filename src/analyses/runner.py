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
from analyses.pmt_analysis import PMTAnalysis


class Runner(object): 
    
    def __init__(self, analyses): 
        self.analyses = analyses
        
    def run(self, cycles: int=500, period_s: int=1): 
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
        
        
runner = Runner(analyses=[
    SSDAnalysis(filepath="../../data/20220829/-20220829-144945-Slot1-In1.csv",
                image_src="../../plots/mock"),
    PMTAnalysis(filepath="../../data/sample/all_data.csv",
                image_src="../../plots/mock")
    ])

runner.run()
