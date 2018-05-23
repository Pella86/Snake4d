# -*- coding: utf-8 -*-
"""
Created on Fri May 18 20:44:22 2018

@author: Mauro
"""

# m rows, n columns

class MatExcept(Exception):
    pass

class Matrix:
    
    def __init__(self, m, n = None):
        self.mat = []
        if type(m) == list and type(m[0]) is list and n is None:
            self.m = len(m)
            self.n = len(m[0])
            self.init_mat()
            
            for i in range(self.m):
                for j in range(self.n):
                    self[i, j] = m[i][j]
        
        elif type(m) is list:
            self.m = len(m)
            self.n = 1
            
            self.init_mat()
            
            for i in range(self.m):
                self[i, 0] = m[i]

        else:
            self.m = m
            self.n = n
            self.init_mat()
            

    
    def init_mat(self):
        for i in range(self.m):
            for j in range(self.n):
                self.mat.append(0)        
    
    
    def __getitem__(self, idx):
        linear_index = idx[1] * self.m + idx[0]      
        return self.mat[linear_index]
    
    def __setitem__(self, idx, c):
        if idx[0] >= self.m or idx[0] < 0: raise MatExcept("Matrix: row out of range")
        if idx[1] >= self.n or idx[1] < 0: raise MatExcept("Matrix: row out of range")        
        
        linear_index = idx[1] * self.m + idx[0]
        self.mat[linear_index] = c
        
    def __add__(self, m2):
        if self.m == m2.m and self.n == m2.n:
            new_mat = []
            for i in range(len(self.mat)):
                new_mat.append(self.mat[i] + m2.mat[i])
            
            mnew = Matrix(self.m, self.n)
            mnew.mat = new_mat
            return mnew
            
        else:
            raise MatExcept("Matrix: addition not same size")

    def __sub__(self, m2):
        if self.m == m2.m and self.n == m2.n:
            new_mat = []
            for i in range(len(self.mat)):
                new_mat.append(self.mat[i] - m2.mat[i])
            
            mnew = Matrix(self.m, self.n)
            mnew.mat = new_mat
            return mnew
            
        else:
            raise MatExcept("Matrix: subtraction not same size") 
    
    def __mul__(self, m2):
        if self.n == m2.m:
            mulmat = Matrix(self.m, m2.n)
            for i in range(mulmat.m):
                for j in range(mulmat.n):
                    for m in range(self.n):
                        mulmat[i, j] += self[i, m] * m2[m, j]
            return mulmat
                    
        else:
            raise MatExcept("Matrix: multiplication columns diff then rows")
    
    def scalar(self, k):
        mat_new = []
        for m in self.mat:
            mat_new.append(m * k)
        
        mres = Matrix(self.m, self.n)
        mres.mat = mat_new
        
        return mres
    
    def transpose(self):
        tmat = Matrix(self.n, self.m)
        
        for i in range(self.m):
            for j in range(self.n):
                tmat[j, i] = self[i, j]
        return tmat
            
    
    def __str__(self):
        s = ""
        for i in range(self.m):
            for j in range(self.n):
                
                s += str(self[i, j]) + " "
            s += "\n"
        
        return s


class SquareMatrix(Matrix):
    
    def __init__(self, m):
        if type(m) is list:
            if len(m) != len(m[0]): raise MatExcept("SqMat: Not a square matrix")
            super().__init__(m)
        else:
            super().__init__(m, m)
    
    def is_diagonal(self):
        for i in range(self.m):
            for j in range(self.n):
                if i == j and self[i, j] == 0:
                    return False
                
                if i != j and self[i, j] != 0:
                    return False
        return True
    
    def is_lower_triangular(self):
        for i in range(self.m):
            for j in range(self.n):
                if j <= i and self[i, j] == 0:
                    return False
                
                if j > i and self[i, j] != 0:
                    return False
        return True
        
    def is_upper_triangular(self):
        for i in range(self.m):
            for j in range(self.n):
                if i <= j and self[i, j] == 0:
                    return False
                
                if i > j and self[i, j] != 0:
                    return False
        return True
    
    def get_identity(self):
        
        imatrix = SquareMatrix(self.m)
        for i in range(self.m):
            imatrix[i, i] = 1
            
        return imatrix

if __name__ == "__main__":
    m = Matrix(2, 3)
    print(m)
    
    m[1, 2] = 1
    
    print(m)
    
    m2 = Matrix(2, 3)
    m2[1, 2] = 3
    
    print(m2)
    print(m2.transpose())
    
    print(m + m2.scalar(4))
    
    print("--- mul ----")
    
    m1 = Matrix(2, 3)
    m1[0, 0] = 2
    m1[0, 1] = 3
    m1[0, 2] = 4
    m1[1, 0] = 1
    
    print(m1)
    
    m2 = Matrix(3, 2)
    m2[0, 1] = 1000
    m2[1, 0] = 1
    m2[1, 1] = 100
    m2[2, 1] = 10
    print(m2)
    
    print(m1 * m2)
    
    m1 = [ [1, 2],
           [3, 4] ]
    m2 = [ [0, 1],
           [0, 0] ]
    m1 = Matrix(m1)
    m2 = Matrix(m2)
    mres = m1 * m2
    print(mres)
    mres = m2 * m1
    print(mres)
    
    print ("--- list init ---")
    
    m = [ [2, 3, 4],
          [1, 0, 0] ]
    
    mini = Matrix(m)
    print(mini)
    
    print("--- sq matrix ---")
    
    m = [ [1, 1, 1],
          [0, 1, 1],
          [0, 0, 1] ]
    
    m = SquareMatrix(m)
    
    print(m)
    print(m.is_diagonal())
    print(m.is_lower_triangular())    
    print(m.is_upper_triangular()) 

    print(m.get_identity())    
    
    
    
    
    
    