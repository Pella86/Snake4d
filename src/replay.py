# -*- coding: utf-8 -*-
"""
Created on Sun May 31 20:53:24 2020

@author: maurop
"""

# =============================================================================
# Imports
# =============================================================================

# py imports
import os
from tkinter import (IntVar, StringVar, Toplevel, Checkbutton, Button, 
                     filedialog, Label)

# project imports
import bfh
import load_replay
import rem_path
        
# =============================================================================
#  Replay settings
# =============================================================================
            
class ReplaySettings:
    
    ''' The class manages the replay settings which are a check box for 
    recording and a path to a file where the replay will get stored'''
    
    file = "./settings/replay.txt"
    
    def __init__(self):
        # Default value if the replay setting file doesn't exist
        self.record = True

        # read the replay setting file
        if os.path.isfile(self.file):
            self.read()
        
        # set up the variable bound to the check box
        self.recordvar = IntVar()
        self.recordvar.set(1 if self.record else 0)

    def display(self, frame):
        ''' Displays a checkbox that can be marked for recording '''
        
        # create a top level 
        level = Toplevel(frame)
        
        # create a radio button for the recording
        checkbox = Checkbutton(level, text = "Record", variable = self.recordvar)
        checkbox.pack()
        
        # create a label that shows when the checkbox is updated
        # display No change if isn't changed
        # display changed for 1 second if is changed
        # display no change again?
        # maybe use a check button?

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
    
    def read(self):
        ''' reads the setting file '''
        with open(self.file, "r") as f:
            lines = f.readlines()
            
        self.record = False if lines[0].split("=")[1].strip() == "False" else True
        
class Replay:
    ''' The class manages the loading and saving replays '''
    
    tmp_replay_file = "./settings/_tmp_replay_file.sk4"
    
    def __init__(self, geng):
        # controls if the users wants to record the replay
        self.replay_settings = ReplaySettings() 
        
        # the replay loading class
        self.replay = load_replay.LoadReplay()
        
        # the game engine is needed because the replay polygons can be 
        # assigned directly to the p_list of the game engine and thus rendered
        self.game = geng
        
        # state to check if the replay is playing
        self.play_state = False
       
        # shows the play/pause string
        self.str_play = StringVar()
        
        # saves the last directory used
        self.previous_save_dir = rem_path.RememberPath("save_dir", "/")
        self.previous_load_dir = rem_path.RememberPath("load_path", "/")
    
    def elaborate_path(self, filename, previous_directory):
        ''' Function that given a file name splits in path and stores it in
        the previous path and construct a replay filename'''
        
        pos = filename.rfind("/")
        
        previous_directory.assign(filename[ : pos])
        
        name = filename[pos + 1 : ]
        # check if the extention was added, if it wasnt, add the extention
        if name[::-1][0:4] != ".sk4"[::-1]:
            name += ".sk4"
        
        return os.path.join(previous_directory.get(), name)
    
    def select_save_path(self):
        ''' Prompt the user to select a path '''
        
        initdir = self.previous_save_dir.get()
        title = "Name a new file"
        extentions = (("snake4d files", ".sk4"),("all files", "*.*"))
        pathname = filedialog.asksaveasfilename(initialdir=initdir,
                                                title=title,
                                                filetypes=extentions)
        
        if pathname:
            return self.elaborate_path(pathname, self.previous_save_dir)
    
    def select_load_path(self):
        initdir = self.previous_load_dir.get()
        title = "Select a replay file"
        extentions = (("snake4d files", ".sk4"),("all files", "*.*"))
        pathname = filedialog.askopenfilename(initialdir=initdir,
                                              title=title,
                                              filetypes=extentions)
        
        if pathname:
            return self.elaborate_path(pathname, self.previous_load_dir)

    
    def reset_replay_file(self):
        # resets the replay file... it should be changed because more often 
        # than not overwrites replays
        with open(self.tmp_replay_file, "wb") as f:
            f.write(b"")        
    
    def save_replay_frame(self, geng):   
        ''' At the update game engine tick this function will append a frame
            to the file '''
        if self.replay_settings.record:
            filename = self.tmp_replay_file
            with open(filename, "ab") as fobj:
                replay_file = bfh.BinaryFile(fobj)
                geng.frame_as_bytes(replay_file)    
    
    def load_replay(self, filename):
        # add a top level to manage the replay
        
        toplevel = Toplevel()
        toplevel.title("Replay controls")
        
        # add the filename as a label
        filename = filename.replace("\\", "/")
        pos = filename.rfind("/") + 1
        name = filename[pos:]
        
        filename_label = Label(toplevel, text=name)
        filename_label.grid(row=0, columnspan=5)
        
        # add buttons allback back play/pause forward allfw
        
        b_allback = Button(toplevel, text="|<", command=self.all_back)
        b_allback.grid(row=1, column=0)
        
        b_back = Button(toplevel, text="<", command=self.back)
        b_back.grid(row=1, column=1)
        
       
        self.str_play.set("pause" if self.play_state else "play")
        
        b_play = Button(toplevel, textvariable=self.str_play, command=self.play)
        b_play.grid(row=1, column=2)
        
        b_fw = Button(toplevel, text=">", command=self.fw)
        b_fw.grid(row=1, column=3)
        
        b_allfw = Button(toplevel, text=">|", command=self.allfw)
        b_allfw.grid(row=1, column=4)
        
        # load the replay
        self.replay.load_replay_file(filename)

        # add a frame visualizer
        self.frame_number_var = StringVar()
        
        frame_number_label = Label(toplevel, textvariable=self.frame_number_var)
        frame_number_label.grid(row=2, column=0, columnspan=5)
        
        self.update_frame_number()

    def update_frame_number(self):
       tot_frames = len(self.replay.frames)
       current_frame = self.replay.current_frame + 1
       s = f"Frame: {current_frame}/{tot_frames}"
       self.frame_number_var.set(s)

    def tmp_replay_file_is_empty(self):
        with open(self.tmp_replay_file, "rb") as f:
            nbytes = len(f.read())    
        return nbytes == 0
    
    def set_plist(self, p_list):
        if p_list:
            self.game.p_list = p_list
            self.update_frame_number()
            
    # commands to control the replay
    # all back, back 1, play/pause, forward 1, all forward
  
    def all_back(self):
        self.replay.current_frame = 0
        
        p_list = self.replay.get_frame()
        
        self.set_plist(p_list)
        self.update_frame_number()
    
    def back(self):
        p_list = self.replay.previous_frame()
        self.set_plist(p_list)
        
    def play(self):
        # toggle the play state
        if self.play_state:
            self.play_state = False
        else:
            self.play_state = True
        
        self.str_play.set("pause" if self.play_state else "play")
        
    
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
        


