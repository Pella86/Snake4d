# -*- coding: utf-8 -*-
"""
Created on Wed May 16 22:37:10 2018

@author: Mauro
"""

#==============================================================================
# # Vector utility for 2, 3, 4 dimensions
#==============================================================================

import math

import bfh

#==============================================================================
# Constants
#==============================================================================

# is close constant
epsilon = 0.00000001

#==============================================================================
# Helpers
#==============================================================================


        
#==============================================================================
# Errors
#==============================================================================

class VecExcept(Exception):
    pass

#==============================================================================
# Vector base class
#==============================================================================

class Vector:
    
    def __init__(self, dimensions, coords = None):
        if isinstance(dimensions, str):
            self.read_file(dimensions)
        else:
            if coords is None:
                self.coords = [0 for i in range(dimensions)]
            else:
                self.coords = coords
                
            self.dimension = dimensions
    
    # setter and getter
    def __getitem__(self, i):
        return self.coords[i]

    def __setitem__(self, i, v):
        self.coords[i] = v
    
    # allows to define return v.x() and v.x() = 5
    def get_set_coord(self, coord_idx, value = False):
        if value:
            self.coords[coord_idx] = value
        return self.coords[coord_idx]
    
    # magnitude of the vector
    def magnitude(self):
        s = 0
        for c in self.coords:
            s += c**2
        return math.sqrt(s)
    
    # helper function for checking the dimensions
    def check_dimensions(self, v2):
        if self.dimension != v2.dimension:
            raise  VecExcept("Vector: wrong dimensions")  

    def check_class(self, v2):
        return self.__class__ == v2.__class__
  
    # normalize to 1
    def normalize(self):
        m = self.magnitude()
        if m == 0: VecExcept("Vector: module is 0")
        for i in range(self.dimension):
            self.coords[i] /= m
        return self
    
    # angle from a axis        
    def angle(self, v2):
        m = self.magnitude() * v2.magnitude()
        if m != 0:
            cos_theta = (self.dot(v2) ) / m
            return math.acos(cos_theta)
        else:
            VecExcept("Vector: Zero Division Error")      

    # dot product
    def dot(self, v2):
        self.check_dimensions(v2)
        dot_p = 0
        for i in range(self.dimension):
            dot_p += self.coords[i] * v2[i]
        return dot_p           
    
    # operator + (elementwise sum)    
    def __add__(self, v2):
        self.check_dimensions(v2)        
       
        new_coords = [0 for i in range(self.dimension)]
        
        for i in range(self.dimension):
            new_coords[i] = self.coords[i] + v2[i]
        
        return self.__class__(new_coords)   
    
    # operator - (elementwise subtraction)
    def __sub__(self, v2):
        self.check_dimensions(v2)        
        new_coords = [0 for i in range(self.dimension)]
        for i in range(self.dimension):
            new_coords[i] = self.coords[i] - v2[i]
        return self.__class__(new_coords)   
    
    # operator * (elementwise multiplication with a constant)
    def __mul__(self, k):
        # if k is a vector do the dot product
        new_coords = [0 for i in range(self.dimension)]
        for i in range(self.dimension):
            new_coords[i] = self.coords[i] * k
        return self.__class__(new_coords)
    
    # operator / (elementwise division)
    def __truediv__(self, d):
        if d == 0: raise VecExcept("Vector: Zero Division Error")
        new_coords = [0 for i in range(self.dimension)]
        for i in range(self.dimension):
            new_coords[i] = self.coords[i] / d
        return self.__class__(new_coords)        
    
    # operator == (check exactly if the vectors are the same)
    def __eq__(self, v2):
        self.check_dimensions(v2)
        for i in range(self.dimension):
            if self.coords[i] != v2[i]:
                return False
        return True

    # if the vector are close enough they are considered the same
    def is_close(self, v2):
        self.check_dimensions(v2)

        for i in range(self.dimension):
            if abs(self.coords[i] - v2[i]) > epsilon:
                return False
        return True        
    
    # representation to string    
    def __str__(self):
        s = "("
        for c in self.coords:
            s += "{:.5g}".format(c) + ":"
        s = s[:-1] + ")"
        return s
    
    def as_bytes(self, bf):
        bf.write("I", self.dimension)
        for c in self.coords:
            bf.write("d", c)
    
    def interpret_bytes(self, bf):
        self.dimension = bf.read('I')
        
        self.coords = [0 for i in range(self.dimension)]
        for i in range(self.dimension):
            self.coords[i] = bf.read('d')   

    def write_file(self, filename):
        with open(filename, "wb") as f:
            # save dimenstions
            bf = bfh.BinaryFile(f)
            self.as_bytes(bf)
    
    def read_file(self, filename):
        with open(filename, "rb") as f:
            bf = bfh.BinaryFile(f)
            self.interpret_bytes(bf)
