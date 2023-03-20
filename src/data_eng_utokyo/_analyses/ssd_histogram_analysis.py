# -*- coding: utf-8 -*-
"""Analysis for creating SSD Histograms
"""

import matplotlib.pyplot as plt

from .._recorders.ssd_recorder import SSDRecorder, SSDParser
from .analysis import Analysis
from .._utilities.general_constants import plotting_params
plt.rcParams.update(plotting_params)


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
