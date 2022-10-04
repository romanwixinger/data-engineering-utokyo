# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 20:14:22 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

The CycleRecorder combines all results of a cycle, namely 

- Image data (MOT number via MLE)
- SSD data (MOT number via peak) 
- Cycle data (Parameters which were set) 

The recorder can then by used in the CycleAnalysis, which allows us to explore
dependencies of the MOT number. 
"""

import sys
sys.path.insert(0,'../..')  # Set src as top-level

from src.recorders.recorder import Recorder
from src.recorders.result_recorder import Recorder, SSDResultsRecorder, ImageResultsRecorder, ParameterRecorder


class CycleRecorder(Recorder): 
    """ Tracks all results and combines them into one dataframe. 
    """ 
    
    


