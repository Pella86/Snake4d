# -*- coding: utf-8 -*-
"""
Created on Thu May 17 13:20:44 2018

@author: Mauro
"""

# import sys to access the src folder
import sys
sys.path.append("./src")

# py imports
import time
import datetime
import os

# GUI stuff
from tkinter import (Tk, _tkinter, StringVar, Label, Menu, Toplevel, IntVar,
                     Checkbutton, filedialog, Button)

# project imports
import visu
import g_eng
import score
import bfh
import poly



#==============================================================================
# # TO DO list
#==============================================================================

# insert a option to save the files

#==============================================================================
# Help message
#==============================================================================

INFO_TEXT = '''*****************snake 4d*****************\n
Rules:                                 \n
    1. eat the food (blue cube)        \n
    2. don't hit the walls (black)     \n
    3. don't cross yourself (green)    \n
                                       \n
How to play:                           \n
      W             I                  \n
     ASD           JKL                 \n
These keys control the SNAKE in the 6  \n
directions:                            \n
                                       \n
W = UP                                 \n
A = RIGHT                              \n
S = DOWN                               \n
D = LEFT                               \n
I = OUT                                \n
J = FORWARD                            \n
K = IN                                 \n
L = REVERSE                            \n
                                       \n
To control the CAMERA use:             \n
  Y, X, C to control 3d rotations       \n
  V, B, N, M, T or Z to control 4d     \n
  rotations                            \n
**********************************************\n'''

#==============================================================================
# Key buffer
#==============================================================================

class KeyBuffer:
    '''
    Key Buffer

    is a simple buffer that keeps track of the key pressed while playing
    it makes a more fluid control of the snake when the game lags.

    Methods:
        __init__
        push_key
        get_key
        clear

    Instance variables:
        self.buf -- a simple list doing the job of a LIFO stack
        self.key_to_dir -- transforms the key in directions
    '''

    def __init__(self):
        '''
        class is initialised with a buffer, and a dictionary that will
        convert the keys to directions
        '''

        self.buf = []

        # construct the dictionary that changes the snake direction
        self.key_to_dir = {}
        bind_key = ["w", "s", "a", "d", "i", "k", "j", "l"]
        possible_dirs = ["UP", "DOWN", "LEFT", "RIGHT", "FW", "RW", "IN", "OUT"]

        for direction, key in zip(possible_dirs, bind_key):
            self.key_to_dir[key] = direction

    def push_key(self, key):
        '''
        insert the key in the buffer

        Keyword arguments:
        key -- can be any character
        '''

        self.buf.append(key)

    def get_key(self):
        '''gets the next key, if none is found returns None'''

        if self.buf:
            return self.key_to_dir[self.buf.pop(0)]
        else:
            return None

    def clear(self):
        '''Just empties the buffer'''

        self.buf = []

#==============================================================================
# Rate class
#   for update rate, fps, ...
#==============================================================================

class Rate:
    '''
    Rate

    small class to manage fps and various update rates
    '''

    def __init__(self, rate):
        '''Initialize the rate calling for the time function

        Keyword argument:
        rate -- is a float representing 1/s frame rate
        '''

        self.rate = rate
        self.init_time = time.time()

    def is_time(self):
        '''Returns true if the current time surpasses the rate'''

        if time.time() - self.init_time > self.rate:
            self.init_time = time.time()
            return True
        else:
            return False
        
# =============================================================================
#  Replay settings
# =============================================================================

# define a switch that can be controlled if replay are saved or not

# define a folder and a file name for the replay
            
