# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 11:31:17 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Simulation analysis. 
"""


import sys
sys.path.insert(0,'..')

import pandas as pd

from recorders.simulation_recorder import SimulationRecorder
from analyses.analysis import Analysis


class SimulationAnalysis(Analysis): 
    