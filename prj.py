# -*- coding: utf-8 -*-
"""
Created on Wed May 16 23:45:48 2018

@author: Mauro
"""

import vec, math


class CamExcept(Exception):
    pass

class Cam3:

    def __init__(self):
        self.From = vec.V3(0,0,5)
        
        self.To = vec.V3(0,0,0)
        
        self.Up = vec.V3(0,1,0)
        
        self.t_matrix = self.trans_matrix()

        self.Lx = 5
        self.Ly = 2.5

        self.Cx = 0
        self.Cy = 0

        self.view_angle = math.pi/4

    def trans_matrix(self):
        #construct camera transform
        C = self.To - self.From
        
        if C == vec.V3(0, 0, 0): 
            raise CamExcept("Cam3: C is 0")
        
        C.normalize()
        A = self.Up.cross(C)

        if A == vec.V3(0, 0, 0):
            raise CamExcept("Cam3: A is 0")
            
        A.normalize()

        B = C.cross(A)        
        return [A,B,C]

    def prj(self,point):
        
        if point == vec.V3(0, 0, 0): raise CamExcept("Cam3: point is 0")
        
        V = point - self.From

        T = 1 / math.tan(self.view_angle / 2)
        
        div = V.dot(self.t_matrix[2])
        
        if div == 0: CamExcept("Cam3: div is 0")
        
        S = T / div

        Sx = self.Cx + (self.Lx * S * V.dot(self.t_matrix[0]))
        Sy = self.Cx + (self.Lx * S * V.dot(self.t_matrix[1]))

        return vec.V2(Sx,Sy)
    
    def change_target(self, t):
        self.To = t
        self.t_matrix = self.trans_matrix()
    
    def change_position(self, p):
        self.From = p
        self.t_matrix = self.trans_matrix()


class Cam4:
    
    def __init__(self):
        self.From = vec.V4(10, 0, 0, 0)
        self.To =  vec.V4(0,0,0,0)
        self.Up =  vec.V4(0,1,0,0)
        self.Over = vec.V4(0,0,1,0)
        
        self.t_matrix = self.trans_matrix()


        self.Bx = 0
        self.By = 0
        self.Bz = 0
        self.Lx = 6.0
        self.Ly = 6.0
        self.Lz = 6.0
        
        self.view_angle = math.pi/4      
        
    def trans_matrix(self):
        
        D = self.To - self.From
        if D.magnitude() == 0: raise CamExcept("Cam4: D module is 0")
        D.normalize()
        
        A = self.Up.cross(self.Over, D)
        if A.magnitude() == 0: raise CamExcept("Cam4: A module is 0")
        A.normalize()
        
        B = self.Over.cross(D, A)
        if B.magnitude() == 0: raise CamExcept("Cam4: B module is 0")
        B.normalize()

        C = D.cross(A, B)
        if C.magnitude() == 0: raise CamExcept("Cam4: C module is 0")

        return [A,B,C,D]    
 
    def prj(self,point):
        point = point - self.From
        if point == vec.V4(0, 0, 0, 0): raise CamExcept("Cam4: prj point null vec")
        
        T = 1/(math.tan(self.view_angle)/2)
        
        S = T / (point.dot(self.t_matrix[3]))
        
        x = S * point.dot(self.t_matrix[0])
        y = S * point.dot(self.t_matrix[1])
        z = S * point.dot(self.t_matrix[2])
        
        return vec.V3(x,y,z)


if __name__ == "__main__":
    
    cam = Cam4()
    
    p = vec.V4(1, 1, 1, 1)
    
    p_proj = cam.prj(p)
    
    print(p_proj)

    
    cam = Cam3()
    
    
    p_proj = cam.prj(p_proj)
    
    print(p_proj)
    
