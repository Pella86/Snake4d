# -*- coding: utf-8 -*-
"""
Created on Thu May 17 13:20:44 2018

@author: Mauro
"""

# GUI stuff
from tkinter import Tk, _tkinter, StringVar, Label, Menu, Toplevel

# project imports
import visu, g_eng, score

# py imports
import time
import datetime

#==============================================================================
# # TO DO list
#==============================================================================

# add help button
# add high score panel
# add text for the beginning and end
#   - Press space to start if game is game_over
#   - Press p or any key to pause/continue if game is running
# add rotations

#==============================================================================
# Help message
#==============================================================================

info_text =  "*****************snake 4d********************\n"
info_text += "Rules:                                 \n"
info_text += "    1. eat the food (blue cube)        \n"
info_text += "    2. don't hit the walls (black)     \n"
info_text += "    3. don't cross yourself (green)    \n"
info_text += "                                       \n"
info_text += "How to play:                           \n"
info_text += "      W             I                  \n"
info_text += "     ASD           JKL                 \n"
info_text += "These keys control the SNAKE in the 6  \n"
info_text += "directions:                            \n"
info_text += "                                       \n"
info_text += "W = UP                                 \n"
info_text += "A = RIGHT                              \n"
info_text += "S = DOWN                               \n"
info_text += "D = LEFT                               \n"
info_text += "I = OUT                                \n"
info_text += "J = FORWARD                            \n"
info_text += "K = IN                                 \n"
info_text += "L = REVERSE                            \n"
info_text += "                                       \n"
info_text += "To control the CAMERA use:             \n"
info_text += "  X or C to control 3d rotations       \n"
info_text += "  B or N or M to control 4d rotations  \n"
info_text += "**********************************************\n"

#==============================================================================
# Key buffer
#   is a simple buffer that keeps track of the key pressed while playing
#   it makes a more fluid control of the snake when the game lags
#==============================================================================

class KeyBuffer:
    
    def __init__(self):
        self.buf = []
        
        # construct the dictionary that changes the snake direction
        self.key_to_dir = {}
        possible_dirs = ["UP", "DOWN", "LEFT", "RIGHT", "FW", "RW", "IN", "OUT"]
        bind_key = ["w", "s", "a", "d", "i", "k", "j", "l"]

        for direction, key in zip(possible_dirs, bind_key):
            self.key_to_dir[key] = direction    
    
    def push_key(self, key):
        self.buf.append(key)
    
    def get_key(self):
        if self.buf:
            return self.key_to_dir[self.buf.pop(0)]
        else:
            return None 
    
    def clear(self):
        self.buf = []

#==============================================================================
# Rate class 
#   for update rate, fps, ...
#==============================================================================
        
class Rate:
    
    def __init__(self, rate):
        self.rate = rate
        self.init_time = time.time()
    
    def is_time(self):
        if time.time() - self.init_time > self.rate:
            self.init_time = time.time()
            return True
        else:
            return False
    
#==============================================================================
# Main Application
#   controls about anything of the game
#==============================================================================

class MainApp:
    
    def __init__(self, root):
        # start the game engine
        self.game = g_eng.GameEngine()
        
        # root frame of tkinter
        self.root = root
        
        # top drop down menu
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New Game", command= lambda : self.new_game(1))
        filemenu.add_cascade(label="Quit", command = self.root.destroy)
        
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help", command= self.help_cmd)
        
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Help", menu=helpmenu)
        
        self.root.config(menu=menubar)
        
        # score label
        self.score_str = StringVar()
        self.score_str.set("Score: 0")
        
        label = Label(self.root, textvariable= self.score_str)
        label.grid(row = 0, column = 0, columnspan = 2)
        
        # game areas, first area is the perspective view,
        # the other two areas are the orthographic 2d projections of the game
        # the project flat class inverts the y axis, so that when pressing 
        # wasd or ijkl the direction match the keyboard
        
        self.areas = []
        
        # area 0 - perspective
        proj = visu.ProjectCam()
        area4 = visu.VisuArea(root, proj, [500, 500])
        area4.fP.grid(row = 1, column = 0, columnspan= 2)
        self.areas.append(area4)
    
        # area 1 - 2d projection of the yx axis
        proj = visu.ProjectFlat("yx")
        proj.zoom = 0.5
        area_xy = visu.VisuArea(root, proj, [250, 250], "YX")
        area_xy.fP.grid(row = 2, column = 0)
        self.areas.append(area_xy)
        
        # area 2 - 2d projection of the wz axis
        proj = visu.ProjectFlat("wz")
        proj.zoom = 0.5
        area_wz = visu.VisuArea(root, proj, [250, 250], "WZ")
        area_wz.fP.grid(row = 2, column = 1)
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
        label = Label(tl, text = info_text, font = ("Fixedsys", 12))
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

# main program
def main():
    print("Snake 4D (2.0)")

    #initialize tk root and application
    root = Tk()
    root.title("Snake 4d (2.0)")
    
    ma = MainApp(root)
    
    try:
        ma.updater()
    
    # there is a pesky error when the user presses the X of the main window
    # this catches the error
    except _tkinter.TclError as e:
        print("Tkinter error: ", end="")
        print(e.__class__)
        print(e)
        
    # rethrow any other exception    
    except Exception as e:
        print(e.__class__)
        print(e)
        raise e
    

if __name__ == "__main__":
    main()
    
    
    
    

    
    