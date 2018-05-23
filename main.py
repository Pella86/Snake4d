# -*- coding: utf-8 -*-
"""
Created on Thu May 17 13:20:44 2018

@author: Mauro
"""


from tkinter import Tk, Frame, Canvas

import vec, prj, poly, qua, math, rot4, copy, snake, g_eng

class PrjArea:
    
    def __init__(self, parent_frame):
        
        self.fP = Frame(parent_frame)
        
        self.cw = 1000
        self.ch = 500
        
        self.area_w = 5
        self.area_h = 2.5
        
        self.c_center_w = self.cw / 2
        self.c_center_h = self.ch / 2
        
        self.canvas = Canvas(self.fP, width = self.cw, height = self.ch)
        self.canvas.pack()
        
        self.var_item_list = []
        
    
    def convert_to_canvas_coord(self, x, y):
        h = self.ch - (self.ch / self.area_h) * y - self.c_center_h
        w = (self.cw / self.area_w) * x + self.c_center_w
        return vec.V2(w, h)
    
    def draw_point(self,v, cvsize, kwargs):
        v = self.convert_to_canvas_coord(v.x(), v.y())
        sizev = vec.V2(cvsize, cvsize)
        
        lp = v - sizev / 2
        hp = v + sizev / 2
        
        return self.canvas.create_rectangle(lp.x(), lp.y(), hp.x(), hp.y(), **kwargs)
    
    def draw_edge(self, start, end, kwargs):
        vx = self.convert_to_canvas_coord(start.x(), start.y())
        vy = self.convert_to_canvas_coord(end.x(), end.y())
        
        return self.canvas.create_line(vx.x(), vx.y(), vy.x(), vy.y(), **kwargs)
    
    
    def draw_poly(self, poly2, edges = True, vertexes = True):
        
        if vertexes:
            for v in poly2.v_list:
                i = self.draw_point(v, 5, kwargs={"fill" : poly2.color})
                self.var_item_list.append(i)
        if edges:
            for e in poly2.e_list:
                v1 = poly2.v_list[ e[0] ]
                v2 = poly2.v_list[ e[1] ]
                i = self.draw_edge(v1, v2, kwargs={"fill" : poly2.color}) 
                self.var_item_list.append(i)

            
    def clear_area(self):
        for i in self.var_item_list:
            self.canvas.delete(i)

        
    
class Project:
    
    def __init__(self):
        self.cam3 = prj.Cam3()
        self.cam3.change_position(vec.V3(5, 5, 5))    
        
        self.cam4 = prj.Cam4()
        self.cam4.From = vec.V4(15, 0.1, 0.1, 0.1)
        self.cam4.t_matrix = self.cam4.trans_matrix() 
    
    def project(self, poly4):
        polygon = copy.deepcopy(poly4)
        
        for i in range(len(polygon.v_list)):
            # convert in 3

            p3 = self.cam4.prj(polygon.v_list[i])      
            p2 = self.cam3.prj(p3)
            polygon.v_list[i] = p2

                
        return polygon
        

    

if __name__ == "__main__":
    
    print("Snake 4D revised")
    
    # draw 2d axes
    
    # draw 3d axes
            
    projection = Project()
    
    game = g_eng.GameEngine()
    
    root = Tk()
    area = PrjArea(root)
    area.fP.pack()


    game.snake.move("LEFT")
    
    game.routine()
    
    def draw_scene():
         for poly4 in game.p_list:
            p = projection.project(poly4)
            area.draw_poly(p, True, False)       

    def move(event):
        pressed_key = event.char
        
        print(pressed_key)
        
        possible_dirs = ["UP", "DOWN", "LEFT", "RIGHT", "FW", "RW", "IN", "OUT"]
        bind_key = ["w", "s", "a", "d", "i", "k", "j", "l"]
        
        key_to_dir = {}
        for direction, key in zip(possible_dirs, bind_key):
            key_to_dir[key] = direction
        
        print("new dir", key_to_dir[pressed_key])
        game.snake.head_dir = key_to_dir[pressed_key]
        game.routine()
        area.clear_area()
        draw_scene()
        root.update()
    
    bind_key = ["w", "s", "a", "d", "i", "k", "j", "l"]
    for key in bind_key:
        root.bind(key, move)
        
    def rotate_cam(e):
        v = projection.cam4.From
        projection.cam4.From = rot4.rot_v(v, math.radians(3), 0, 0, 0, 0, math.radians(3))
        projection.cam4.t_matrix = projection.cam4.trans_matrix()
        area.clear_area()
        draw_scene()
        root.update()
        
    root.bind("x", rotate_cam)
     
    root.mainloop()

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
    
    
    
    

    
    