# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 14:44:36 2015

@author: sigurd
"""

# This is the master script for calling analysis and plotting functions
# It runs (4) scripts that can be chosen to be submitted to the hpc-cluster.


####-----------------------------------------------#####
# Usage: python R_analysis.py -i <inputdir> -p <protein> -n nomerge -q qsub
####-----------------------------------------------#####

import sys,inspect
import os
import argparse

# use this if you want to include modules from a subfolder
the_list = ["src","src/analysis","src/plotting"]
for folders in the_list:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],str(folders))))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
    
import qsub_hpc             # If qsub is specified the ccptraj, R and plot scripts will be submitted to the hpc-queue. 
import cpptraj_analysis     # This script runs the cpptraj module for merging mdcrd files and making the analysis on the combined dcd file. The analysis includes rmsd, distance and clustering
import R_analysis           # This script runs the "bio3d" package of "R" - which makes the principal component analysis
import plot                 # This script plots the cpptraj created data-files
from variables import *

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--idir')
parser.add_argument('-p', '--protein')
parser.add_argument('-q','--qsub')
parser.add_argument('-n','--nomerge')
args = parser.parse_args()

print args



#Usage: cpptraj.py -i <inputdir> -p <protein_name> -q qsub -n nomerge

home    = os.getcwd() #Specify the root directory
protein = args.protein
root    = args.idir
qsub    = args.qsub
nomerge = args.nomerge

#Enter the cases of the main folder and execute the script writing
def main():
    if qsub == None:
        makeAnalysis = cpptraj_analysis.main()
        print 'starting the plotting'
        RPlot = R_analysis.main()        
        makePlot = plot.main()
    else:
        submit = qsub_hpc.main()
if __name__ == '__main__': main()