#==============================================================================
# 2d vector
#==============================================================================

class V2(Vector):
    
    def __init__(self, x, y = None):

        if y is None and type(x) is list:
            super().__init__(2, x)
        elif y is None and type(x) is str:
            super().__init__(x)
        else:
            super().__init__(2)
            self.coords[0] = x
            self.coords[1] = y
    
    def x(self, c = False):
        return self.get_set_coord(0, c)

    def y(self, c = False):
        return self.get_set_coord(1, c)

#==============================================================================
# 3d vector
#==============================================================================

class V3(Vector):
    
    def __init__(self, x, y = None, z = None):

        if y is None and z is None and type(x) is list:
            super().__init__(3, x)      
        elif y is None and type(x) is str:
            super().__init__(x)
        else:
            super().__init__(3)
            self.coords[0] = x
            self.coords[1] = y
            self.coords[2] = z            

    def x(self, c = False):
        return self.get_set_coord(0, c)

    def y(self, c = False):
        return self.get_set_coord(1, c)

    def z(self, c = False):
        return self.get_set_coord(2, c)  
    
    # cross product between 2 vectors
    def cross(self, v2):
        x = self[1] * v2[2] - self[2] * v2[1]
        y = self[2] * v2[0] - self[0] * v2[2]
        z = self[0] * v2[1] - self[1] * v2[0]
        return V3(x,y,z)

#==============================================================================
# 4d vector    
#==============================================================================

class V4(Vector):
    
    def __init__(self, x, y = None, z = None, w = None):
        if type(x) is list and y is None and z is None and w is None:
            super().__init__(4, x)         
        elif y is None and type(x) is str:
            super().__init__(x)
        else:
            super().__init__(4)
            self.coords[0] = x
            self.coords[1] = y
            self.coords[2] = z
            self.coords[3] = w

    def x(self, c = False):
        return self.get_set_coord(0, c)

    def y(self, c = False):
        return self.get_set_coord(1, c)

    def z(self, c = False):
        return self.get_set_coord(2, c)  

    def w(self, c = False):
        return self.get_set_coord(3, c) 

    def cross(self, v, w):
        A = (v[0] * w[1])-(v[1] * w[0])
        B = (v[0] * w[2])-(v[2] * w[0])
        C = (v[0] * w[3])-(v[3] * w[0])
        D = (v[1] * w[1])-(v[2] * w[1])
        E = (v[1] * w[3])-(v[3] * w[1])
        F = (v[2] * w[3])-(v[3] * w[2])
        
        x =  (self[1] * F)-(self[2] * E)+(self[3] * D)
        y = -(self[0] * F)+(self[2] * C)-(self[3] * B)
        z =  (self[0] * E)-(self[1] * C)+(self[3] * A)
        w = -(self[0] * D)+(self[1] * B)-(self[2] * A)
        
        return V4(x, y, z, w)



if __name__ == "__main__":
#    print("vector math utilites")
#    
#    print("------- 2d -------")
#    
#    va = V2(0, 1)
#    print("va:", va)
#    
#    vb = V2(1, 0)
#    print("vb:", vb)
#    
#    vc = va + vb
#    print("sum:", vc)
#    
#    print("------- 3d -------")
#    
#    va = V3(0, 0, 1)
#    print("va:", va)
#    print("angle to x axis:", math.degrees(va.angle(V3(1, 0, 0))))
#    
#    vb = V3(1, 0, 1)
#    print("vb:", vb)
#    
#    vc = (va + vb) / 2
#    print("mean:", vc)
#    
#    print("mag:", vc.magnitude())
#    print("dot:", vc.dot(va))
#    
#    print("cross:", vc.cross(va))
#
#     
#    v2 = V2(1, 0)
#    v3 = V3(1, 0, 0)
#    
#    try:
#        v = v2 + v3
#    except VecExcept as e:
#        print(e)
#        
#    print("------- 4d -------")
#
#    a = V4(4, 1, 2, 3)
#    b = V4(3, 2, 1, 1)
#    c = V4(1, 2, 3, 2)
#    
#    print("cross 4:", a.cross(b, c).normalize())
    
    v4 = V4(1.2, 1.5, 1.6, 2042104.2)
    
    print("--- write ---")
    v4.write_file("./test_vector.vec")
    
    print("--- read ---")
    v4read = V4("./test_vector.vec")
    print(v4read)
    
    
    
    
