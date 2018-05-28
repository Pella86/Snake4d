# -*- coding: utf-8 -*-
"""
Created on Wed May 23 15:33:29 2018

@author: Mauro
"""

#==============================================================================
# Drawing classes
#==============================================================================

from tkinter import Frame, Canvas, Label
import vec, prj, poly, qua, rot4
import copy
import math

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

#==============================================================================
# Class Edge
#   little utility to control the drawn edge
#==============================================================================

class Edge:
    
    def __init__(self, v1, v2, e, color):
        # start and end point
        self.v1 = v1
        self.v2 = v2
        
        # relationship with the vertexes
        self.e = e
        
        # color
        self.c = color
        
        # canvas item number, needed for deletion
        self.item_n = None
        
        # vertex item numbers
        self.v1_item_n = None
        self.v2_item_n = None
        
        # if true, means someone wants to draw the vector.
        # if False, nobody wants the vector so it can be safely removed
        self.checked_in = False

#==============================================================================
# class Drawn Edges
#   little utilites to control the edge alredy drawn on the screen
#==============================================================================

class DrawnEdges:
    
    def __init__(self):
        self.drawn = []

    # add one edge to the list
    def add_edge(self, v1, v2, inpe, color):
        edge_present = False
        
        for i, e in enumerate(self.drawn):
            # find the closest possible edge to the one inputed
            # if tehre is one already in the list, then mark it 
            # as already drawn
            if e.v1.is_close(v1) and e.v2.is_close(v2):
                edge_present = True
                edge_i = i
                break
        
        # if the edge is already present check it in
        if edge_present:
            self.drawn[edge_i].checked_in = True
        # if the edge is not present, pipe it to draw it
        else:
            self.drawn.append(Edge(v1, v2, inpe, color))
    
    def reset_check_in(self):
        for i in range(len(self.drawn)):
            self.drawn[i].checked_in = False

#==============================================================================
# class Area visualization
#   manages all the drawing functions       
#==============================================================================

class VisuArea:
    
    def __init__(self, parent_frame, project_method, area_size, title = ""):
        
        # parent frame
        self.fP = Frame(parent_frame)
        
        # title if present
        if title:
            label = Label(self.fP, text=title)
            label.pack()
        
        # how big in pixels is the area
        self.cw = area_size[0]
        self.ch = area_size[1]
        
        # how big is the area in custom units
        # self.area_w / self.cw = 1 unit
        self.area_w = 5
        self.area_h = 5
        
        # where the center is
        self.c_center_w = self.cw / 2
        self.c_center_h = self.ch / 2
        
        # the canvas where drawing happens
        self.canvas = Canvas(self.fP, width = self.cw, height = self.ch)
        self.canvas.pack()
        
        # projection method, can be perspective or flat
        self.project_method = project_method
        
        # the already drawn edges class
        self.drawn_edges = DrawnEdges()
        
        # text drawn on the canvas
        self.text_items = []
    
    # text utilieties, add and clear text
    def add_text(self, text):
        item_n = self.canvas.create_text([self.cw / 2., self.ch / 2.], text=text, font=("Fixedsys", 26), fill="lightgreen", justify="center")
        self.text_items.append(item_n)
         
    def clear_text(self):
        for i in self.text_items:
            self.canvas.delete(i)
    
    # converts the units and adjust for the y axis inversion
    # 0,0 is now bottom left corner    
    def convert_to_canvas_coord(self, x, y):
        h = self.ch - (self.ch / self.area_h) * y - self.c_center_h
        w = (self.cw / self.area_w) * x + self.c_center_w
        return vec.V2(w, h)
    
    # draw a square centered to the point
    def draw_point(self,v, cvsize, kwargs):
        v = self.convert_to_canvas_coord(v.x(), v.y())
        sizev = vec.V2(cvsize, cvsize)
        
        lp = v - sizev / 2 # low point
        hp = v + sizev / 2 # high point
        
        return self.canvas.create_rectangle(lp.x(), lp.y(), hp.x(), hp.y(), **kwargs)
    
    # draw a line
    def draw_edge(self, start, end, kwargs):
        vx = self.convert_to_canvas_coord(start.x(), start.y())
        vy = self.convert_to_canvas_coord(end.x(), end.y())
        
        return self.canvas.create_line(vx.x(), vx.y(), vy.x(), vy.y(), **kwargs)
    
    # draw an entire 2d polygon
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
                
                # check-in that the primitive has been drawn
                self.drawn_edges.drawn[i].checked_in = True
    
    # removes edges and vertexes not needed anymore
    def clear_area(self):
        # create a new list
        tmp_drawn = []
        
        # add the edges to keep and remove the one that are not needed anymore
        for e in self.drawn_edges.drawn:
            if e.checked_in == False:
                self.canvas.delete(e.item_n)
                if e.v1_item_n:
                    self.canvas.delete(e.v1_item_n)
                    self.canvas.delete(e.v2_item_n)
            else:
                tmp_drawn.append(e)
        
        # the new filtered list becomes the the list
        self.drawn_edges.drawn = tmp_drawn
        self.drawn_edges.reset_check_in()
    
    # transform a 4d polygon to a 2d one
    def project4(self, poly):
        p2 = self.project_method.project(poly)
        return p2
    
    # draw all the polygons in a list
    def draw_plist(self, p_list):
        for p in p_list:
            p2 = self.project4(p)
            self.draw_poly(p2, True)

