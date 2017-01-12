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

# use this if you want to include modules from a subfolder
the_list = ["lib","lib/analysis","lib/plotting","lib/setup"]
for folders in the_list:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],str(folders))))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
from variables import *

class CreateFolders():
    def __init__(self,absdir):
        # Make necessary folders
        if not os.path.exists(""+root+""):
            os.mkdir(""+absdir+"")
        if not os.path.exists(""+root+"/resultsDir"):
            os.mkdir(""+absdir+"/resultsDir")
        if not os.path.exists(""+root+"/data"):
            os.mkdir(""+absdir+"/data")
        if not os.path.exists(""+root+"/plots"):
            os.mkdir(""+absdir+"/plots")
            
    def deleteOldData(self,absdir):
        os.system("rm -rf "+absdir+"/data/*")
        os.system("rm -rf "+absdir+"/plots/*")
        



#Enter the cases of the main folder and execute the script writing
def main():
    Createfolder = CreateFolders(absdir)
#    Createfolder.create_folder(absdir)
    Createfolder.__init__(absdir)
    
                 
    if deleteOldData == "on":
        Createfolder.deleteOldData(absdir)
     # This script plots the cpptraj created data-files
    
    import qsub_hpc             # If qsub is specified the ccptraj, R and plot scripts will be submitted to the hpc-queue. 
    import cpptraj_analysis     # This script runs the cpptraj module for merging mdcrd files and making the analysis on the combined dcd file. The analysis includes rmsd, distance and clustering
    import R_analysis           # This script runs the "bio3d" package of "R" - which makes the principal component analysis
    import plot
    import CombinedPlots
    import MMPBSA_analysis
    import PCA_combined
        
        
    
    if qsub == None:
        if PCACombinedOnly == "off":
            CPPTRAJ = cpptraj_analysis.main()
            
            if R_Analysis == "on":        
                RPlot = R_analysis.main()  
                
            if MMPBSA == "on":
                mmpbsa = MMPBSA_analysis.main()
                
            if makePlots == "on":
                Plot = plot.main()
            if makeHistPlots == "on":
                HistPlot = CombinedPlots.main()
                
            if PCACombined == "on":
                PCA_combined = PCA_combined.main()
        
            else:
                submit = qsub_hpc.main()
        if PCACombinedOnly == "on":
            PCA_combined = PCA_combined.main()
if __name__ == '__main__': main()




