# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 19:18:01 2020

@author: maurop
"""

import bfh
import poly


class LoadReplay:
    ''' This class loads a replay file'''
    
    def __init__(self):
        # contains the frames
        self.frames = []
        
        # marks which frame is the frame selected
        self.current_frame = 0
        
    def load_replay_file(self, filename):
        with open(filename, "rb") as f:
            bf = bfh.BinaryFile(f)
            
            n_bytes = len(f.read())
            
            print("File size:", n_bytes)
            
            while bf.co < n_bytes:
            
                # read frame
                p_list_len = bf.read("I")
                
                p_list = [poly.Polygon() for i in range(p_list_len)]
        
                for p in p_list:
                    p.interpret_bytes(bf)
            
                self.frames.append(p_list)
            
            print("Frames loaded:", len(self.frames))
    
    def next_frame(self):
        if self.current_frame + 1 < len(self.frames):
            self.current_frame += 1
            return self.frames[self.current_frame]
    
    def next_frame_wrap(self):
        if self.current_frame + 1 < len(self.frames):
            self.current_frame += 1
            return self.get_frame()
        else:
            self.current_frame = 0
            
    def previous_frame(self):
        if self.current_frame - 1 > 0:
            self.current_frame -= 1
            return self.frames[self.current_frame]        
        
    def get_frame(self):
        return self.frames[self.current_frame]