#==============================================================================
# Perspective projection    
#==============================================================================

class ProjectCam:
    
    def __init__(self):
        # 3d cam
        self.cam3 = prj.Cam3()
        self.cam3.change_position(vec.V3(2.5, 2.5, 2.5))    
        
        # 4d cam
        self.cam4 = prj.Cam4()
        self.cam4.change_position(vec.V4(15, 0.1, 0.1, 0.1))
        
        # construct the index to axis mapping for the 3d-rotations
        self.idx_to_axis = {}
        for i in range(3):
            axis = [0 for k in range(3)]
            axis[i] = 1
            self.idx_to_axis[i] = vec.V3(axis)
    
    # projects 4d to 2d
    def project(self, poly4):
        # copy values like edges and colors
        polygon = copy.deepcopy(poly4)
        
        # calculate new vertexes
        for i in range(len(polygon.v_list)):
            p3 = self.cam4.prj(polygon.v_list[i])      
            p2 = self.cam3.prj(p3)
            polygon.v_list[i] = p2
        return polygon
    
    # rotate the camera in the 3-space
    def rotate3(self, angles):
        # angles is a list of angles around the main axes
        # angles = [angle, angle, angle]
        for i in range(3):
            if angles[i] != 0:
                angle = math.radians(angles[i])
                axis = self.idx_to_axis[i]
                v = qua.rot_around_axis(self.cam3.From, axis, angle)
                self.cam3.change_position(v)
    
    # rotate camera in the 4-space
    def rotate4(self, angles):

        if angles[0] != 0:
            angle = math.radians(angles[0])
            rotv = rot4.rot_alpha(self.cam4.From, angle)

        if angles[1] != 0:
            angle = math.radians(angles[1])
            rotv = rot4.rot_beta(self.cam4.From, angle)
        
        if angles[2] != 0:
            angle = math.radians(angles[2])
            rotv = rot4.rot_gamma(self.cam4.From, angle)
        
        if angles[3] != 0:
            angle = math.radians(angles[3])
            rotv = rot4.rot_delta(self.cam4.From, angle)
        
        if angles[4] != 0:
            angle = math.radians(angles[4])
            rotv = rot4.rot_rho(self.cam4.From, angle)
        
        if angles[5] != 0:
            angle = math.radians(angles[5])
            rotv = rot4.rot_epsilon(self.cam4.From, angle)

        self.cam4.change_position(rotv)


#==============================================================================
# Flat projection
#==============================================================================

class ProjectFlat:
    
    def __init__(self, axes):
        # axes is a string of 2 letters corresponding to the axis to project
        
        # construct a axis to index mapping
        self.ax2coord = {}
        ax_names = "xyzw"
        for i, c in enumerate(ax_names):
            self.ax2coord[c] = i
        
        # zoom level 
        self.zoom = 0.3
        
        # i and j are then used to gather the coordinates
        # i and j must be between 0 and 3 or the above specified axes
        self.i = self.ax2coord[axes[0]]
        self.j = self.ax2coord[axes[1]]        
    
    # flatten the points according to the above description    
    def project(self, poly4): 
        # copy the polygon
        poly2 = poly.Polygon()
        poly2.color = poly4.color
        
        # extract the 2d information
        for v in poly4.v_list:
            # is specular inverted to match the the keyboard directions
            x = v[self.i] * self.zoom * -1 
            y = v[self.j] * self.zoom 
            poly2.v_list.append(vec.V2(x, y))
        
        # index / vertex class
        class EIndex:
            def __init__(self, v1, v2, e):
                self.v1 = v1
                self.v2 = v2
                self.e = e
                
        preserved = []
        
        # gather the edges of the 4d polygon
        for e in poly4.e_list:
            # gather the vertexes of the projected polygon
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
        
        # construct the edge list based on the is close filtering above
        # this reduces the number of edges to draw by 4 on average
        poly2.e_list = [ei.e for ei in preserved]
            
        return poly2    