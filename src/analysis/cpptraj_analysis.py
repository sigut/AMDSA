# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/sigurd/.spyder2/.temp.py
"""
import os, os.path
import sys
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
qsub = args.qsub
nomerge = args.nomerge

##qsub parameters
nodes = "1"
cores = "1"
walltime = "4"

#Analysis parameters:
epsilon = "1.0"
sieve_hier = "100"
sieve_dbscan = "100"
#minpoints = 100

  
class Analysis:
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
       
    #Write the number of trajin lines
    def makeTrajin(self,root,protein):
        def natural_sort(l): # This is a function made to sort the mdcrd files to order them from 1,2,3...11,12,13...
            convert = lambda text: int(text) if text.isdigit() else text.lower() 
            alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
            return sorted(l, key = alphanum_key)
      
    #Find the number of mdcrd files in the MD_files folder
        mdcrd_files = []
        for file in os.listdir("md_files"):
            if file.endswith(".mdcrd"):
                if file.startswith(""+protein+"_equil"):
                    name = file
                    mdcrd_files.append(name)
        mdcrd_files = natural_sort(mdcrd_files)
        
        f = open("in_files/trajin.traj",'w')
        for names in mdcrd_files:
            f.write("trajin md_files/"+names+" 1 last 1 \n")
            f.write(' \n')
    #Cpptraj for stripping all the water
        f.write('\n')
        f.write('# Center \n')
        f.write('center origin :1 \n')
        f.write('image origin center \n')
        f.write('\n')
        f.write('# Remove all water molecules \n')
        f.write('strip :WAT,Cl-,Na+ outprefix in_files/strip \n')
        f.write('\n')
        f.write('# Create output \n')
        f.write('trajout resultsDir/mergedResult_strip.dcd charmm nobox \n')
        f.write('go')
    # Make cpptraj keep nearest water molecules  
#        f.write('\n')
#        f.write('# Keep closest 100 water molecules, remove the rest \n')
#        f.write('closest 100 :1-376 closestout in_files/closestmols.dat outprefix in_files/closest \n')
#        f.write('\n')
#        f.write('# Create output \n')
#        f.write('trajout resultsDir/mergedResult_closest.dcd charmm nobox \n')
#        f.write('go')
        f.close()
   
    def analyse(self,root):
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists("data/cluster"):
            os.makedirs("data/cluster")
            
        f = open("in_files/analysis.traj",'w')
        f.write("trajin resultsDir/mergedResult_strip.dcd 1 last 1 \n")
        f.write('rms first out data/rmsd.dat @N,CA,C time 1 \n')
        if protein == "pbpu":
            f.write("distance end_to_end1 :63@N :376@P out data/distance.dat \n")
        if protein == "pbpv":
            f.write("distance end_to_end1 :63@N :373@P out data/distance.dat \n")
        f.write("cluster hieragglo epsilon "+epsilon+" rms @CA,C,N sieve "+sieve_hier+" out data/cluster_hier_out.dat summary data/cluster_hier_summary_out.dat repout data/cluster/hier_centroid repfmt pdb \n")
        f.write("cluster dbscan minpoints 100 epsilon "+epsilon+" rms @CA,C,N sieve "+sieve_dbscan+" out data/cluster_dbscan_out.dat summary data/cluster_dbscan_summary_out.dat repout data/cluster/dbscan_centroid repfmt pdb \n")
        f.close()
           
    # If specified the calculation is submitted to the hpc queue
    def run_analysis(self,root,qsub):
        prmtop = self.prmtop        
        # If qsub is not specified in the commandline, the cpptraj merge should be done locally.
        if qsub == None:
            print 
            if nomerge == None:
                print "--- Merging the mdcrd files manually"
                os.system("cpptraj -p in_files/"+prmtop+" -i in_files/trajin.traj")
                os.system("cpptraj -p in_files/strip."+prmtop+" -i in_files/analysis.traj")
            else:
                print '--- Will not merge the mdcrd files ---'
                os.system("cpptraj -p in_files/strip."+prmtop+" -i in_files/analysis.traj")
        else:
            print "--- submitting the cpptraj analysis to the hpc queue"
#            os.system("rm -rf cpptraj_submit.sh.*")         #Remove old output and error files
#            name = "cpptraj_submit.sh"
#            f = open("cpptraj_submit.sh",'w')
#            f.write("#!/bin/sh\n")            
#            f.write("#\n")
#            f.write("# job name\n")
#            f.write("#PBS -N "+name+"\n")
#            f.write("# request cores\n")
#            f.write("#PBS -l nodes="+nodes+":ppn="+cores+"\n")
#            f.write("#clock time\n")
#            f.write("#PBS -l walltime="+walltime+" \n")
#            f.write("cd $PBS_O_WORKDIR\n")
#            if nomerge == None:
#                f.write("cpptraj -p in_files/"+prmtop+" -i in_files/trajin.traj \n")
#            f.write("cpptraj -p in_files/strip."+prmtop+" -i in_files/analysis.traj \n")
#            f.close()        
#            os.system("qsub cpptraj_submit.sh")
        

def main():
    os.chdir(""+root+"")
    # Define the constructor
    makeAnalysis = Analysis()
    #Define the methods of the constructor    
    makeAnalysis.find_prmtop(root)
    makeAnalysis.makeTrajin(root,protein)
    makeAnalysis.analyse(root)
    makeAnalysis.run_analysis(root,qsub)
    os.chdir(""+home+"")
if __name__ == '__main__': main()