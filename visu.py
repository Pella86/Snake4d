# -*- coding: utf-8 -*-
"""
Created on Wed May 23 15:33:29 2018

@author: Mauro
"""
from tkinter import Frame, Canvas, Label
import vec, prj, poly
import copy

class VisuArea:
    
    def __init__(self, parent_frame, project_method, area_size, title):
        
        self.fP = Frame(parent_frame)
        
        label = Label(self.fP, text=title)
        label.pack()
        
        self.cw = area_size[0]
        self.ch = area_size[1]
        
        self.area_w = 5
        self.area_h = 5
        
        self.c_center_w = self.cw / 2
        self.c_center_h = self.ch / 2
        
        self.canvas = Canvas(self.fP, width = self.cw, height = self.ch)
        self.canvas.pack()
        
        self.var_item_list = []
        
        self.project_method = project_method
        
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
    
    def project4(self, poly):
        p2 = self.project_method.project(poly)
        return p2
    
    def draw_plist(self, p_list):
        for p in p_list:
            p2 = self.project4(p)
            self.draw_poly(p2)
    

class ProjectCam:
    
    def __init__(self):
        self.cam3 = prj.Cam3()
        self.cam3.change_position(vec.V3(2.5, 2.5, 2.5))    
        
        self.cam4 = prj.Cam4()
        self.cam4.change_position(vec.V4(15, 0.1, 0.1, 0.1))
    
    def project(self, poly4):
        polygon = copy.deepcopy(poly4)
        
        for i in range(len(polygon.v_list)):
            p3 = self.cam4.prj(polygon.v_list[i])      
            p2 = self.cam3.prj(p3)
            polygon.v_list[i] = p2
        return polygon

class ProjectFlat:
    
    def __init__(self, axes):
        self.ax2coord = {}
        ax_names = "xyzw"
        for i, c in enumerate(ax_names):
            self.ax2coord[c] = i
        
        self.zoom = 0.3
        
        self.i = self.ax2coord[axes[0]]
        self.j = self.ax2coord[axes[1]]        
        
    def project(self, poly4):      
        poly2 = poly.Polygon()
        poly2.e_list = poly4.e_list
        poly2.color = poly4.color
        
        for v in poly4.v_list:
            x = v[self.i] * self.zoom * -1
            y = v[self.j] * self.zoom 
            poly2.v_list.append(vec.V2(x, y))

        return poly2    