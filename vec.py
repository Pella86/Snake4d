# -*- coding: utf-8 -*-
"""
Created on Wed May 16 22:37:10 2018

@author: Mauro
"""

# Vector utility for 2, 3, 4 dimensions

import math

# is close constant
epsilon = 0.00000001

class VecExcept(Exception):
    pass


class Vector:
    
    def __init__(self, dimensions, coords = None):
        if coords is None:
            self.coords = [0 for i in range(dimensions)]
        else:
            self.coords = coords
            
        self.dimension = dimensions
    
    def __getitem__(self, i):
        return self.coords[i]

    def __setitem__(self, i, v):
        self.coords[i] = v
    
    def get_set_coord(self, coord_idx, value = False):
        if value:
            self.coords[coord_idx] = value
        return self.coords[coord_idx]
    
    def magnitude(self):
        s = 0
        for c in self.coords:
            s += c**2
        return math.sqrt(s)
    
    def check_dimensions(self, v2):
        if self.dimension != v2.dimension:
            raise  VecExcept("wrong dimensions")  
    
    def normalize(self):
        m = self.magnitude()
        for i in range(self.dimension):
            self.coords[i] /= m
        return self
            
    def angle(self, v2):
        m = self.magnitude() * v2.magnitude()
        if m != 0:
            cos_theta = (self.dot(v2) ) / m
            return math.acos(cos_theta)
        else:
            VecExcept("Zero Division Error")      
 
    def dot(self, v2):
        self.check_dimensions(v2)
        dot_p = 0
        for i in range(self.dimension):
            dot_p += self.coords[i] * v2[i]
        return dot_p           
    
    def check_class(self, v2):
        return self.__class__ == v2.__class__
    
    def __add__(self, v2):
        self.check_dimensions(v2)        
       
        new_coords = [0 for i in range(self.dimension)]
        
        for i in range(self.dimension):
            new_coords[i] = self.coords[i] + v2[i]
        
        return self.__class__(new_coords)   
    
    def __sub__(self, v2):
        self.check_dimensions(v2)        
        new_coords = [0 for i in range(self.dimension)]
        for i in range(self.dimension):
            new_coords[i] = self.coords[i] - v2[i]
        return self.__class__(new_coords)   
    

    def __mul__(self, k):
        # if k is a vector do the dot product
        new_coords = [0 for i in range(self.dimension)]
        for i in range(self.dimension):
            new_coords[i] = self.coords[i] * k
        return self.__class__(new_coords)
    
    def __truediv__(self, d):
        if d == 0: raise VecExcept("Zero Division Error")
        new_coords = [0 for i in range(self.dimension)]
        for i in range(self.dimension):
            new_coords[i] = self.coords[i] / d
        return self.__class__(new_coords)        
    
    def __eq__(self, v2):
        self.check_dimensions(v2)
        for i in range(self.dimension):
            if self.coords[i] != v2[i]:
                return False
        return True

    def is_close(self, v2):
        self.check_dimensions(v2)
        
#        if abs(self.dot(v2)) > epsilon:
#            return False
#        for i in range(self.dimension):
#            if self.coords[i] - v2[i] > epsilon:
#                return False

        for i in range(self.dimension):
            if abs(self.coords[i] - v2[i]) > epsilon:
                return False
        return True        
        
    def __str__(self):
        s = "("
        for c in self.coords:
            s += "{:.5g}".format(c) + ":"
        s = s[:-1] + ")"
        return s


class V2(Vector):
    
    def __init__(self, x, y = None):

        if y is None and type(x) is list:
            super().__init__(2, x)
        else:
            super().__init__(2)
            self.coords[0] = x
            self.coords[1] = y
    
    def x(self, c = False):
        return self.get_set_coord(0, c)

    def y(self, c = False):
        return self.get_set_coord(1, c)

class V3(Vector):
    
    def __init__(self, x, y = None, z = None):

        if y is None and z is None and type(x) is list:
            super().__init__(3, x)      
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

    def cross(self, v2):
        x = self[1] * v2[2] - self[2] * v2[1]
        y = self[2] * v2[0] - self[0] * v2[2]
        z = self[0] * v2[1] - self[1] * v2[0]
        return V3(x,y,z)
    
class V4(Vector):
    
    def __init__(self, x, y = None, z = None, w = None):
        if y is None and z is None and w is None and type(x) is list:
            super().__init__(4, x)         
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
#    v2a = V2(0, 1)
#    
#    v2b = V2(1, 0)
#    
#    v2c = v2a + v2b
#    print(v2c)
#    
#    print(v2a, v2b, v2c)
#    
#    print(type(v2c))
#    
#    print("--------------")
#    
#    v3a = V3(0, 0, 1)
#    v3b = V3(1, 0, 1)
#    v3c = (v3a + v3b) / 2
#    print(type(v3c))
#    
#    print(v3c, type(v3c))
    
#    v3 = V3(0, 2, 3)
#    
#    print(v2a)
#    print(v3)
#    
#    try:
#        print(v2 + v3)
#    except VecExcept:
#        pass
    
#    v3a = V3(1, 2, 3)
#    v3b = V3(3, 4, 5)
#    
#    print(v3a, v3b)
    
#    v3a = V3(3, 4, 5)
#    
#    v3c = v3a + v3 * 5
#    
#    print(v3c)
#    print(v3c.magnitude())
#
#    
#    print(v3, v3a)    
#    dotprod = v3.dot(v3a)
#    
#    print(dotprod)
#    
#    a = v3.angle(V3(0,0,1))
#    
#    print(math.degrees(a))
#    
#    crossr = v3.cross(V3(0,0,1))
#    
#    print(crossr)
#    
#    print(crossr.normalize())

    a = V4(4, 1, 2, 3)
    b = V4(3, 2, 1, 1)
    c = V4(1, 2, 3, 2)
    
    print(a.cross(b, c).normalize())
    
    
    
    
