# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 17:24:58 2018

@author: Mauro
"""

#==============================================================================
# Imports
#==============================================================================
import struct

#==============================================================================
# Helpers
#==============================================================================

def as_bytes(dtype, data):
    return struct.pack(dtype, data)

#==============================================================================
# Constants
#==============================================================================

# little conversion table for the supported files
type_to_size = {}
type_to_size['I'] = 4
type_to_size['d'] = 8
type_to_size['c'] = 1

#==============================================================================
# Binary file class
#==============================================================================

class BinaryFile:
    ''' reads the bytes from a file object with custom cumulative offset'''
    
    def __init__(self, fobj, co = 0):
        '''
        self.file is a file object, self.co is the cumulative offset where
        to start the procedure
        '''
        
        self.file = fobj
        self.co = co
    
    def write(self, dtype, data):
        ''' writes a data packet and moves the offset'''
        self.file.seek(self.co)
        b = as_bytes(dtype, data)
        self.file.write(b)
        self.co += len(b)
    
    def read(self, dtype):
        ''' 
        reads a data packet and moves the offset, returns the data packet
        in the specified format
        '''
        self.file.seek(self.co)
        size_read = type_to_size[dtype]
        b = self.file.read(size_read)
        self.co += size_read
        return struct.unpack(dtype, b)[0]
    
    def write_string(self, string):
        
        self.file.seek(self.co)
        
        strlen = len(string)
        
        #write str len
        self.write("I", strlen)
        
        fmt = 'c'*strlen

        data = []
        for c in string:
            data.append(bytes(c, "utf-8"))
        
        b = struct.pack(fmt, *data)
        self.file.write(b)
        self.co += len(b)
    
    def read_string(self):
        self.file.seek(self.co)
        
        # read the length
        strlen = self.read("I")
        
        b = self.file.read(strlen)
        s = str(b, "ascii")
        self.co += strlen
        return s
    
    
        
