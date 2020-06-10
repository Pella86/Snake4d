# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 17:44:37 2020

@author: maurop
"""

import os


class RememberPath:
    
    ''' This class serves as a database for the open/save file path, 
    it remembers which was the last directory used'''
    
    #File where path are stored
    paths_file = "./settings/paths.txt"
    
    # class attribute dictionary storing the paths
    paths = {}

    def __init__(self, name, path):
        ''' creates a path checking if is already present in the file'''
        
        # read the file 
        if os.path.isfile(self.paths_file):
            self.read()
           
        # add if is a new path
        self.add_path(name, path)
        
        # internal variable identfying the path
        self.name = name
        
    def add_path(self, name, path):
        ''' Append path and append it to the file, if is not present
        in the file '''
        
        if self.paths.get(name) == None:
            self.paths[name] = path
            self.write()
    
    def get(self):
        return self.paths[self.name]
    
    
    def assign(self, path):
        ''' assign a new path to the name, then update the file '''
        self.paths[self.name] = path
        self.write()
    
    def read(self):
        with open(self.paths_file, "r") as f:
            lines = f.readlines()
            
        for line in lines:
            parts = line.split("=")
            self.paths[parts[0].strip()] = parts[1].strip()
    
    def write(self):
        with open(self.paths_file, "w") as f:
            for name, path in self.paths.items():
                f.write(f"{name}={path}\n")