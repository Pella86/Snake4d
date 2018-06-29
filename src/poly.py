# -*- coding: utf-8 -*-
"""
Created on Thu May 17 15:34:47 2018

@author: Mauro
"""

import copy

import vec
import bfh


#==============================================================================
# Polygon class
# simple utility for the polygon class
#==============================================================================

class Polygon:
    def __init__(self):
        self.v_list = []
        self.e_list = []
        self.f_list = []
        self.color = "red"
    
    def as_bytes(self, bf):
        bf.write_string(self.color)
        
        # write vertex list
        
        bf.write("I", len(self.v_list))
        
        for v in self.v_list:
            v.as_bytes(bf)
        
        # write edge list
        
        earr = []
        for e in self.e_list:
            earr.append(e[0])
            earr.append(e[1])
        
        earrlen = len(earr)
        bf.write("I", earrlen)
        for e in earr:
            bf.write("I", e)
        
        # write face list
        farr = []
        for f in self.f_list:
            farr.append(f[0])
            farr.append(f[1])
            farr.append(f[2])
            farr.append(f[3])
        
        farrlen = len(farr)
        bf.write("I", farrlen)
        for f in farr:
            bf.write("I", f) 
            
    def interpret_bytes(self, bf):
        # read the color
        self.color = bf.read_string()
        
        # read vertex list
        v_list = []
        
        # read len
        v_len = bf.read("I")
        
        for i in range(v_len):
            v4 = vec.V4(0, 0, 0, 0)
            v4.interpret_bytes(bf)
            v_list.append(v4)
        
        self.v_list = v_list
        # read edge list
        earrlen = bf.read("I")
        half_earrlen = int(earrlen / 2)
        
        self.e_list = [[0,0] for i in range(half_earrlen)]
        
        earr = []            
        for i in range(earrlen):
            e = bf.read("I")
            earr.append(e)
        
        for i in range(half_earrlen):                
            self.e_list[i][0] = earr[i*2]
            self.e_list[i][1] = earr[i*2 + 1]

        # read face list
        farrlen = bf.read("I")
        half_farrlen = int(farrlen / 4)
        
        self.f_list = [[0,0, 0, 0] for i in range(half_farrlen)]
        
        farr = []
        for i in range(farrlen):
            f = bf.read("I")
            farr.append(f)
        
        for i in range(half_farrlen):
            self.f_list[i][0] = farr[i*4]
            self.f_list[i][1] = farr[i*4 + 1]
            self.f_list[i][2] = farr[i*4 + 2]
            self.f_list[i][3] = farr[i*4 + 3]
        
   
    
    def write_file(self, filename):
        print("-- write --")
        with open(filename, "wb") as f:
            bf = bfh.BinaryFile(f)
            self.as_bytes(bf)
    
    def read_file4(self, filename):
        print("-- read --")
        with open(filename, "rb") as f:
            bf = bfh.BinaryFile(f)
            self.interpret_bytes(bf)
            

#==============================================================================
# Generate 3d cube
#==============================================================================

# v1, v2 are the respectively lower and upper corner
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

#==============================================================================
# Generate hypercube
#==============================================================================

# v0 and v1 are respectively the lower and upper corner
def cube4d(v0,v1):
    polygon = Polygon()
    
    polygon.v_list.append(v0) #v0
    polygon.v_list.append(v1) #v1
    
    polygon.v_list.append(vec.V4(v1[0],v0[1],v0[2],v0[3])) #v2
    polygon.v_list.append(vec.V4(v1[0],v1[1],v0[2],v0[3])) #v3
    polygon.v_list.append(vec.V4(v0[0],v1[1],v0[2],v0[3])) #v4
    polygon.v_list.append(vec.V4(v0[0],v0[1],v1[2],v0[3])) #v5
    polygon.v_list.append(vec.V4(v1[0],v0[1],v1[2],v0[3])) #v6
    polygon.v_list.append(vec.V4(v1[0],v1[1],v1[2],v0[3])) #v7
    polygon.v_list.append(vec.V4(v0[0],v1[1],v1[2],v0[3])) #v8
    
    polygon.v_list.append(vec.V4(v0[0],v0[1],v0[2],v1[3])) #v9
    polygon.v_list.append(vec.V4(v1[0],v0[1],v0[2],v1[3])) #v10
    polygon.v_list.append(vec.V4(v1[0],v1[1],v0[2],v1[3])) #v11
    polygon.v_list.append(vec.V4(v0[0],v1[1],v0[2],v1[3])) #v12
    polygon.v_list.append(vec.V4(v0[0],v0[1],v1[2],v1[3])) #v13
    polygon.v_list.append(vec.V4(v1[0],v0[1],v1[2],v1[3])) #v14
    polygon.v_list.append(vec.V4(v0[0],v1[1],v1[2],v1[3])) #v15
    
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

    polygon.f_list.append((1,14,6,7))
    polygon.f_list.append((6,2,3,7))
    polygon.f_list.append((2,10,11,3))
    polygon.f_list.append((10,14,1,11))

    polygon.f_list.append((7,6,5,8))
    polygon.f_list.append((3,2,0,4))
    polygon.f_list.append((11,10,9,12))
    polygon.f_list.append((1,14,13,15))

    polygon.f_list.append((14,6,5,13))
    polygon.f_list.append((6,2,0,5))
    polygon.f_list.append((2,10,9,0))
    polygon.f_list.append((10,14,13,9))

    polygon.f_list.append((1,15,8,7))
    polygon.f_list.append((8,4,3,7))
    polygon.f_list.append((4,12,11,3))
    polygon.f_list.append((12,15,1,11))

    polygon.f_list.append((1,11,3,7))
    polygon.f_list.append((14,6,2,10))
    polygon.f_list.append((15,8,4,12))
    polygon.f_list.append((13,5,0,9))

    polygon.f_list.append((15,13,5,8))
    polygon.f_list.append((5,8,4,0))
    polygon.f_list.append((0,4,12,9))
    polygon.f_list.append((13,9,12,15))

    return polygon

#==============================================================================
# Generate an hypercube given a center and a size
#==============================================================================

def create_cube4d( point, size, color):
    v = vec.V4(1, 1, 1, 1) * size/2.0
    
    higher = point + v
    lower = point - v

    c = cube4d(lower,higher)
    c.color = color
    return c


if __name__ == "__main__":
    
    c4 = cube4d(vec.V4(-1, -1, -1, -1), vec.V4(1, 1, 1, 1))
    
    c4.write_file("./test_poly.poly")
    
    c4.read_file4("./test_poly.poly")