# -*- coding: utf-8 -*-
"""
Created on Wed May 16 23:45:48 2018

@author: Mauro
"""
#==============================================================================
# Camera utilities
#==============================================================================

import vec, math

#==============================================================================
# Errors
#==============================================================================

class CamExcept(Exception):
    pass

#==============================================================================
# 3d camera
#==============================================================================

class Cam3:

    def __init__(self):
        
        # vertex where the camera is
        self.From = vec.V3(0,0,5)
        
        # vertex where the camera points
        self.To = vec.V3(0,0,0)
        
        # up direction
        self.Up = vec.V3(0,1,0)
        
        # transformation matrix
        self.t_matrix = self.calc_tmatrix()
        
        # 2d screen projection sizes
        self.Lx = 7
        self.Ly = 7
        
        # center of 2d screen
        self.Cx = 0
        self.Cy = 0
        
        # view angle (set to 60 deg by default)
        self.view_angle = math.pi/3

    def calc_tmatrix(self):
        ''' calculate the transformation matrix '''
        
        C = self.To - self.From        
        C.normalize()
        
        A = self.Up.cross(C)            
        A.normalize()

        B = C.cross(A)  
        if B.magnitude() == 0: CamExcept("Cam3: t matrix B is 0")
        #B.normalize() apparently useless?
        
        return [A,B,C]

    def prj(self,point):
        ''' project a point on the 2d screen '''
        
        if point == vec.V3(0, 0, 0): raise CamExcept("Cam3: point is 0")
        
        V = point - self.From

        T = 1 / math.tan(self.view_angle / 2)
        
        div = V.dot(self.t_matrix[2])
        
        if div == 0: CamExcept("Cam3: S div is 0")
        
        S = T / div

        Sx = self.Cx + (self.Lx * S * V.dot(self.t_matrix[0]))
        Sy = self.Cx + (self.Lx * S * V.dot(self.t_matrix[1]))

        return vec.V2(Sx,Sy)
    
    # changing position of the target or form means to calculate the transform
    # matrix again
    
    def change_target(self, t):
        self.To = t
        self.t_matrix = self.calc_tmatrix()
    
    def change_position(self, p):
        self.From = p
        self.t_matrix = self.calc_tmatrix()

#==============================================================================
# 4d Camera
#==============================================================================

class Cam4:
    
    def __init__(self):
        self.From = vec.V4(10, 0, 0, 0)
        self.To =  vec.V4(0,0,0,0)
        self.Up =  vec.V4(0,1,0,0)
        self.Over = vec.V4(0,0,1,0)
        
        self.t_matrix = self.calc_tmatrix()
        
        # prjection screen cube center
        self.Bx = 0
        self.By = 0
        self.Bz = 0
        
        # projection screen cube dimensions
        self.Lx = 1.5
        self.Ly = 1.5
        self.Lz = 1.5
        
        # 4d view angle (set at 60 deg by default)
        self.view_angle = math.pi/3    
         
    def calc_tmatrix(self):
        '''calculates the transformation matrix'''
        
        D = self.To - self.From
        D.normalize()
        
        A = self.Up.cross(self.Over, D)
        A.normalize()
        
        B = self.Over.cross(D, A)
        B.normalize()

        C = D.cross(A, B)
        if C.magnitude() == 0: raise CamExcept("Cam4: C module is 0")

        return [A,B,C,D]    
 
    def prj(self, point):
        '''project the a 4d point into a 3d cube screen'''
        point = point - self.From
        if point == vec.V4(0, 0, 0, 0): raise CamExcept("Cam4: prj point null vec")
        
        T = 1/(math.tan(self.view_angle)/2)
        
        S = T / (point.dot(self.t_matrix[3]))
        
        x = self.Bx + (self.Lx * S * point.dot(self.t_matrix[0]))
        y = self.By + (self.Ly * S * point.dot(self.t_matrix[1]))
        z = self.Bz + (self.Lz * S * point.dot(self.t_matrix[2]))
        
        return vec.V3(x,y,z)

    def change_target(self, t):
        self.To = t
        self.t_matrix = self.calc_tmatrix()
    
    def change_position(self, p):
        self.From = p
        self.t_matrix = self.calc_tmatrix()

if __name__ == "__main__":
    
    cam = Cam4()
    
    p = vec.V4(1, 1, 1, 1)
    p_proj = cam.prj(p)
    
    print(p_proj)
    
    cam = Cam3()
    
    p_proj = cam.prj(p_proj)
    
    print(p_proj)
    
