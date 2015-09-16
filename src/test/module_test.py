# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 11:09:46 2015

@author: sigurd
"""

import os, os.path
import sys
import argparse
import re
import numpy as np

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--idir')
args = parser.parse_args()

# Variables:
home = os.getcwd() #Specify the root directory
root = args.idir

files = "rmsd"

class test():
    def __init__(self):
        self.x = []
        self.y = []

    def read_datafile(self,root):
        os.chdir(""+root+"")
        data = open("data/rmsd.dat", "r")
        lines = data.readlines()[1:]
        data.close()
        x = []
        y = []
        for line in lines:
            p = line.split()
            x.append(float(p[0]))
            y.append(float(p[1]))
            xv = np.array(x)
            yv = np.array(y)
            self.x = xv
            self.y = yv
        os.chdir(""+home+"")
        
    def print_test(self):
        q = self.x
        w = self.y
        print 'this is the self.x value'
        print q
        print 'this is the self.x value'
        print w
        
        xtest_1 = []
        
        
def main():
    makeTest = test()
    makeTest.read_datafile(root)    
    makeTest.print_test()
if __name__ == '__main__': main()
        