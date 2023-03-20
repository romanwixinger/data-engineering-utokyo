# -*- coding: utf-8 -*-
"""Combines all results of an analysis cycle.

The CycleRecorder combines all results of a cycle, namely 

- Image data (MOT number via MLE)
- SSD data (MOT number via peak) 
- Cycle data (Parameters which were set) 

The recorder can then by used in the CycleAnalysis, which allows us to explore
dependencies of the MOT number. 

Todo: 
    * Implement the CycleRecorder.
"""

from .recorder import Recorder


class CycleRecorder(Recorder): 
    """ Tracks all results and combines them into one dataframe. 
    """ 
    pass
    
    


