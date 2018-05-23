# -*- coding: utf-8 -*-
"""
Created on Wed May 16 23:46:53 2018

@author: Mauro
"""

import math, vec
import copy

class Z(vec.V2):
    
    def __init__(self, im, re):
        super().__init__(im, re)

    def re(self, value = False):
        return self.get_set_coord(0, value)    

    def im(self, value = False):
        return self.get_set_coord(1, value)

    def zi(self):
        self.im(-self.im())
        return self

class Q(vec.V4):
    
    def __init__(self, w, x, y = None, z = None):
        
        if isinstance(x, vec.V3):
            y = x[1]
            z = x[2]
            x = x[0]

        super().__init__(x, y, z, w)
        
    def qi(self):
        for i in range(0, self.dimension - 1):
            self.coords[i] = -self.coords[i]
        return self
    
    def cross(self, q2):
        s1 = self.w()
        s2 = q2.w()

        v1 = vec.V3(self.x(), self.y(), self.z())
        v2 = vec.V3(  q2.x(),   q2.y(),   q2.z())
        
        s3 = s1 * s2 - (v1.dot(v2))
        
        v3 = (v2 * s1 + v1 * s2) + v1.cross(v2)

        return Q(s3, v3)
    
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
    

def rotx(theta):
    s = math.cos(theta / 2)
    u = vec.V3(1, 0, 0)
    v = u * math.sin(theta / 2)
    return Q(s, v)

def rotx_point(point, theta):
    p = Q(0, point)
    q = rotx(theta)
    q1 = copy.deepcopy(q)
    q1.qi()
    
    prot = q.cross(p).cross(q1)
    return vec.V3(prot.x(), prot.y(), prot.z())

    
#def rotx(theta):
#	s = cos(theta/2)
#	u = V3(1,0,0)
#	v = scalar3(sin(theta/2),u)
#	return SQ(s,v)
#
#def rotx_point(point,theta):
#	p = Q(0,point.c[0],point.c[1],point.c[2])
#	q = rotx(theta)
#	q1 = q.qi()
#	prot = qxq(qxq(q,p),q1)
#	return  V3(prot.x,prot.y,prot.z)
        
if __name__ == "__main__":
    
    z1 = Z(1, 3)
    
    z1.zi()
    
    print(z1)
    
    print(z1.magnitude())
    
    print("----------")
    
    q1 = Q(1,2,3,4)
    
    print(q1)
    
    q2 = Q(5, vec.V3(1, 2, 3))    
    
    print(q2)
    
    print(q1.cross(q2))
    
    print("----------")
   
    v1 = vec.V3(1, 1, 0)
    
    t = math.radians(90)
    
    v2 = rotx_point(v1, t)
    
    print(v2)
    
    print("----------")
    
    qL = Q(1, 0, 0, 0)
    qL.normalize()
    qR = Q(0, 0, 1, 0)
    qR.normalize()
    
    p = vec.V4(1, 1, 1, 1)
    
    pi = qL.hamilton(p).hamilton(qR)
    
    print(pi)
    