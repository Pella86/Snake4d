# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 17:44:37 2020

@author: maurop
"""

import os


class RememberPath:
    
    paths_file = "./settings/paths.txt"
    #paths_file = "./paths.txt"
    paths = {}

    def __init__(self, name, path):
        # read the file 
        if os.path.isfile(self.paths_file):
            self.read()
           
        # add if is a new path
        self.add_path(name, path)
        
        # internal variable identfying the path
        self.name = name
        
    def add_path(self, name, path):
        # append path and append it to the file, if is not present in the file
        if self.paths.get(name) == None:
            self.paths[name] = path
            self.write()
    
    def get(self):
        return self.paths[self.name]
    
    
    def assign(self, path):
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