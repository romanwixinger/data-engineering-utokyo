# -*- coding: utf-8 -*-
"""Runner for a collection of Analyses.
"""

import sys
sys.path.insert(0,'../..')  # Set src as top-level

import time


class Runner(object): 
    
    def __init__(self, analyses): 
        self.analyses = analyses
        
    def run(self, cycles: int=100, period_s: int=5): 
        last = time.time()
        start = time.time()
        for i in range(cycles):
            if time.time() < self.next_execution(start, period_s, i): 
                time.sleep(self.next_execution(start, period_s, i) - time.time())
                
            for analyses in self.analyses: 
                analyses.run()
                
            print("Time between executations:", "%.2f" % round(time.time() - last, 2), "s")
            last = time.time()
                
        return 
    
    def next_execution(self, start, period_s, i):
        return start + period_s * i
        
    
