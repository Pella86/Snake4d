# -*- coding: utf-8 -*-
"""
Created on Tue May 22 14:25:00 2018

@author: Mauro
"""

#==============================================================================
# Snake class
#==============================================================================

import vec, poly
import copy

# to do: make segment smaller in the directions orthogonal to the direction
#        this will make the snake less simmetric
#        head could be a thetra hedron or half a hypersphere on top of
#        cylinder

class Snake:
    
    def __init__(self):
        # position of the head
        self.head_pos = vec.V4(0, 0, 0, 0)
        # direction
        self.head_dir ="UP"
        #initial size
        init_size = 4
        
        # polygon list of the snake
        self.p_list = []
        
        for i in range(init_size):
            next_cube_center = self.head_pos - vec.V4( (init_size - 1) - i, 0, 0 , 0)
            next_cube = self.create_cube(next_cube_center)
            self.p_list.append(next_cube)
        
        # generate the directions vectors and forbbidden directions
        possible_dirs = ["UP", "DOWN", "LEFT", "RIGHT", "FW", "RW", "IN", "OUT"]
        
        self.dir_v = {}
        self.opposite_dir = {}
        for i, direction in enumerate(possible_dirs):
            # generate direction vectors
            v = [0, 0, 0, 0]
            v[int(i / 2)] = 1 if i % 2 == 0 else -1
            self.dir_v[direction] = vec.V4(v)
            
            # generate forbidden directions (ex. UP -> cant go DOWN)
            self.opposite_dir[direction] = possible_dirs[i + (1 if i % 2 == 0 else -1)]        
    
    # create an hypercube segment
    def create_cube(self, point):
        return poly.create_cube4d(point, 1., "green")
    
    def change_dir(self, new_dir):
        if new_dir != self.opposite_dir[self.head_dir]:
            self.head_dir = new_dir
            return True
        else:
            return False
    
    def move(self):
        # move the snake head
        self.head_pos = self.head_pos + self.dir_v[self.head_dir]
        
        # move the snake body by popping the last element and adding a
        # segment in the head 
        self.p_list.pop(0)
        self.p_list.append(self.create_cube(self.head_pos))
    
    def add_segment(self):
        # copy the last block
        last_block = copy.deepcopy(self.p_list[-1])
        # add to polygon list
        self.p_list.append(last_block)


if __name__ ==  "__main__":
    
    pass
    