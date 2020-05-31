# -*- coding: utf-8 -*-
"""
Created on Thu May 17 13:20:44 2018

@author: Mauro
"""

# import sys to access the src folder
import sys
sys.path.append("./src")

# py imports
import datetime

# GUI stuff
from tkinter import (Tk, _tkinter, StringVar, Label, Menu, Toplevel, filedialog)

# project imports
import visu
import g_eng
import score
import replay
import keybuf
import rate


#==============================================================================
# # TO DO list
#==============================================================================

# Refactor collisions
# Comment/Refactor rotation messs
# Create a blender folder and blender file to render the stuff
# Think about a better way to do the replay

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
        self.replay -- manages the replay
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
        self.rot3k_to_angle = self.set_rotation_keys("xyc")
        self.rot4k_to_angle = self.set_rotation_keys("vbnmtz")

        # the buffered key press
        self.key_buffer = keybuf.KeyBuffer()

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
        
        self.replay = replay.Replay(self.game)
    
    def set_rotation_keys(self, keys):
        
        n_rot = len(keys)
        angle_delta = 5 # degrees
        
        # 4d rotations mapping
        rot4_keys = list(keys) + list(keys.upper())
        for key in rot4_keys:
            self.root.bind(key, self.rot)yyyy

        # creates a dictionary that maps the key pressed to set of angles
        rot_to_angle = {}

        for i, k in enumerate(rot4_keys):
            # set the rotations to 0
            possible_rots = [0 for i in range(n_rot)]
            
            # assign the angle to the relevant rotation
            possible_rots[i % n_rot] = angle_delta if k.islower() else -angle_delta
            rot_to_angle[k] = possible_rots

        return rot_to_angle
        

    def create_menu(self):
        '''
        creates the top drop down menus

        File:
            New Game
            Quit
        Replay:
            Replay settings
            Load replay
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
    
    # controls the rotations in response to a key press
    def rot(self, event):
         # if pressed clear the annoying instruction text
        self.areas[0].clear_text()
        
        # perform the camera rotations only in the perspective one
        # in the others, doesn't make sense
        
        # if the key pressed is in the 4d rotations
        # if the key is a 3d rotation the get function will return None
        rotation = self.rot4k_to_angle.get(event.char)
        
        if rotation:
            self.areas[0].project_method.rotate4(rotation)
        
        # else the key must be a 3d rotation
        rotation = self.rot3k_to_angle[event.char]
        
        self.areas[0].project_method.rotate3(rotation)

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
        draw_rate = rate.Rate(1 / 25.0)
        game_rate = rate.Rate(1 / 2.0)
        update_rate = rate.Rate(1 / 50.0)
        replay_rate = rate.Rate(1 / 2.0)

        # reset the file
        self.replay.reset_replay_file()

        
        while True:
            
            if replay_rate.is_time():
                self.replay.play_frames()

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
                    
                    # writes the frames if the record option is on
                    self.replay.save_replay_frame(self.game)

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
