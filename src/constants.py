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
                 location: str="",
                 ssd: str="",
                 pmt: str="",
                 coil: str="",
                 heater: str="",
                 ion: str="",
                 gauge: str="",
                 laser: str="",
                 image: str="",
                 ): 
    
        self.location = "../data/"
        self.ssd = ssd
        self.pmt = pmt
        self.coil = coil
        self.heater = heater
        self.ion = ion
        self.gauge = gauge
        self.laser = laser
        self.image = image
        
                
""" Instances """

# Romans settings
roman_loc = Locations(
    location="../../data/sample/",
    ssd="../../data/sample/"+"-20220314-100806-Slot1-In2.csv",
    pmt="../../data/sample/"+"all_data.csv",
    coil="../../data/sample/"+"coil_log.txt",
    heater="../../data/sample/"+"HeaterLog_20220314_100740_00001.csv",
    ion="../../data/sample/"+"IonBeamControl1.5_DESKTOP-8ICG2TJ_20220314_114132.csv",
    gauge="../../data/sample/"+"TPG256GaugeMonitor_Single_DESKTOP-BEF5FI4_20220312_203214.csv",
    laser="../../data/sample/"+"15.03.2022, 21.30, 384.22817013 THz.lta",
    image="../../data/sample/"+"cmos_000039.csv"
    )

# Unittest settings
unittest_loc = Locations(
    location="../../data/unittest/", 
    ssd="../../data/unittest/"+"ssd.csv",
    pmt="../../data/unittest/"+"pmt.csv", 
    coil="../../data/unittest/"+"coil.txt", 
    heater="../../data/unittest/"+"heater.csv",
    ion="../../data/unittest/"+"ion.csv", 
    gauge="../../data/unittest/"+"gauge.csv", 
    laser="../../data/unittest/"+"laser.lta", 
    image="../../data/unittest/"+"image.csv"
    )

# Remote settings
remote_loc = Locations(
    gauge="../../../TPG256Monitor/TPG256GaugeMonitor_Single_DESKTOP-BEF5FI4_20220908_124458.csv",
    )

# Standard setting
loc = roman_loc
