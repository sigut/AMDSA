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
import sys,inspect
import argparse
import re

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--idir')
parser.add_argument('-p', '--protein')
parser.add_argument('-q','--qsub')
parser.add_argument('-n','--nomerge')
args = parser.parse_args()


# Variables:
home = os.getcwd() #Specify the root directory
root = args.idir
protein = args.protein

absdir = os.path.abspath(""+root+"")

dcdname = "mergedResult_strip.dcd"
directory = "./src/analysis/"

#qsub parameters
nodes = "1"
cores = "1"
walltime = "4"



class R():
#    def init(self):
#        self = None

    def write_R(self,root,protein):
        f = open(""+directory+"R_script.R",'w')
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
        filenames = [""+directory+"R_script.R", ""+directory+"analysis_body.R",]
        with open(""+root+"in_files/analysis.R", 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    outfile.write(infile.read())
    
    def write_R_sh(self,root):   
        name = "R_analysis.sh"
        f = open(""+root+""+name+"",'w')
        f.write("#!/bin/sh\n")            
        f.write("#\n")
        f.write("# job name\n")
        f.write("#PBS -N "+name+"\n")
        f.write("# request cores\n")
        f.write("#PBS -l nodes="+nodes+":ppn="+cores+"\n")
        f.write("#clock time\n")
        f.write("#PBS -l walltime="+walltime+" \n")
        f.write("cd $PBS_O_WORKDIR\n")
        f.write("# Load mpi \n")
        f.write("module load mpi/gcc-4.7.2-openmpi-1.6.3 \n")
        f.write("module load python \n")
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