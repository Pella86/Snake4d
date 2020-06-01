# -*- coding: utf-8 -*-
"""
Created on Sun May 31 20:53:24 2020

@author: maurop
"""

# =============================================================================
# Imports
# =============================================================================

import os
from tkinter import (IntVar, StringVar, Toplevel, Checkbutton, Label, Button, 
                     filedialog)

import bfh
import poly

# =============================================================================
#  Replay settings
# =============================================================================

# define a switch that can be controlled if replay are saved or not

# define a folder and a file name for the replay
            
class ReplaySettings:
    
    ''' The class manages the replay settings which are a check box for 
    recording and a path to a file where the replay will get stored'''
    
    file = "./settings/replay.txt"
    tmp_replay_file = "./settings/_tmp_replay_file.sk4"
    
    def __init__(self):
        # Default values if the replay setting file doesn't exist
        self.record = False
        self.previous_path = ""
        
        # read the replay setting file
        if os.path.isfile(self.file):
            self.read()
        
        # set up the variable bound to the check box
        self.recordvar = IntVar()
        self.recordvar.set(1 if self.record else 0)

    def display(self, frame):
        
        # create a top level 
        level = Toplevel(frame)
        
        # create a radio button for the recording
        checkbox = Checkbutton(level, text = "Record", variable = self.recordvar)
        checkbox.pack()
        
    
        
    
    def select_path(self):
        ''' Prompt the user to select a path '''
        
        initdir = self.previous_path if self.previous_path else "/"
        title = "Name a new file"
        extentions = (("snake4d files", ".sk4"),("all files", "*.*"))
        path = filedialog.asksaveasfilename(initialdir=initdir,
                                            title=title,
                                            filetypes=extentions)
        
        if path:
            # break the path down 
            pos = path.rfind("/")
            
            self.previous_path = path[ : pos]
            name = path[pos + 1 : ]
            if name[::-1][0:4] != ".sk4"[::-1]:
                name += ".sk4"
                
            self.save()
            
            return os.path.join(self.previous_path, name)
    

    def read_state(self):
        ''' This function reads the check box and updates the settings 
            accordingly
        '''
        if self.recordvar.get() == 1:
            current_record_state = True
        else:
            current_record_state = False
            
        if current_record_state != self.record:
            self.record = current_record_state
            self.save()
        
    def save(self):
        ''' saves the setting file overwriting it'''
        with open(self.file, "w") as f:
            f.write("record=" + str(self.record) + "\n")
            f.write("path=" + self.previous_path + "\n")
    
    def read(self):
        ''' reads the setting file '''
        with open(self.file, "r") as f:
            lines = f.readlines()
            
        self.record = False if lines[0].split("=")[1].strip() == "False" else True
        self.previous_path = lines[1].split("=")[1].strip()
        
        if not os.path.isdir(self.previous_path):
            self.path = "."
            self.save()

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

class Replay:
    ''' The class manages the loading and saving replays '''
    
    def __init__(self, geng):
        self.replay_settings = ReplaySettings() 
        
        self.replay = LoadReplay()
        
        self.game = geng
        
        self.play_state = False
       
        self.str_play = StringVar()
    
    def reset_replay_file(self):
        # resets the replay file... it should change because more often than
        # not overwrites replays
        with open(self.replay_settings.tmp_replay_file, "wb") as f:
            f.write(b"")        
    
    def save_replay_frame(self, geng):   
        # At the update game engine tick this function will append a frame
        # to the file
        if self.replay_settings.record:
            filename = self.replay_settings.tmp_replay_file
            with open(filename, "ab") as fobj:
                replay_file = bfh.BinaryFile(fobj)
                geng.frame_as_bytes(replay_file)    
    
    def load_replay(self, filename):
        # add a top level to manage the replay
        
        toplevel = Toplevel()
        
        # add buttons allback back play/pause forward allfw
        
        b_allback = Button(toplevel, text="|<", command=self.all_back)
        b_allback.grid(row=0, column=0)
        
        b_back = Button(toplevel, text="<", command=self.back)
        b_back.grid(row=0, column=1)
        
       
        self.str_play.set("play" if self.play_state else "pause")
        
        b_play = Button(toplevel, textvariable=self.str_play, command=self.play)
        b_play.grid(row=0, column=2)
        
        b_fw = Button(toplevel, text=">", command=self.fw)
        b_fw.grid(row=0, column=3)
        
        b_allfw = Button(toplevel, text=">|", command=self.allfw)
        b_allfw.grid(row=0, column=4)
        
        
        self.replay.load_replay_file(filename)
    
    
    def set_plist(self, p_list):
        if p_list:
            self.game.p_list = p_list
  
    def all_back(self):
        self.replay.current_frame = 0
        
        p_list = self.replay.get_frame()
        
        self.set_plist(p_list)
    
    def back(self):
        p_list = self.replay.previous_frame()
        self.set_plist(p_list)
        
    def play(self):
        # toggle the play state
        if self.play_state:
            self.play_state = False
        else:
            self.play_state = True
        
        self.str_play.set("play" if self.play_state else "pause")
        
    
    def fw(self):
        p_list = self.replay.next_frame()
        self.set_plist(p_list)
    
    def allfw(self):
        self.replay.current_frame = len(self.replay.frames) - 1
        p_list = self.replay.get_frame()
        self.set_plist(p_list)
    
    def play_frames(self):
        
        # make sure something is loaded
        if self.replay.frames:
            
            if self.play_state:
                
                p_list = self.replay.next_frame_wrap()
                self.set_plist(p_list)
        
        