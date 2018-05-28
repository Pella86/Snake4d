# -*- coding: utf-8 -*-
"""
Created on Wed May 23 23:12:55 2018

@author: Mauro
"""

import cProfile
import main
import pstats
import os


test_name = "Opt_draw_functions"
run_prof = False

test_folder = "./profiler_data/" + test_name + os.sep
if not os.path.isdir(test_folder):
    os.mkdir(test_folder)

if __name__ == "__main__":
    if run_prof:
        cProfile.runctx("main.main()", globals(), locals(), test_folder + "stats")
    else:
        with open( test_folder + "beauty_stats.txt", "w") as f:
            p = pstats.Stats(test_folder + 'stats', stream=f)
            p.strip_dirs().sort_stats("cumulative").print_stats()
        