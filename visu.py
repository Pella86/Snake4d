# -*- coding: utf-8 -*-
"""
Created on Wed May 23 15:33:29 2018

@author: Mauro
"""
from tkinter import Frame, Canvas, Label
import vec, prj, poly
import copy

# The drawing functions are the ones taking more time
# One way to reduce the drawing burden is to reduce the drawed objects

# optimization 1
# dont draw overlapping edges and vertex
# in the flat projection there is a huge ammount of overlapping vertexes and
# edges, this filtering assumes that scanning the polygon array for
# equal x and y is less expensive then drawing them

# optimization 2
# draw only new stuff, construct a drawn primitives buffer that checks if the
# edge was already drawn. The edges are queried and if they are present in the
# buffer, they get a check in flag
# if they are not present, they dont have the check in flag so they can be
# easly deleted

class Edge:
    
    def __init__(self, v1, v2, e, color):
        self.v1 = v1
        self.v2 = v2
        self.e = e
        self.c = color
        self.item_n = None
        self.v1_item_n = None
        self.v2_item_n = None
        self.checked_in = False

class DrawnEdges:
    
    def __init__(self):
        self.drawn = []

    def add_edge(self, v1, v2, inpe, color):
        edge_present = False
        
        for i, e in enumerate(self.drawn):
            if e.v1.is_close(v1) and e.v2.is_close(v2):
                edge_present = True
                edge_i = i
                break
        
        if edge_present:
            self.drawn[edge_i].checked_in = True
        else:
            self.drawn.append(Edge(v1, v2, inpe, color))
    
    def reset_check_in(self):
        for i in range(len(self.drawn)):
            self.drawn[i].checked_in = False
       

class VisuArea:
    
    def __init__(self, parent_frame, project_method, area_size, title = ""):
        
        self.fP = Frame(parent_frame)
        if title:
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
        
        self.drawn_edges = DrawnEdges()
        
        self.text_items = []
    
    def add_text(self, text):
        item_n = self.canvas.create_text([self.cw / 2., self.ch / 2.], text=text, font=("Fixedsys", 26), fill="lightgreen", justify="center")
        self.text_items.append(item_n)
        
    
    def clear_text(self):
        for i in self.text_items:
            self.canvas.delete(i)
        
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
    
    def draw_poly(self, poly2, draw_vert = True):
                
        # select which edges needs to be drawn
        for e in poly2.e_list:
            v1 = poly2.v_list[ e[0] ]
            v2 = poly2.v_list[ e[1] ]
            self.drawn_edges.add_edge(v1, v2, e, poly2.color)
            
        # this should draw only the edges that are selected
        for i, edge in enumerate(self.drawn_edges.drawn):
            if edge.item_n == None:
                # draws the edge
                inum = self.draw_edge(edge.v1, edge.v2, kwargs={"fill" : edge.c}) 
                self.drawn_edges.drawn[i].item_n = inum
                
                # draws vertexes
                if draw_vert:
                    inum = self.draw_point(poly2.v_list[edge.e[0]], 3.5, kwargs={"fill" : edge.c})
                    self.drawn_edges.drawn[i].v1_item_n = inum
    
                    inum = self.draw_point(poly2.v_list[edge.e[1]], 3.5, kwargs={"fill" : edge.c})
                    self.drawn_edges.drawn[i].v2_item_n = inum   
                
                # check in that the primitive has been drawn
                self.drawn_edges.drawn[i].checked_in = True

                
            

    def clear_area(self):
        tmp_drawn = []
        for e in self.drawn_edges.drawn:
            if e.checked_in == False:
                self.canvas.delete(e.item_n)
                if e.v1_item_n:
                    self.canvas.delete(e.v1_item_n)
                    self.canvas.delete(e.v2_item_n)
            else:
                tmp_drawn.append(e)
        
        self.drawn_edges.drawn = tmp_drawn
        self.drawn_edges.reset_check_in()
        

    
    def project4(self, poly):
        p2 = self.project_method.project(poly)
        return p2
    
    def draw_plist(self, p_list):
        for p in p_list:
            p2 = self.project4(p)
            self.draw_poly(p2, True)
    

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
        poly2.color = poly4.color
        
        for v in poly4.v_list:
            x = v[self.i] * self.zoom * -1
            y = v[self.j] * self.zoom 
            poly2.v_list.append(vec.V2(x, y))
        
        # index / vertex clas
        class EIndex:
            def __init__(self, v1, v2, e):
                self.v1 = v1
                self.v2 = v2
                self.e = e
                
        preserved = []
        
        # gather the edges of the 4d polygon
        for e in poly4.e_list:
            # gather the verterxes of the projected polygon
            v1 = poly2.v_list[e[0]]
            v2 = poly2.v_list[e[1]]
            
            ei = EIndex(v1, v2, e)
            
            # scan the edge vertexes to find overlapping edges
            # based on difference norm
            unique = True
            for pei in preserved:
                if ei.v1.is_close(pei.v1) and ei.v2.is_close(pei.v2):
                    unique = False
                    break
            
            if unique:
                preserved.append(ei) 
        
        poly2.e_list = [ei.e for ei in preserved]
            
        return poly2    