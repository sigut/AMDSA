# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 15:42:56 2015

@author: sigurd
"""

# This script creates the .R and .sh submission files for bio3d PCA of a given simulation.
# It can be called from its folder ./src/analysis or through the Master.py script.
# If qsub is specified, the analysis is done by the hpc system along with the other analysis methods such as cpptraj.

####-----------------------------------------------#####
# Usage: python R_analysis.py -i <inputdir> -p <protein>
####-----------------------------------------------#####
import os, os.path
import argparse
import inspect
import sys

the_list = ["src"]
for folders in the_list:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],str(folders))))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)

from variables import *


# Variables:
dcdname = "mergedResult_strip.dcd"
directory = "./src/analysis/"

class R():
#    def init(self):
#        self = None

    def write_R(self,root,protein):
        f = open(""+absdir_home+"/src/analysis/R_script.R",'w')
        f.write("## Commands \n")
        f.write("\n")
        f.write(" \n")
        f.write("# Clear all \n")    
        f.write("\n")
        f.write("rm(list=ls()) \n")    
        f.write("\n")
        f.write("# Load bio3d Library \n")    
        f.write("\n")
        f.write("library(bio3d) \n")
        f.write("\n")
        f.write("setup.ncore(8) \n")    
        f.write("\n")
        f.write("# Location of PDB files \n")    
        f.write("\n")
        f.write("id_pdb =   c(\""+absdir+"/pdb_files/"+protein+"_equil1.pdb\") \n")    
        f.write("\n")
        f.write("# Location of mdcrd files \n")    
        f.write("\n")
        f.write("folderNames =   c(\""+absdir+"/resultsDir/\") \n")    
        f.write("\n")
        f.write("# Trajectory file names \n")    
        f.write("\n")
        f.write("id_dcd =   c(\""+dcdname+"\") \n")    
        f.close()
        
        #Merge the two R files to create the file analysis.R 
        filenames = [""+absdir_home+"/src/analysis/R_script.R", ""+absdir_home+"/src/analysis/analysis_body.R",]
        with open(""+absdir+"/in_files/analysis.R", 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    outfile.write(infile.read())
    
    def write_R_sh(self,root):   
        name = "R_analysis.sh"
        f = open(""+absdir+"/"+name+"",'w')
        f.write("#!/bin/sh\n")            
        f.write("#\n")
        f.write("# job name\n")
        f.write("#PBS -N "+name+"\n")
        f.write("# request cores\n")
        f.write("#PBS -l nodes="+nodesAnalysis+":ppn="+coresAnalysis+"\n")
        f.write("#clock time\n")
        f.write("#PBS -l walltime="+walltimeAnalysis+" \n")
        f.write("cd $PBS_O_WORKDIR\n")
        f.write("# Load mpi \n")
        f.write("module load mpi/gcc-4.7.2-openmpi-1.6.3 \n")
        f.write(" \n")
        f.write("# Run R script  \n")
        f.write("R < analysis.R --no-save \n")
        f.close()
        
def main():
    # Define the constructor    
    makeR_Analysis = R()
    #Define the methods of the constructor    
    makeR_Analysis.write_R(root,protein)
    makeR_Analysis.write_R_sh(root)
    os.chdir(""+root+"")    
    os.system("R < in_files/analysis.R --no-save")
    os.chdir(""+home+"")
if __name__ == '__main__': main()