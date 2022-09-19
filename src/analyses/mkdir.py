# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 14:30:58 2022

@author: Roman Wixinger (roman.wixinger@gmail.com)

Test for creating folders. 
"""

import os

def create_folders(plot_path: str, result_path: str): 
    if not os.path.isdir(plot_path): 
        os.mkdir(plot_path)
        os.mkdir(plot_path + "ssd/")
        os.mkdir(plot_path + "image/")
        
    if not os.path.isdir(result_path): 
        os.mkdir(result_path)
        

def mkdir_if_not_exist(path: str): 
    if not os.path.isdir(path): 
        os.mkdir(path)
        