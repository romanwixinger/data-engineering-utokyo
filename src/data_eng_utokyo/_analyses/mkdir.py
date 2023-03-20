# -*- coding: utf-8 -*-
""" Functionality for creating folders.
"""

import os


def create_folders(plot_path: str, result_path: str):
    """Creates folders to save results to.

    Also create two subfolders with names ssd and image.

    Args:
        plot_path (str): Path at which the plots should be saved later.
        result_path (str): Path at which the results should be saved later.
    """
    if not os.path.isdir(plot_path): 
        os.mkdir(plot_path)
        os.mkdir(plot_path + "ssd/")
        os.mkdir(plot_path + "image/")
        
    if not os.path.isdir(result_path): 
        os.mkdir(result_path)

    return
        

def mkdir_if_not_exist(path: str):
    """ Creates a folder at path if the folder does not already exist.

    Args:
        path (str): The full path of the folder that should be created.
    """
    if not os.path.isdir(path): 
        os.mkdir(path)
    return
