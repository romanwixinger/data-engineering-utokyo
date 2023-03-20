# -*- coding: utf-8 -*-
"""Finds the paths of the data, for example the many images created with the CMOS camera.

Can retrieve the newest filepath which matches a certain regex. This can safe us from hardcoding the filepaths.
"""

import os
import re


class PathHelper(object):
    
    @classmethod
    def get_filepaths(cls, folder: str, match: str=".*ccd_.*.xlsx") -> list:
        """Takes a path to a folder, loads all the filepaths and returns a list of the filepaths which match.

        Args:
            folder (str): Path to the folder in which we look for files.
            match (str): Regex string that the files should match.

        Returns:
            List of the matching filepaths in the folder.
        """
        
        all_filepaths = cls.get_all_filepaths_in_folder(folder)
        pattern = re.compile(match)
        return [s for s in all_filepaths if pattern.match(s)]
    
    @classmethod 
    def get_folders(cls, folder: str, match: str=".*ccd_.*.xlsx"): 
        """Finds matching files, and then returns all folder which are exactly two levels above of these files.

        Takes a filepath to a folder, loads all filepaths to files that match and return a list of the unique folders
        (two levels above) in which they were found. This method can be used to find the metadata (all_data.csv) of
        csv files.

        Args:
            folder (str): Initial folder in which the files should be searched.
            match (str): Regex which the files have to match.

        Returns:
            A list of the unique folders which are exactly two levels above at least one file which was matched.
        """
        
        all_filepaths = cls.get_all_filepaths_in_folder(folder)
        pattern = re.compile(match)
        filepaths = [s for s in all_filepaths if pattern.match(s)]
        print(filepaths)
        folder_set = set((os.path.dirname(os.path.dirname(os.path.dirname(fp))) for fp in filepaths))
        return list(folder_set)
        
    @classmethod
    def get_all_filepaths_in_folder(cls, folder: str):
        """Returns all filepaths of files in a folder.

        Args:
            folder (str): Initial folder in which the files are searched.

        Returns:
            List of the full filepaths of these files.
        """
        filepaths = []
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames: 
                filepath = os.path.join(dirpath, filename)
                filepaths.append(filepath)
        return filepaths
    
    @classmethod
    def get_most_recent_filepath(cls, folder: str, match: str=".*ccd_.*.xlsx"):
        """
        Todo:
            * Check and document what this method does.
        """
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
        """ Returns the creation time of an object.

        Args:
            filepath (str): Path of the file.

        Returns:
            Time that passed between file creation and the last epoch as given in seconds as float number.
        """
        return os.path.getctime(filepath)
