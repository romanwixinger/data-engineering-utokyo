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

names = [
    "ssd",
    "pmt",
    "coil",
    "gauge",
    "laser",
    "ion",
    "heater"
    ]


class Helper(): 
    
    @classmethod
    def get_nr_of_rows(cls, df: pd.DataFrame): 
        return len(df.index)

    @classmethod
    def try_except_wrapper(cls, func, message): 
        try: 
            func()
        except Exception as e: 
            message = message + f": {e}"
            raise Exception(message)
        return
            
    @classmethod
    def _simulate_adding_rows(cls, recorder, n: int): 
        """ Sets the counter back such that the reader reads the last part of
            the csv again. 
        """
        recorder.read_data_lines = recorder.read_data_lines - n
        recorder.last_updated = 0
        return


class TestRecorders(unittest.TestCase): 
        
    def test_init(self): 
        for SpecialRecorder, filepath in zip(recorders, paths): 
            recorder = SpecialRecorder(filepath)
      
    def test_get_table(self): 
        for SpecialRecorder, filepath, name in zip(recorders, paths, names): 
             recorder = SpecialRecorder(filepath)
             Helper.try_except_wrapper(
                 func=recorder.get_table,
                 message=f"test_get_table() failed for {SpecialRecorder}"
            ) 

    def test_get_table_nr(self): 
        for SpecialRecorder, filepath, name in zip(recorders, paths, names): 
             recorder = SpecialRecorder(filepath)
             df = recorder.get_table()
             n = Helper.get_nr_of_rows(df) 
             assert n == 6, f"test_get_table_nr() failed for {SpecialRecorder}: Found {n} instead of 6"

    def test_get_data(self): 
        for SpecialRecorder, filepath, name in zip(recorders, paths, names): 
             recorder = SpecialRecorder(filepath)
             Helper.try_except_wrapper(
                 func=recorder.get_data,
                 message=f"test_get_data() failed for {SpecialRecorder}"
            ) 
    
    def test_get_data_nr(self): 
        for SpecialRecorder, filepath, name in zip(recorders, paths, names): 
             recorder = SpecialRecorder(filepath)
             df = recorder.get_data()
             n = Helper.get_nr_of_rows(df) 
             assert n == 6, f"test_get_data_nr() failed for {SpecialRecorder}: Found {n} instead of 6"
    
    def test_get_metadata(self): 
        for SpecialRecorder, filepath, name in zip(recorders, paths, names): 
             recorder = SpecialRecorder(filepath)
             Helper.try_except_wrapper(
                 func=recorder.get_metadata,
                 message=f"test_get_metadata() failed for {SpecialRecorder}"
            )
        return
        
    def test_get_metadata_nr(self):  
        for SpecialRecorder, filepath, name in zip(recorders, paths, names): 
            recorder = SpecialRecorder(filepath)
            df = recorder.get_metadata()
            n = Helper.get_nr_of_rows(df)
            assert n in [0,1], "test_get_metadata_nr() failed with n={n}."
            
    def test_refresh(self):
        """ Test the case when the csv is modified and we load the new data.
        """
        
        for SpecialRecorder, filepath, name in zip(recorders, paths, names):
            set_back_n_rows = 6 if SpecialRecorder == LaserRecorder else 3
            recorder = SpecialRecorder(filepath=filepath, always_update=True) 
            n = Helper.get_nr_of_rows(recorder.get_table())
            Helper._simulate_adding_rows(recorder, set_back_n_rows)
            m = Helper.get_nr_of_rows(recorder.get_table())
            assert m - n == (6/6 if SpecialRecorder == LaserRecorder else 3), f"test_refresh() with {SpecialRecorder} failed: n={n}, m={m}."
        
    
if __name__ == '__main__': 

    unittest.main()
    