# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 11:31:17 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Simulation analysis. 
"""


import sys
sys.path.insert(0,'../..')  # Set src as top-level
 
import pandas as pd

from src.recorders.simulation_recorder import SimulationRecorder
from src.analyses.analysis import Analysis


class SimulationAnalysis(Analysis): 
    