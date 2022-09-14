# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0,'..')

import unittest
import pandas as pd
from shutil import copy

from constants import unittest_short_loc, unittest_long_loc

from recorders.ssd_recorder import SSDRecorder
from recorders.pmt_recorder import PMTRecorder
from recorders.coil_recorder import CoilRecorder
from recorders.gauge_recorder import GaugeRecorder
from recorders.laser_recorder import LaserRecorder
from recorders.ion_recorder import IonRecorder
from recorders.heater_recorder import HeaterRecorder


n = 6
m = 7
recorders = [
    SSDRecorder,
    PMTRecorder,
    CoilRecorder,
    GaugeRecorder,
    LaserRecorder,
    IonRecorder,
    HeaterRecorder
    ][n:m]

short_paths = [
    unittest_short_loc.ssd,
    unittest_short_loc.pmt,
    unittest_short_loc.coil,
    unittest_short_loc.gauge,
    unittest_short_loc.laser,
    unittest_short_loc.ion,
    unittest_short_loc.heater
    ][n:m]

long_paths = [
    unittest_long_loc.ssd,
    unittest_long_loc.pmt,
    unittest_long_loc.coil,
    unittest_long_loc.gauge,
    unittest_long_loc.laser,
    unittest_long_loc.ion,
    unittest_long_loc.heater
    ][n:m]

names = [
    "ssd",
    "pmt",
    "coil",
    "gauge",
    "laser",
    "ion",
    "heater"
    ][n:m]


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
    def simulate_adding_rows(cls, recorder, n: int): 
        """ Sets the counter back such that the reader reads the last part of
            the csv again. 
        """
        recorder.read_data_lines = recorder.read_data_lines - n
        recorder.last_updated = 0
        return
    
    @classmethod
    def generate_a_filepath_for_copy(cls, filepath) -> str:
        split = os.path.splitext(filepath)
        assert(len(split) == 2) 
        prefix = split[0]
        postfix = split[1]
        return prefix + "_copy" + postfix


class TestRecorders(unittest.TestCase): 
        
    def test_init(self): 
        for SpecialRecorder, filepath in zip(recorders, short_paths): 
            recorder = SpecialRecorder(filepath)
      
    def test_get_table(self): 
        for SpecialRecorder, filepath, name in zip(recorders, short_paths, names): 
             recorder = SpecialRecorder(filepath)
             Helper.try_except_wrapper(
                 func=recorder.get_table,
                 message=f"test_get_table() failed for {SpecialRecorder}"
            ) 

    def test_get_table_nr(self): 
        for SpecialRecorder, filepath, name in zip(recorders, short_paths, names): 
             recorder = SpecialRecorder(filepath)
             df = recorder.get_table()
             n = Helper.get_nr_of_rows(df) 
             assert n == 18, f"test_get_table_nr() failed for {SpecialRecorder}: Found {n} instead of 6"
             
    def test_get_data(self): 
        for SpecialRecorder, filepath, name in zip(recorders, short_paths, names): 
             recorder = SpecialRecorder(filepath)
             Helper.try_except_wrapper(
                 func=recorder.get_data,
                 message=f"test_get_data() failed for {SpecialRecorder}"
            ) 

    def test_get_data_nr(self): 
        for SpecialRecorder, filepath, name in zip(recorders, short_paths, names): 
             recorder = SpecialRecorder(filepath)
             df = recorder.get_data()
             n = Helper.get_nr_of_rows(df) 
             assert n == 18, f"test_get_data_nr() failed for {SpecialRecorder}: Found {n} instead of 18"

    def test_get_data(self): 
        for SpecialRecorder, filepath, name in zip(recorders, short_paths, names): 
             recorder = SpecialRecorder(filepath)
             Helper.try_except_wrapper(
                 func=recorder.get_data,
                 message=f"test_get_data() failed for {SpecialRecorder}"
            ) 
    
    def test_get_data_nr(self): 
        for SpecialRecorder, filepath, name in zip(recorders, short_paths, names): 
             recorder = SpecialRecorder(filepath)
             df = recorder.get_data()
             n = Helper.get_nr_of_rows(df) 
             assert n == 18, f"test_get_data_nr() failed for {SpecialRecorder}: Found {n} instead of 6"
    def test_get_metadata(self): 
        for SpecialRecorder, filepath, name in zip(recorders, short_paths, names): 
             recorder = SpecialRecorder(filepath)
             Helper.try_except_wrapper(
                 func=recorder.get_metadata,
                 message=f"test_get_metadata() failed for {SpecialRecorder}"
            )
        return
    
    def test_get_metadata_nr(self):  
        for SpecialRecorder, filepath, name in zip(recorders, short_paths, names): 
            recorder = SpecialRecorder(filepath)
            df = recorder.get_metadata()
            n = Helper.get_nr_of_rows(df)
            assert n in [0,1], "test_get_metadata_nr() failed with n={n}."
            
    def test_mock_refresh(self):
        """ Test the case when the csv is modified and we load the new data.
            In this version, we do not modify the csv file, but we just reset
            the counters. 
        """
        
        for SpecialRecorder, filepath, name in zip(recorders, short_paths, names):
            set_back_n_rows = 12 if SpecialRecorder == LaserRecorder else 6
            recorder = SpecialRecorder(filepath=filepath, always_update=True) 
            n = Helper.get_nr_of_rows(recorder.get_table())
            Helper.simulate_adding_rows(recorder, set_back_n_rows)
            m = Helper.get_nr_of_rows(recorder.get_table())
            assert m - n == (12/6 if SpecialRecorder == LaserRecorder else 6/1), f"test_refresh() with {SpecialRecorder} failed: n={n}, m={m}."
            
    def test_simulate_refresh(self):
         """ Test the case when the csv is modified and we load the new data.
             In this version, we actually generate a copy of the file and 
             modify over the course of the unit test. 
         """
         
         for SpecialRecorder, short_fp, long_fp, name in zip(recorders, short_paths, long_paths, names):
             # Setup copy 
             copy_filepath = Helper.generate_a_filepath_for_copy(short_fp)
             copy(short_fp, copy_filepath)
             
             # Setup recorder and evaluate
             recorder = SpecialRecorder(filepath=copy_filepath, always_update=True) 
             n = Helper.get_nr_of_rows(recorder.get_table())
             
             # Update csv and evaluate
             copy(long_fp, copy_filepath)
             m = Helper.get_nr_of_rows(recorder.get_table())
             
             # Delete copy
             os.remove(copy_filepath)
             
             # Sanity check
             assert m > n, f"test_refresh() with {SpecialRecorder} failed: n={n}, m={m}."
             
    def test_10x_get_table(self):
        for SpecialRecorder, path in zip(recorders, short_paths):
            recorder = SpecialRecorder(filepath=path)
            for i in range(10):
                df = recorder.get_table()
                


    
    
if __name__ == '__main__': 

    unittest.main()
    