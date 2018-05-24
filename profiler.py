# -*- coding: utf-8 -*-
"""
Created on Wed May 23 23:12:55 2018

@author: Mauro
"""

import cProfile
import main
import pstats

if __name__ == "__main__":
#    cProfile.runctx("main.main()", globals(), locals(), "./profiler_dats/test_1/profiler_stats")
    with open("./profiler_data/test_1/profiler_beautify_stats.txt", "w") as f:
        p = pstats.Stats('stats', stream=f)
        p.strip_dirs().sort_stats("cumulative").print_stats()
    