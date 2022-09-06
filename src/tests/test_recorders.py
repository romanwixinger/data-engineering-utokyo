# -*- coding: utf-8 -*-

import sys
sys.path.insert(0,'..')

import unittest

from recorders.ssd_recorder import SSDRecorder
from recorders.pmt_recorder import PMTRecorder
from recorders.coil_recorder import CoilRecorder
from recorders.gauge_recorder import GaugeRecorder
from recorders.laser_recorder import LaserRecorder
from recorders.ion_recorder import IonRecorder
from recorders.heater_recorder import HeaterRecorder


class TestRecorders(unittest.TestCase): 
    
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
        
        ]

    def test_init(self): 
        for SpecialRecorder in self.recorders: 
            recorder = SpecialRecorder()
    
    def test_get_table(self): 
        for SpecialRecorder in self.recorders: 
            recorder = SpecialRecorder()
            df = recorder.get_table()
            assert(df is not None)
    
    def test_get_data(self): 
        for SpecialRecorder in self.recorders: 
            recorder = SpecialRecorder()
            df = recorder.get_data()
            assert(df is not None)
    
    def test_get_metadata(self): 
        for SpecialRecorder in self.recorders: 
            recorder = SpecialRecorder()
            df = recorder.get_metadata()
            assert(df is not None)
    
    
if __name__ == '__main__': 
    unittest.main()
    