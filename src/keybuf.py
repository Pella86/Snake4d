# -*- coding: utf-8 -*-
"""
Created on Sun May 31 21:40:41 2020

@author: maurop
"""


#==============================================================================
# Key buffer
#==============================================================================

class KeyBuffer:
    '''
    Key Buffer

    is a simple buffer that keeps track of the key pressed while playing
    it makes a more fluid control of the snake when the game lags.

    Methods:
        __init__
        push_key
        get_key
        clear

    Instance variables:
        self.buf -- a simple list doing the job of a LIFO stack
        self.key_to_dir -- transforms the key in directions
    '''

    def __init__(self):
        '''
        class is initialised with a buffer, and a dictionary that will
        convert the keys to directions
        '''

        self.buf = []

        # construct the dictionary that changes the snake direction
        self.key_to_dir = {}
        bind_key = ["w", "s", "a", "d", "i", "k", "j", "l"]
        possible_dirs = ["UP", "DOWN", "LEFT", "RIGHT", "FW", "RW", "IN", "OUT"]

        for direction, key in zip(possible_dirs, bind_key):
            self.key_to_dir[key] = direction

    def push_key(self, key):
        '''
        insert the key in the buffer

        Keyword arguments:
        key -- can be any character
        '''

        self.buf.append(key)

    def get_key(self):
        '''gets the next key, if none is found returns None'''

        if self.buf:
            return self.key_to_dir[self.buf.pop(0)]
        else:
            return None

    def clear(self):
        '''Just empties the buffer'''

        self.buf = []