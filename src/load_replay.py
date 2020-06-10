# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 19:18:01 2020

@author: maurop
"""

import bfh
import poly

def str_file_size(size):
    ''' Puts the file size in the 1 kb format instead of 1000 b'''
    
    # Size limits in bytes 
    limits = [1, 1e3, 1e6, 1e9, 1e12]
    
    # Corresponding letters
    letters = ["", "K", "M", "G", "T"]
    
    # Fuse the two and invert the list
    sizes = list(zip(limits, letters))[::-1]
    
    # start from the bigger till one finds an appropriate limit
    for limit, letter in sizes:
        value = size / limit
        if value >= 1:
            value = size / limit
            if letter:
                return f"{value:.1f} {letter}b"
            else:
                value = int(value)
                return f"{value} b"
    
    value = int(size)
    return f"{value} b"


class LoadReplay:
    ''' This class loads a replay file'''
    
    def __init__(self):
        # contains the frames
        self.frames = []
        
        # marks which frame is the frame selected
        self.current_frame = 0
        
    def load_replay_file(self, filename):
        ''' Loads the replay file and appends it to the frames'''
        self.frames = []
        
        with open(filename, "rb") as f:
            bf = bfh.BinaryFile(f)
            
            n_bytes = len(f.read())
            
            print("Replay file size:", str_file_size(n_bytes))
            
            while bf.co < n_bytes:
            
                # read frame
                p_list_len = bf.read("I")
                
                p_list = [poly.Polygon() for i in range(p_list_len)]
        
                for p in p_list:
                    p.interpret_bytes(bf)
            
                self.frames.append(p_list)
            
            print("Frames loaded:", len(self.frames))
    
    def next_frame(self):
        ''' increments the frame and returns the current frame'''
        if self.current_frame + 1 < len(self.frames):
            self.current_frame += 1
            return self.get_frame()
    
    def next_frame_wrap(self):
        ''' Wraps around the end to start back, used in the play/pause 
        animation'''
        if self.current_frame + 1 < len(self.frames):
            self.current_frame += 1
            return self.get_frame()
        else:
            self.current_frame = 0
            
    def previous_frame(self):
        ''' decrements the frame and returns the current frame'''
        if self.current_frame - 1 > 0:
            self.current_frame -= 1
            return self.get_frame()    
        
    def get_frame(self):
        ''' gets the current frame'''
        return self.frames[self.current_frame]