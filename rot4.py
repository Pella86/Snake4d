# -*- coding: utf-8 -*-
"""
Created on Fri May 18 20:44:22 2018

@author: Mauro
"""

import mat, vec, math

#t = math.pi
#mxy = [ [  math.cos(t), math.sin(t), 0, 0],
#        [ -math.sin(t), math.cos(t), 0, 0],
#        [            0,           0, 0, 0],
#        [            0,           0, 0, 0] ]
#
#mxy = mat.SquareMatrix(mxy)
#
#print(mxy)
#
#v = vec.V4(1, 0, 0, 0)
#vm = mat.Matrix(v.coords)
#print(vm)
#
#vrot =  mxy * vm
#print(vrot)


def rot_v(v, alpha, beta, gamma, delta, rho, epsilon):
    
    # XY Plane rot matrix
    mxy = [ [  math.cos(alpha), math.sin(alpha), 0, 0],
            [ -math.sin(alpha), math.cos(alpha), 0, 0],
            [            0,           0, 1, 0],
            [            0,           0, 0, 1] ]    
    
    mxy = mat.SquareMatrix(mxy)
    
    # YZ Plane rot matrix
    myz = [ [ 1, 0, 0, 0],
            [ 0, math.cos(beta), math.sin(beta), 0],
            [ 0, -math.sin(beta), math.cos(beta), 0],
            [ 0, 0, 0, 1] ]    
    
    myz = mat.SquareMatrix(myz)
    
    # ZX Plane rot matrix
    mzx = [ [ math.cos(gamma), 0, -math.sin(gamma), 0],
            [ 0, 1, 0, 0],
            [ math.sin(gamma), 0, math.cos(gamma), 0],
            [ 0, 0, 0, 1] ]    
    
    mzx = mat.SquareMatrix(mzx)

    # XW Plane rot matrix
    mxw = [ [ math.cos(delta), 0, 0, math.sin(delta)],
            [ 0, 1, 0, 0],
            [ 0, 0, 1, 0],
            [ -math.sin(delta), 0, 0, math.cos(delta)] ]    
    
    mxw = mat.SquareMatrix(mxw)   
    
    # YW Plane rot matrix
    myw = [ [ 1, 0, 0, 0],
            [ 0, math.cos(rho), 0, -math.sin(rho)],
            [ 0, 0, 1, 0],
            [ 0, math.sin(rho), 0, math.cos(rho)] ]    
    
    myw = mat.SquareMatrix(myw) 
    
    # ZW Plane rot matrix
    mzw = [ [ 1, 0, 0, 0],
            [ 0, 1, 0, 0],
            [ 0, 0, math.cos(epsilon), -math.sin(epsilon)],
            [ 0, 0, math.sin(epsilon), math.cos(epsilon)] ]    
    
    mzw = mat.SquareMatrix(mzw)
    
    #... all the other matrixes...
    
    # multiply them
    
    mres = mxy * myz * mzx * mxw * myw * mzw
    
    mv = mat.Matrix(v.coords) # creates a 1 column matrix
    
    r =  mres * mv
    
    return vec.V4(r[0,0], r[1,0], r[2,0], r[3,0])


    
