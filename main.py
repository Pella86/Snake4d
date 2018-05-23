# -*- coding: utf-8 -*-
"""
Created on Thu May 17 13:20:44 2018

@author: Mauro
"""


from tkinter import Tk, Frame

import visu, g_eng
import time

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
        
        proj = visu.ProjectCam()
        area4 = visu.VisuArea(root, proj, [500, 500], "Main Screen")
        area4.fP.grid(row = 0, column = 0, columnspan= 2)
        self.areas.append(area4)
    
        proj = visu.ProjectFlat("yx")
        proj.zoom = 0.5
        area_xy = visu.VisuArea(root, proj, [250, 250], "YX")
        area_xy.fP.grid(row = 1, column = 0)
        self.areas.append(area_xy)
    
        proj = visu.ProjectFlat("wz")
        proj.zoom = 0.5
        area_wz = visu.VisuArea(root, proj, [250, 250], "WZ")
        area_wz.fP.grid(row = 1, column = 1)
        self.areas.append(area_wz)  
        
        bind_key = ["w", "s", "a", "d", "i", "k", "j", "l"]
        for key in bind_key:
            self.root.bind(key, self.move)
        
        self.key_buffer = KeyBuffer()
            
    def move(self, event):
        pressed_key = event.char
        
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
                
                next_dir = self.key_buffer.get_key()
                if next_dir:
                    self.game.snake.change_dir(next_dir)
                self.game.routine()
            
            if time.time() - update_time > update_rate:
                update_time = time.time()
                self.root.update_idletasks()
                self.root.update()

        

    

if __name__ == "__main__":
    
    print("Snake 4D revised")

    root = Tk()
    ma = MainApp(root)
    ma.updater()
    
    
#    def draw():
#        for area in areas:
#            area.clear_area()
#            area.draw_plist(game.p_list)        
#    
#    def upscreen(event):
#        print("UPDATE SCREEN")
#        draw()
#        root.update()
#
#    def move(event):
#        pressed_key = event.char
#        
#        possible_dirs = ["UP", "DOWN", "LEFT", "RIGHT", "FW", "RW", "IN", "OUT"]
#        bind_key = ["w", "s", "a", "d", "i", "k", "j", "l"]
#        
#        key_to_dir = {}
#        for direction, key in zip(possible_dirs, bind_key):
#            key_to_dir[key] = direction
#        
#        if game.snake.change_dir(key_to_dir[pressed_key]):
#            game.routine()
#            draw()
#            root.update()
#    
#    bind_key = ["w", "s", "a", "d", "i", "k", "j", "l"]
#    for key in bind_key:
#        root.bind(key, move)
#        
#    root.bind("m", upscreen)
#    
#    #root.mainloop()
#
#    slice_frame = 10000000
#    c = slice_frame
#
#    while True:
#        if c % slice_frame == 0:
#            game.routine()
#            draw()
#            root.update()
#            
#        
#        c += 1       
    
            
#    projection = Project()
#    
#    game = g_eng.GameEngine()
#    
#    root = Tk()
#    area = PrjArea(root)
#    area.fP.pack()
#    
#    game.routine()
#    
#    def draw_scene():
#         for poly4 in game.p_list:
#            p = projection.project_flat(poly4, "xy")
#            area.draw_poly(p, True, True)       
#
#    def move(event):
#        pressed_key = event.char
#        
#        print(pressed_key)
#        
#        possible_dirs = ["UP", "DOWN", "LEFT", "RIGHT", "FW", "RW", "IN", "OUT"]
#        bind_key = ["w", "s", "a", "d", "i", "k", "j", "l"]
#        
#        key_to_dir = {}
#        for direction, key in zip(possible_dirs, bind_key):
#            key_to_dir[key] = direction
#        
#        print("new dir", key_to_dir[pressed_key])
#        game.snake.change_dir(key_to_dir[pressed_key])
#        game.routine()
#        area.clear_area()
#        draw_scene()
#        root.update()
#    
#    bind_key = ["w", "s", "a", "d", "i", "k", "j", "l"]
#    for key in bind_key:
#        root.bind(key, move)
#        
#    def rotate_cam(e):
#        v = projection.cam4.From
#        rotv = rot4.rot_v(v, math.radians(3), 0, 0, 0, 0, math.radians(3))
#        projection.cam4.change_position(rotv)
#        
#        area.clear_area()
#        draw_scene()
#        root.update()
#        
#    root.bind("x", rotate_cam)
#    
#    root.mainloop()

#    
#    slice_frame = 10000000
#    c = slice_frame

#    while True:
#        if c % slice_frame == 0:
#            area.clear_area()
#            game.routine()
#            
#            draw_scene()
#
#            root.update()
#            
#        
#        c += 1   
    
    
    
    

    
    