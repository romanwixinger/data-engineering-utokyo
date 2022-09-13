# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 13:31:02 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Image Analysis: Takes images from the CCD camera and generates plot and reports
from these images. The plots contain 2D gaussian fits which tell us the MOT 
number and the power. The reports are then a collection of results as a table. 
"""

import sys
sys.path.insert(0,'..')

import os
import re

from fit_mot_number import perform_analysis


class Helper(): 
    
    @classmethod
    def get_filepaths(cls, folder: str, match: str="*ccd_*.xlsx"):
        """ Takes a path to a folder, loads all the filepaths and returns 
        a list of the filepaths which match. 
        """
        
        all_filepaths = cls.get_all_filepaths_in_folder(folder)
        pattern = re.compile(".*ccd_.*.xlsx")
        return [s for s in all_filepaths if pattern.match(s)]
    
    @classmethod
    def get_all_filepaths_in_folder(cls, folder: str): 
        filepaths = []
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames: 
                filepath = os.path.join(dirpath, filename)
                filepaths.append(filepath)
        return filepaths
    
folder = "C:\\Users\\roman\\Desktop\\Research_UTokyo\\Data\\mot"
paths = Helper.get_filepaths(folder)

print(paths)