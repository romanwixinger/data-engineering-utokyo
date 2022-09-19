# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 09:42:32 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

SSD Histogram 
"""

import sys
sys.path.insert(0,'..')

import matplotlib.pyplot as plt

import constants as c
from recorders.ssd_recorder import SSDParser
from analyses.analysis import Analysis
from analyses.peak_finder import PeakFinder

plt.rcParams.update(c.plotting_params) 

class SSDHistogramAnalysis(Analysis): 
    
    def __init__(self, filepath: str, 
                 image_src: str="../../plots/",  
                 image_extension: str=".png"):
        super(SSDHistogramAnalysis, self).__init__(
            recorder=SSDParser(filepath), 
            filepath=filepath, 
            name="SSD Histogram Analysis",
            image_src=image_src, 
            image_extension=image_extension,
            ) 
        
        