class ReplaySettings:
    
    ''' The class manages the replay settings which are a check box for 
    recording and a path to a file where the replay will get stored'''
    
    file = "./settings/replay.txt"
    
    def __init__(self):
        # Default values if the replay setting file doesn't exist
        self.record = False
        self.path = "."
        self.name = ""
        
        # read the replay setting file
        if os.path.isfile(self.file):
            self.read()
        
        # set up the variable bound to the check box
        self.recordvar = IntVar()
        self.recordvar.set(1 if self.record else 0)
        
        self.text_path = StringVar()

    def display(self, frame):
        
        # create a top level 
        level = Toplevel(frame)
        
        # create a radio button for the recording
        checkbox = Checkbutton(level, text = "Record", variable = self.recordvar)
        checkbox.pack()
        
        # add a label with the path written
        self.update_display_path()
        
        label_path = Label(level, textvariable=self.text_path)
        label_path.pack()
        
        # add a box to chose the path and filename
        # display the path and name of the current replay
        bselect_path = Button(level, text= "Select path", command = self.select_path)
        bselect_path.pack()
        
    def update_display_path(self):
        if self.name:
            filename = self.get_filename().replace("\\", "/")
        else:
            filename = "path not set"
            
        max_displayed_chars = 23
        cover_symbol = "..."
        truncate_chars = max_displayed_chars - len(cover_symbol)
        
        if len(filename) >= max_displayed_chars:
            beginning = filename[:truncate_chars]
            ending = filename[len(filename)-truncate_chars:]
            filename = beginning + cover_symbol + ending

        self.text_path.set(filename)
    
    def select_path(self):
        
        initdir = self.path if self.path else "/"
        title = "Name a new file"
        extentions = (("snake4d files", ".sk4"),("all files", "*.*"))
        path = filedialog.asksaveasfilename(initialdir=initdir,
                                            title=title,
                                            filetypes=extentions)
        
        if path:
            # break the path down 
            
            pos = path.rfind("/")
            
            self.path = path[ : pos]
            self.name = path[pos + 1 : ]
            
            if self.name.find(".sk4") == -1:
                self.name += ".sk4"
                
            self.save()
            
            self.update_display_path()
    
    
    def get_filename(self):
        return os.path.join(self.path, self.name)
        
        
    
    def read_state(self):
        if self.recordvar.get() == 1:
            current_record_state = True
        else:
            current_record_state = False
            
        if current_record_state != self.record:
            self.record = current_record_state
            self.save()
        
    def save(self):
        with open(self.file, "w") as f:
            f.write("record=" + str(self.record) + "\n")
            f.write("path=" + self.path + "\n")
            f.write("name=" + self.name + "\n")
    
    def read(self):
        with open(self.file, "r") as f:
            
            lines = f.readlines()
            
        self.record = False if lines[0].split("=")[1].strip() == "False" else True
        self.path = lines[1].split("=")[1].strip()
        self.name = lines[2].split("=")[1].strip()
        
        if not os.path.isdir(self.path):
            self.path = "."
            self.save()

class LoadReplay:
    
    def __init__(self, game):
        self.frames = []
        self.current_frame = 0
        self.game = game
        
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
            
            print("Frame loaded:", len(self.frames))
        
    def set_frame(self):
        self.game.p_list = self.frames[self.current_frame]
    
    def next_frame(self):
        if self.current_frame + 1 < len(self.frames):
            self.current_frame += 1
            self.set_frame()
            
    def previous_frame(self):
        if self.current_frame - 1 > 0:
            self.current_frame -= 1
            self.set_frame()
            

class Replay:

    def __init__(self, geng):
        self.replay_settings = ReplaySettings() 
        
        self.replay = LoadReplay(geng)
        
    
    def reset_replay_file(self):
        with open(self.replay_settings.get_filename(), "wb") as f:
            f.write(b"")        
    
    def save_replay_frame(self, geng):        
        if self.replay_settings.record:
            filename = self.replay_settings.get_filename()
            with open(filename, "ab") as fobj:
                replay_file = bfh.BinaryFile(fobj)
                geng.frame_as_bytes(replay_file)    
    
    def load_replay(self, filename):
        # add a top level to manage the replay
        
        toplevel = Toplevel()
        
        # add buttons allback back play/pause forward allfw
        
        b_all_back = Button(toplevel, text="|<", command=self.all_back)
        b_all_back.pack()
        
        b_fw = Button(toplevel, text=">", command=self.fw)
        b_fw.pack()
        
        self.replay.load_replay_file(filename)
  
    def all_back(self):
        pass
    
    def fw(self):
        self.replay.next_frame()
        print("current_frame:", self.replay.current_frame)
        
    

#==============================================================================
# Main Application
#==============================================================================

