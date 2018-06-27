# -*- coding: utf-8 -*-
"""
Created on Wed May 16 23:46:53 2018

@author: Mauro
"""

#==============================================================================
# Quaternion utilities
#==============================================================================

import math, vec
import copy

class Q(vec.V4):
    
    # possibly change in Q(x,y,z,w) or Q(s, v)
    def __init__(self, w, x, y = None, z = None):
        
        # if the first argument is a vector
        if isinstance(x, vec.V3):
            y = x[1]
            z = x[2]
            x = x[0]

        super().__init__(x, y, z, w)
    
    # inverse of the quaternion
    def qi(self):
        for i in range(0, self.dimension - 1):
            self.coords[i] = -self.coords[i]
        return self
    
    # cross product
    def cross(self, q2):
        s1 = self.w()
        s2 = q2.w()

        v1 = vec.V3(self.x(), self.y(), self.z())
        v2 = vec.V3(  q2.x(),   q2.y(),   q2.z())
        
        s3 = s1 * s2 - (v1.dot(v2))
        
        v3 = (v2 * s1 + v1 * s2) + v1.cross(v2)

        return Q(s3, v3)
    
    # hamilton multiplication
    def hamilton(self, q):
        a1 = self.w()
        a2 = q.w()
        
        b1 = self.x()
        b2 = q.x()
        
        c1 = self.y()
        c2 = q.y()
        
        d1 = self.z()
        d2 = q.z()
        
        w = a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2
        x = a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2
        y = a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2
        z = a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2
        
        return Q(w, x, y, z)
    
    # get the vector part of the quaternion
    def get_vector(self):
        return vec.V3(self.x(), self.y(), self.z())
        
    
def rot_around_axis(point, axis, angle):
    axis.normalize()
    # construct the quaternion
    s = math.cos(angle / 2)
    v = axis * math.sin(angle /2)
    
    q = Q(s, v)
    qi = copy.deepcopy(q).qi()
    
    p = Q(0, point)
    
    prot = q.cross(p).cross(qi)
    return vec.V3(prot.x(), prot.y(), prot.z())
        
if __name__ == "__main__":
    
    print("----------")
    
    q1 = Q(1,2,3,4)
    
    print(q1)
    
    q2 = Q(5, vec.V3(1, 2, 3))    
    
    print(q2)
    
    print(q1.cross(q2))
    
    
    print("----------")
    
    # temptative quaternion rotation
    # problem is to find the given angle and axis
    # probably use bivectors or a rotor
    qL = Q(1, 0, 0, 0)
    qL.normalize()
    qR = Q(0, 0, 1, 0)
    qR.normalize()
    
    p = vec.V4(1, 1, 1, 1)
    
    pi = qL.hamilton(p).hamilton(qR)
    
    print(pi)
    