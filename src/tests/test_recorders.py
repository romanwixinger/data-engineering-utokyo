# -*- coding: utf-8 -*-

import sys
sys.path.insert(0,'..')

import unittest
import pandas as pd

from constants import unittest_loc

from recorders.ssd_recorder import SSDRecorder
from recorders.pmt_recorder import PMTRecorder
from recorders.coil_recorder import CoilRecorder
from recorders.gauge_recorder import GaugeRecorder
from recorders.laser_recorder import LaserRecorder
from recorders.ion_recorder import IonRecorder
from recorders.heater_recorder import HeaterRecorder


recorders = [
    SSDRecorder,
    PMTRecorder,
    CoilRecorder,
    GaugeRecorder,
    LaserRecorder,
    IonRecorder,
    HeaterRecorder
    ]

paths = [
    unittest_loc.ssd,
    unittest_loc.pmt,
    unittest_loc.coil,
    unittest_loc.gauge,
    unittest_loc.laser,
    unittest_loc.ion,
    unittest_loc.heater
    ]


class Helper(): 
    
    @classmethod
    def get_nr_of_rows(cls, df: pd.DataFrame): 
        return len(df.index)

class TestRecorders(unittest.TestCase): 
        
    def test_init(self): 
        for SpecialRecorder, filepath in zip(recorders, paths): 
            recorder = SpecialRecorder(filepath)
      
    def test_get_table(self): 
        for SpecialRecorder, filepath in zip(recorders, paths): 
            recorder = SpecialRecorder(filepath)
            df = recorder.get_table()
            assert(df is not None)
            assert(Helper.get_nr_of_rows(df) == 5)

    
    def test_get_data(self): 
        for SpecialRecorder, filepath in zip(recorders, paths): 
            recorder = SpecialRecorder(filepath)
            df = recorder.get_data()
            assert(df is not None)
            assert(Helper.get_nr_of_rows(df) == 5)
    
    def test_get_metadata(self): 
        for SpecialRecorder, filepath in zip(recorders, paths): 
            recorder = SpecialRecorder(filepath)
            df = recorder.get_metadata()
            assert(df is not None)
            assert(Helper.get_nr_of_rows(df) in [0,1])
    
    
if __name__ == '__main__': 
    unittest.main()
    