class MainApp:
    '''
    Main Application

    controls everything in the game from graphics to game engine

    Keyword argument:
        root -- the parent frame, best if is root

    Public methods:
        rot4 -- 4d rotations
        rot3 -- 3d rotations
        help_cmd -- command that calls the help message
        new_game -- command that reinitializes the game
        toggle_pause -- pauses unpauses the game
        move -- triggers the change of direction given by the key pressed
        draw -- draws the scene
        updater -- the cycle ticker of the game

    Instance variables:
        self.game -- the game engine
        self.root -- the parent frame
        self.score_str -- is the text variable for the score
        self.areas -- are the drawing areas
        self.rot3k_to_angle -- maps the keys to the 3d rotations
        self.rot4k_to_angle -- maps the keys to the 4d rotations
        self.key_buffer -- the keys buffer
        self.paused -- the game state paused or not
        self.score_board -- the score display utilites
    '''

    def __init__(self, root):
        # start the game engine
        self.game = g_eng.GameEngine()

        # root frame of tkinter
        self.root = root

        # creates top menu
        self.create_menu()

        # score label
        self.score_str = StringVar()
        self.score_str.set("Score: 0")

        label = Label(self.root, textvariable=self.score_str)
        label.grid(row=0, column=0, columnspan=2)

        # game areas, first area is the perspective view,
        # the other two areas are the orthographic 2d projections of the game
        # the project flat class inverts the y axis, so that when pressing
        # wasd or ijkl the direction match the keyboard

        self.areas = []

        # area 0 - perspective
        proj = visu.ProjectCam()
        area4 = visu.VisuArea(root, proj, [500, 500])
        area4.fP.grid(row=1, column=0, columnspan=2)
        self.areas.append(area4)

        # area 1 - 2d projection of the yx axis
        proj = visu.ProjectFlat("yx")
        proj.zoom = 0.5
        area_xy = visu.VisuArea(root, proj, [250, 250], "YX")
        area_xy.fP.grid(row=2, column=0)
        self.areas.append(area_xy)

        # area 2 - 2d projection of the wz axis
        proj = visu.ProjectFlat("wz")
        proj.zoom = 0.5
        area_wz = visu.VisuArea(root, proj, [250, 250], "WZ")
        area_wz.fP.grid(row=2, column=1)
        self.areas.append(area_wz)

        # snake movements

        # moving keys pressed wasd, ijkl
        bind_key = ["w", "s", "a", "d", "i", "k", "j", "l"]
        for key in bind_key:
            self.root.bind(key, self.move)

        # scene rotations - both + and - roations are supported, pressing x
        # will rotate the scene in a direction and pressing X (shift+x) will
        # rotate backwards in respect to that direction

        # 3d rotations mapping
        rot3_keys_str = "xyc"
        rot3_keys = list(rot3_keys_str) + list(rot3_keys_str.upper())
        for key in rot3_keys:
            self.root.bind(key, self.rot3)
        # creates a diction that maps the key pressed to a set of angles
        self.rot3k_to_angle = {}

        rot_keys = rot3_keys_str + rot3_keys_str.upper()
        for i, k in enumerate(rot_keys):
            possible_rots = [0 for i in range(3)]
            possible_rots[i % 3] = 5 if i < 3 else -5
            self.rot3k_to_angle[k] = possible_rots

        # 4d rotations mapping
        rot4_keys_str = "vbnmtz"
        rot4_keys = list(rot4_keys_str) + list(rot4_keys_str.upper())
        for key in rot4_keys:
            self.root.bind(key, self.rot4)

        # creates a dictionary from key pressed to set of angles

        self.rot4k_to_angle = {}

        rot_keys = rot4_keys_str + rot4_keys_str.upper()
        for i, k in enumerate(rot_keys):
            possible_rots = [0 for i in range(6)]
            possible_rots[i % 6] = 5 if i < 6 else -5
            self.rot4k_to_angle[k] = possible_rots


        # the buffered key press
        self.key_buffer = KeyBuffer()

        # pause function
        self.paused = True
        self.root.bind("p", self.toggle_pause)

        # new game function
        self.root.bind("<space>", self.new_game)

        # adds a central text to the first area for instructions
        self.areas[0].add_text("Press any key to play")

        # the scores, which are saved in score.txt
        self.score_board = score.ScoreBoard(self.root)
        
        # creates the replay settings
        #self.replay_settings = ReplaySettings()
        
        self.replay = Replay(self.game)
        

    def create_menu(self):
        '''
        creates the top drop down menus

        File:
            New Game
            Quit
        Replay:
            Replay settings
        Help:
            Help
        '''

        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New Game", command=lambda: self.new_game(1))
        filemenu.add_cascade(label="Quit", command=self.root.destroy)
        
        replaymenu = Menu(menubar, tearoff=0)
        replaymenu.add_command(label="Replay settings", command=self.replay_settings_display)
        replaymenu.add_command(label="Load replay", command=self.load_replay)
        
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help", command=self.help_cmd)

        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Replay", menu =replaymenu)
        menubar.add_cascade(label="Help", menu=helpmenu)


        self.root.config(menu=menubar)
    
    def load_replay(self):
        initdir= "./tests"
        filename = filedialog.askopenfilename(initialdir=initdir)
        
        self.paused = True

        self.replay.load_replay(filename)
        
        
    
    def replay_settings_display(self):
        # read the settings from a file
        self.replay_settings.display(self.root)

    # controls the 4 dimensional rotation of the scenes
    def rot4(self, event):
        # if pressed clear the annoying instruction text
        self.areas[0].clear_text()

        # perform the camera rotations only in the perspective one
        # in the others, doesn't make sense
        rangles = self.rot4k_to_angle[event.char]
        self.areas[0].project_method.rotate4(rangles)

    # controls the 3 dimensional rotation of the scenes
    def rot3(self, event):
        # clear annoying text
        self.areas[0].clear_text()

        # perform the rotation
        rangles = self.rot3k_to_angle[event.char]
        self.areas[0].project_method.rotate3(rangles)

    # shows the help board
    def help_cmd(self):
        tl = Toplevel(self.root)
        label = Label(tl, text=INFO_TEXT, font=("Fixedsys", 12))
        label.pack()

    # starts a new game by rebooting the entire game engine
    def new_game(self, event):
        self.game = g_eng.GameEngine()
        self.areas[0].clear_text()
        self.areas[0].add_text("Press any key to play")
        self.key_buffer.clear()

    # pause toggle
    def toggle_pause(self, event):
        # the pause works only if the game is running
        if self.game.state != "game_over":
            if self.paused:
                self.paused = False
                self.areas[0].clear_text()
            else:
                self.paused = True
                self.areas[0].add_text("Press P to continue")

    # move command control
    def move(self, event):
        pressed_key = event.char
        self.paused = False
        # this pushes the key to the buffer, the actual actuator is the
        # get key in the updated function
        self.key_buffer.push_key(pressed_key)

    # draw the scenes
    def draw(self):
        for area in self.areas:
            area.clear_area()
            area.draw_plist(self.game.p_list)

    # the UI cycle
    def updater(self):

        # rates of update
        draw_rate = Rate(1 / 25.0)
        game_rate = Rate(1 / 2.0)
        update_rate = Rate(1 / 50.0)
        
        game_frame_counter = 0
        
        # reset the file
        self.replay.reset_replay_file()

        
        while True:

            # drawing scenese
            if draw_rate.is_time():
                self.draw()

            # game stuff
            if  game_rate.is_time():

                if self.paused or self.game.state == "game_over":
                    pass
                else:
                    # clears annoying text
                    self.areas[0].clear_text()

                    # reads the next key, thus the next direction from the
                    # buffer
                    next_dir = self.key_buffer.get_key()

                    # if the key is actually a direction and is a valid one
                    # here could actually skip the invalid directions...
                    # like random keys but keep the backward to head direction
                    # which is a mistake the player can make
                    if next_dir:
                        self.game.snake.change_dir(next_dir)

                    self.game.routine()
                    
                    # writes the frames
                    
                    self.replay.save_replay_frame(self.game)
                    
                    game_frame_counter += 1

                    # updates the score label
                    self.score_str.set("Score: " + str(self.game.score))

                    # if the games ends in a game over, then show the top score
                    # board
                    if self.game.state == "game_over":
                        self.areas[0].add_text("Game Over\nPress space for new game")

                        # create new score
                        curr_score = score.Score(datetime.datetime.now(), self.game.score)
                        self.score_board.add_score(curr_score)
                        self.score_board.render_scores()

                        # pause the game
                        self.paused = True

            # update the tkinter cycle
            if update_rate.is_time():
                self.root.update_idletasks()
                self.root.update()
                self.replay.replay_settings.read_state()

# main program
def main():
    print("Snake 4D (2.0)")

    #initialize tk root and application
    root = Tk()
    root.title("Snake 4d (2.0)")

    mapp = MainApp(root)

    try:
        mapp.updater()

    # there is a pesky error when the user presses the X of the main window
    # this catches the error
    except _tkinter.TclError as exp:
        print("Tkinter error: ", end="")
        print(exp.__class__)
        print(exp)

    # rethrow any other exception
    except Exception as exp:
        print(exp.__class__)
        print(exp)
        raise exp


if __name__ == "__main__":
    main()
