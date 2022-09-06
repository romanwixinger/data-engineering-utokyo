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
                 location: str,
                 ssd: str,
                 pmt: str,
                 coil: str,
                 heater: str,
                 ion: str,
                 gauge: str,
                 laser: str,
                 image: str,
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
roman_loc = Locations(
    location="../../data/sample/",
    ssd="-20220314-100806-Slot1-In2.csv",
    pmt="all_data.csv",
    coil="coil_log.txt",
    heater="HeaterLog_20220314_100740_00001.csv",
    ion="IonBeamControl1.5_DESKTOP-8ICG2TJ_20220314_114132.csv",
    gauge="TPG256GaugeMonitor_Single_DESKTOP-BEF5FI4_20220312_203214.csv",
    laser="15.03.2022, 21.30, 384.22817013 THz.lta",
    image="cmos_000039.csv"
    )

# Unittest settings
unittest_loc = Locations(
    location="../../data/unittest/", 
    ssd="ssd.csv",
    pmt="pmt.csv", 
    coil="coil.txt", 
    heater="heater.csv",
    ion="ion.csv", 
    gauge="gauge.csv", 
    laser="laser.lta", 
    image="image.csv"
    )


# Standard setting
loc = roman_loc
