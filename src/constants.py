# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 17:13:32 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

File for global constants. Create an instance with you settings here. Then 
assign this instance to loc, such that your other scripts use your settings. 
"""

class Locations(): 
    
    @classmethod
    def __init__(self, 
                 location: str="../../data/",
                 ssd: str="-20220314-100806-Slot1-In2.csv",
                 pmt: str="all_data.csv",
                 coil: str="coil_log.txt",
                 heater: str="HeaterLog_20220314_100740_00001.csv",
                 ion: str="IonBeamControl1.5_DESKTOP-8ICG2TJ_20220314_114132.csv",
                 gauge: str="TPG256GaugeMonitor_Single_DESKTOP-BEF5FI4_20220312_203214.csv",
                 laser: str="15.03.2022, 21.30, 384.22817013 THz.lta",
                 image: str="cmos_000039.csv"
                 ): 
    
        self.location = "../data/"
        self.ssd = location + ssd
        self.pmt = location + pmt
        self.coil = location + coil
        self.heater = location + heater
        self.ion = location + ion
        self.gauge = location + gauge
        self.laser = location + laser
        self.image = location + image
        
        
""" Instances """

# Romans settings
roman_loc = Locations()


# Standard setting
loc = roman_loc
