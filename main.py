# -*- coding: utf-8 -*-
"""
Created on Thu May 17 13:20:44 2018

@author: Mauro
"""


from tkinter import Tk, _tkinter, StringVar, Label, Menu, Toplevel

import visu, g_eng
import time

# add new game button
# add help button
# add high score panel


info_text =  "*****************snake 4d********************\n"
info_text += "Rules:                                 \n"
info_text += "    1. eat the food (red cube)         \n"
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

class Score:
    def __init__(self):
        pass

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
        
        self.key_buffer = KeyBuffer()
        
        self.paused = True
        self.root.bind("p", self.toggle_pause)
        self.root.bind("<space>", self.new_game)
    
    def help_cmd(self):
        tl = Toplevel(self.root)
        label = Label(tl, text = info_text, font = ("Fixedsys", 12))
        label.pack()
        
    def new_game(self, event):
        self.game = g_eng.GameEngine()
    
    def toggle_pause(self, event):
        self.paused = False if self.paused == True else True
            
    def move(self, event):
        pressed_key = event.char
        self.paused = False
        self.key_buffer.push_key(pressed_key)

      
    def draw(self):
        for area in self.areas:
            area.clear_area()
            area.draw_plist(self.game.p_list)  
    
    def updater(self):
        draw_rate = 1 / 10.0
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
                    next_dir = self.key_buffer.get_key()
                    
                    if next_dir:
                        self.game.snake.change_dir(next_dir)
                    
                    self.game.routine()
                    self.score_str.set("Score: " + str(self.game.score))
                    
                    if self.game.state == "game_over":
                        self.paused = True
            
            if time.time() - update_time > update_rate:
                update_time = time.time()
                self.root.update_idletasks()
                self.root.update()


        
def main():
    print("Snake 4D revised")

    root = Tk()
    ma = MainApp(root)
    
    try:
        ma.updater()
    except _tkinter.TclError:
        pass
    except Exception as e:
        print(e.__class__)
        print(e)
        raise e
    

if __name__ == "__main__":
    main()
    
    
    
    
    

    
    