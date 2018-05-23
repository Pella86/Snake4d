# -*- coding: utf-8 -*-
"""
Created on Thu May 17 15:34:47 2018

@author: Mauro
"""

import vec

class Polygon:
    def __init__(self):
        self.v_list = []
        self.e_list = []
        self.color = "red"

def cube3d(v1,v2):
    polygon = Polygon()
    
    v3 = vec.V3(v1[0],v2[1],v1[2])
    v4 = vec.V3(v2[0],v1[1],v2[2])
    v5 = vec.V3(v2[0],v2[1],v1[2])
    v6 = vec.V3(v2[0],v1[1],v1[2])
    v7 = vec.V3(v1[0],v1[1],v2[2])
    v8 = vec.V3(v1[0],v2[1],v2[2])
    
    polygon.v_list.append(v1)
    polygon.v_list.append(v2)
    polygon.v_list.append(v3)
    polygon.v_list.append(v4)
    polygon.v_list.append(v5)
    polygon.v_list.append(v6)
    polygon.v_list.append(v7)
    polygon.v_list.append(v8)
    
    polygon.e_list.append((0,5))
    polygon.e_list.append((5,4))
    polygon.e_list.append((4,2))
    polygon.e_list.append((2,0))
    
    polygon.e_list.append((5,3))
    polygon.e_list.append((4,1))
    polygon.e_list.append((2,7))
    polygon.e_list.append((0,6))

    polygon.e_list.append((1,3))
    polygon.e_list.append((3,6))
    polygon.e_list.append((6,7))
    polygon.e_list.append((7,1))
    
    return polygon

def cube4d(v0,v1):
    polygon = Polygon()
    
    polygon.v_list.append(v0)
    polygon.v_list.append(v1)
    
    polygon.v_list.append(vec.V4(v1[0],v0[1],v0[2],v0[3])) #v2
    polygon.v_list.append(vec.V4(v1[0],v1[1],v0[2],v0[3])) #v3
    polygon.v_list.append(vec.V4(v0[0],v1[1],v0[2],v0[3])) #v4
    polygon.v_list.append(vec.V4(v0[0],v0[1],v1[2],v0[3])) #v5
    polygon.v_list.append(vec.V4(v1[0],v0[1],v1[2],v0[3])) #v6
    polygon.v_list.append(vec.V4(v1[0],v1[1],v1[2],v0[3])) #v7
    polygon.v_list.append(vec.V4(v0[0],v1[1],v1[2],v0[3])) #v8
    
    polygon.v_list.append(vec.V4(v0[0],v0[1],v0[2],v1[3]))
    polygon.v_list.append(vec.V4(v1[0],v0[1],v0[2],v1[3]))
    polygon.v_list.append(vec.V4(v1[0],v1[1],v0[2],v1[3]))
    polygon.v_list.append(vec.V4(v0[0],v1[1],v0[2],v1[3]))
    polygon.v_list.append(vec.V4(v0[0],v0[1],v1[2],v1[3]))
    polygon.v_list.append(vec.V4(v1[0],v0[1],v1[2],v1[3]))
    polygon.v_list.append(vec.V4(v0[0],v1[1],v1[2],v1[3]))
    
    polygon.e_list.append((0,2))
    polygon.e_list.append((0,9))
    polygon.e_list.append((2,3))
    polygon.e_list.append((2,10))
    polygon.e_list.append((3,4))
    polygon.e_list.append((3,11))
    polygon.e_list.append((4,0))
    polygon.e_list.append((4,12))
    
    polygon.e_list.append((0,5))
    polygon.e_list.append((2,6))
    polygon.e_list.append((4,8))
    polygon.e_list.append((3,7))
    
    polygon.e_list.append((5,6))
    polygon.e_list.append((5,13))
    polygon.e_list.append((6,7))
    polygon.e_list.append((6,14))
    polygon.e_list.append((7,8))
    polygon.e_list.append((7,1))
    polygon.e_list.append((8,5))
    polygon.e_list.append((8,15))
    
    polygon.e_list.append((9,10))
    polygon.e_list.append((10,11))
    polygon.e_list.append((11,12))
    polygon.e_list.append((12,9))
    
    polygon.e_list.append((10,14))
    polygon.e_list.append((11,1))
    polygon.e_list.append((12,15))
    polygon.e_list.append((9,13))
    
    polygon.e_list.append((13,14))
    polygon.e_list.append((14,1))
    polygon.e_list.append((1,15))
    polygon.e_list.append((15,13))
    return polygon

def create_cube4d( point, size, color):
    v = vec.V4(1, 1, 1, 1) * size/2.0
    
    higher = point + v
    lower = point - v

    c = cube4d(lower,higher)
    c.color = color
    return c