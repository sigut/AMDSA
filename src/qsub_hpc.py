# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 10:19:09 2015

@author: sigurd
"""
import os, os.path
import sys,inspect
import argparse
import re

 # realpath() will make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
    
# use this if you want to include modules from a subfolder
the_list = ["src","src/analysis","src/plotting"]
for folders in the_list:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],str(folders))))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)

import cpptraj_analysis

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--idir',help='The root input directory to perform analysis')
parser.add_argument('-p', '--protein',help='Specify the protein name in the folder. For instance \"pbpu\" ')
parser.add_argument('-q','--qsub',help='if -q qsub is specified the analysis will be submitted to the hpc-queue')
parser.add_argument('-n','--nomerge',help='if -n nomerge is specified the cpptraj will not merge the mdcrd files into the dcd file')
args = parser.parse_args()

# Variables:
home = os.getcwd() #Specify the root directory
root = args.idir
protein = args.protein
qsub = args.qsub
nomerge = args.nomerge

##qsub parameters
nodes = "1"
cores = "1"
walltime = "4"

class qsub():
    def init(self):
        self.prmtop = None
        
    def find_prmtop(self,root):
        for file in os.listdir("in_files/"):
           if file.endswith(".prmtop"):
               if not file.endswith("_nowat.prmtop"):
                   if not file.startswith("strip"):
                       if not file.startswith("closest"):
                           filename = file                            
                           self.prmtop = filename
                           print ' this is the prmtop file:'
                           print self.prmtop
    
    def cpp_qsub(self,root,qsub):
        prmtop = self.prmtop        
        # If qsub is not specified in the commandline, the cpptraj merge should be done locally.
   
        print "--- submitting the cpptraj analysis to the hpc queue"
        os.system("rm -rf cpptraj_submit.sh.*")         #Remove old output and error files
        name = "cpptraj_submit.sh"
        f = open("cpptraj_submit.sh",'w')
        f.write("#!/bin/sh\n")            
        f.write("#\n")
        f.write("# job name\n")
        f.write("#PBS -N "+name+"\n")
        f.write("# request cores\n")
        f.write("#PBS -l nodes="+nodes+":ppn="+cores+"\n")
        f.write("#clock time\n")
        f.write("#PBS -l walltime="+walltime+" \n")
        f.write("cd $PBS_O_WORKDIR\n")
        if nomerge == None:
            f.write("cpptraj -p in_files/"+prmtop+" -i in_files/trajin.traj \n")
            f.write("cpptraj -p in_files/strip."+prmtop+" -i in_files/analysis.traj \n")
            f.write("R < analysis.R --no-save")            
            f.write("python "+home+"/src/plotting/plot.py -i ./ -p "+protein+" \n")
        else:
            f.write("cpptraj -p in_files/strip."+prmtop+" -i in_files/analysis.traj \n")
            f.write("R < analysis.R --no-save")            
            f.write("python "+home+"/src/plotting/plot.py -i ./ -p "+protein+" \n")
        f.close()        
        os.system("qsub cpptraj_submit.sh")
            
def main():
    os.chdir(""+root+"")
# Define the analysis constructor    
    makeAnalysis = cpptraj_analysis.Analysis()
#Define the methods of the constructor    
    makeAnalysis.find_prmtop(root)
    makeAnalysis.makeTrajin(root,protein)
    makeAnalysis.analyse(root)

#Define the qsub constructor   
    submit = qsub()
    #Define the method of the constructor
    submit.find_prmtop(root)
    submit.cpp_qsub(root,qsub)
    
    os.chdir(""+home+"")
if __name__ == '__main__': main()