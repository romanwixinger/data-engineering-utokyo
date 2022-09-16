# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 10:33:23 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Utilities for finding the paths of the data, for example the many images. 
Can retrieve the newest filepath which matches a certain regex. This can safe
us from hardcoding the filepaths. 
"""


import os
import re


class PathHelper(): 
    
    @classmethod
    def get_filepaths(cls, folder: str, match: str=".*ccd_.*.xlsx"):
        """ Takes a path to a folder, loads all the filepaths and returns 
        a list of the filepaths which match. 
        """
        
        all_filepaths = cls.get_all_filepaths_in_folder(folder)
        pattern = re.compile(match)
        return [s for s in all_filepaths if pattern.match(s)]
    
    @classmethod
    def get_all_filepaths_in_folder(cls, folder: str): 
        filepaths = []
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames: 
                filepath = os.path.join(dirpath, filename)
                filepaths.append(filepath)
        return filepaths
    
    @classmethod
    def get_most_recent_filepath(cls, folder: str, match: str=".*ccd_.*.xlsx"): 
        all_filepaths = cls.get_all_filepaths_in_folder(folder)
        if not all_filepaths: 
            raise Exception("No matching filepaths found.")
        most_recent = all_filepaths[0]
        most_recent_time = cls.get_ctime(most_recent)
        for fp in all_filepaths[1:]: 
            fp_time = cls.get_ctime(fp)
            if most_recent_time < fp_time: 
                most_recent = fp
                most_recent_time = fp_time
        return most_recent
        
    @classmethod
    def get_ctime(cls, filepath: str) -> float: 
        return os.path.getctime(filepath)
    