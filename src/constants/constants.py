# -*- coding: utf-8 -*-
"""File for saving the filepaths of different sources.

Create an instance with you settings here. Then assign this instance to loc, such that your other scripts use your
settings.

Todo:
    * Check if this is still in use somewhere.
"""

class Locations(object):
    """Represents the filepaths to all data sources.
    """
    
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
unittest_short_loc = Locations(
    location="../../data/unittest/", 
    ssd="../../data/unittest/"+"ssd_short.csv",
    pmt="../../data/unittest/"+"pmt_short.csv", 
    coil="../../data/unittest/"+"coil_short.txt", 
    heater="../../data/unittest/"+"heater_short.csv",
    ion="../../data/unittest/"+"ion_short.csv",
    gauge="../../data/unittest/"+"gauge_short.csv", 
    laser="../../data/unittest/"+"laser_short.lta", 
    image="../../data/unittest/"+"image_short.csv"
    )
unittest_long_loc = Locations(
    location="../../data/unittest/", 
    ssd="../../data/unittest/"+"ssd_long.csv",
    pmt="../../data/unittest/"+"pmt_long.csv", 
    coil="../../data/unittest/"+"coil_long.txt", 
    heater="../../data/unittest/"+"heater_long.csv",
    ion="../../data/unittest/"+"ion_long.csv",
    gauge="../../data/unittest/"+"gauge_long.csv", 
    laser="../../data/unittest/"+"laser_long.lta", 
    image="../../data/unittest/"+"image_long.csv"
    )


# Remote settings
remote_loc = Locations(
    gauge="../../../TPG256Monitor/TPG256GaugeMonitor_Single_DESKTOP-BEF5FI4_20220908_124458.csv",
    )

# Standard setting
loc = roman_loc


""" Plotting """

plotting_params = {
    'legend.fontsize': 'medium',
    'figure.figsize': (10, 7),
    'figure.titlesize': 'x-large',
    'axes.labelsize': 'x-large',
    'axes.titlesize': 'x-large',
    'xtick.labelsize':'medium',
    'ytick.labelsize':'medium',
    'font.size': 14
    }
