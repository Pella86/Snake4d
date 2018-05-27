# -*- coding: utf-8 -*-
"""
Created on Thu May 17 13:20:44 2018

@author: Mauro
"""


from tkinter import Tk, _tkinter, StringVar, Label, Menu, Toplevel

import visu, g_eng, score
import time
import datetime

# add new game button
# add help button
# add high score panel
# add text for the beginning and end
#   - Press space to start if game is game_over
#   - Press p or any key to pause/continue if game is running
# add rotations


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


class KeyBuffer:
    
    def __init__(self):
        self.buf = []
        
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

class MainApp:
    
    def __init__(self, root):
        self.game = g_eng.GameEngine()
        
        self.areas = []
        
        self.root = root
        
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New Game", command= lambda : self.new_game(1))
        filemenu.add_command(label="Help", command= self.help_cmd)
        filemenu.add_cascade(label="Quit", command = self.root.destroy)
        
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)
        
        self.score_str = StringVar()
        self.score_str.set("Score: 0")
        
        label = Label(self.root, textvariable= self.score_str)
        label.grid(row = 0, column = 0, columnspan = 2)
        
        proj = visu.ProjectCam()
        area4 = visu.VisuArea(root, proj, [500, 500])
        area4.fP.grid(row = 1, column = 0, columnspan= 2)
        self.areas.append(area4)
    
        proj = visu.ProjectFlat("yx")
        proj.zoom = 0.5
        area_xy = visu.VisuArea(root, proj, [250, 250], "YX")
        area_xy.fP.grid(row = 2, column = 0)
        self.areas.append(area_xy)
    
        proj = visu.ProjectFlat("wz")
        proj.zoom = 0.5
        area_wz = visu.VisuArea(root, proj, [250, 250], "WZ")
        area_wz.fP.grid(row = 2, column = 1)
        self.areas.append(area_wz)  
        
        bind_key = ["w", "s", "a", "d", "i", "k", "j", "l"]
        for key in bind_key:
            self.root.bind(key, self.move)
        
        rot3_keys_str = "xyc"
        rot3_keys = list(rot3_keys_str) + list(rot3_keys_str.upper())
        for key in rot3_keys:
            self.root.bind(key, self.rot3)
        
        rot4_keys_str = "vbnmtz"
        rot4_keys = list(rot4_keys_str) + list(rot4_keys_str.upper())
        for key in rot4_keys:
            self.root.bind(key, self.rot4)        
        
        self.key_buffer = KeyBuffer()
        
        self.paused = True
        self.root.bind("p", self.toggle_pause)
        self.root.bind("<space>", self.new_game)
        
        self.areas[0].add_text("Press any key to play")
        
        self.score_board = score.ScoreBoard(self.root)
    
    def rot4(self, event):
        self.areas[0].clear_text()
        rot_keys = "vbnmtz"
        rot_keys = rot_keys + rot_keys.upper()
        
        rotk_to_angle = {}
        
        for i, k in enumerate(rot_keys):
            possible_rots = [0 for i in range(6)]
            possible_rots[i % 6] = 5 if i < 6 else -5 
            rotk_to_angle[k] = possible_rots
        
        self.areas[0].project_method.rotate4(rotk_to_angle[event.char])
    
    def rot3(self, event):
        self.areas[0].clear_text()
        rot_keys = "xyc"
        rot_keys += rot_keys.upper()
        
        rotk_to_angle = {}
        
        for i, k in enumerate(rot_keys):
            possible_rots = [0 for i in range(3)]
            possible_rots[i % 3] = 5 if i < 3 else -5
            rotk_to_angle[k] = possible_rots
        
        r = rotk_to_angle[event.char]
        self.areas[0].project_method.rotate3(r)
    
    def help_cmd(self):
        tl = Toplevel(self.root)
        label = Label(tl, text = info_text, font = ("Fixedsys", 12))
        label.pack()
        
    def new_game(self, event):
        self.game = g_eng.GameEngine()
        self.areas[0].clear_text()
        self.areas[0].add_text("Press any key to play")
        self.key_buffer.clear()
    
    def toggle_pause(self, event):
        if self.game.state != "game_over":
            self.paused = False if self.paused == True else True
        
        if self.paused and self.game.state != "game_over":
            self.areas[0].add_text("Press P to continue")
        elif self.game.state != "game_over":
            self.areas[0].clear_text()
            
    def move(self, event):
        pressed_key = event.char
        self.paused = False
        self.key_buffer.push_key(pressed_key)

      
    def draw(self):
        for area in self.areas:
            area.clear_area()
            area.draw_plist(self.game.p_list)  
    
    def updater(self):
        draw_rate = 1 / 25
        game_rate = 1 / 2.0
        update_rate = 1 / 50.0
        
        draw_time = time.time()
        game_time = time.time()
        update_time = time.time()
        
        while True:
            
            if time.time() - draw_time > draw_rate:
                draw_time = time.time()
                self.draw()
                
            
            if  time.time() - game_time > game_rate:
                game_time = time.time()
                
                if self.paused or self.game.state == "game_over":
                    pass
                else:
                    self.areas[0].clear_text()
                    next_dir = self.key_buffer.get_key()
                    
                    if next_dir:
                        self.game.snake.change_dir(next_dir)
                    
                    self.game.routine()
                    self.score_str.set("Score: " + str(self.game.score))
                    
                    if self.game.state == "game_over":
                        self.areas[0].add_text("Game Over\nPress space for new game")
                        
                        # create new score
                        curr_score = score.Score(datetime.datetime.now(), self.game.score)
                        
                        self.score_board.add_score(curr_score)
                        
                        self.score_board.render_scores()
                        
                        self.paused = True
            
            if time.time() - update_time > update_rate:
                update_time = time.time()
                self.root.update_idletasks()
                self.root.update()


        
def main():
    print("Snake 4D (2.0)")

    root = Tk()
    root.title("Snake 4d (2.0)")
    ma = MainApp(root)
    
    try:
        ma.updater()
    except _tkinter.TclError as e:
        print("Tkinter error: ", end="")
        print(e.__class__)
        print(e)
        
    except Exception as e:
        print(e.__class__)
        print(e)
        raise e
    

if __name__ == "__main__":
    main()
    
    
    
    

    
    