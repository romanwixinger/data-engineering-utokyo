# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 13:31:02 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Image Analysis: Takes images from the CCD camera and generates plot and reports
from these images. The plots contain 2D gaussian fits which tell us the MOT 
number and the power. The reports are then a collection of results as a table. 
"""

import sys
sys.path.insert(0,'..')

from recorders.image_recorder import ImageRecorder
from fit_mot_number import perform_analysis
from analyses.analysis import Analysis
    
    
class ImageAnalysis(Analysis): 
    pass
    
    
if __name__=="__main__": 
    
    folder = "C:\\Users\\roman\\Desktop\\Research_UTokyo\\Data\\mot"
    match = ".*ccd_detuning.*.xlsx"
    
    image_recorder = ImageRecorder(filepath=folder, match=match)
    
    