# -*- coding: utf-8 -*-
"""
Created on Sun May 31 21:42:17 2020

@author: maurop
"""

# =============================================================================
# Imports
# =============================================================================

import time

#==============================================================================
# Rate class
#   for update rate, fps, ...
#==============================================================================

class Rate:
    '''
    Rate

    small class to manage fps and various update rates
    '''

    def __init__(self, rate):
        '''Initialize the rate calling for the time function

        Keyword argument:
        rate -- is a float representing 1/s frame rate
        '''

        self.rate = rate
        self.init_time = time.time()

    def is_time(self):
        '''Returns true if the current time surpasses the rate'''

        if time.time() - self.init_time > self.rate:
            self.init_time = time.time()
            return True
        else:
            return False