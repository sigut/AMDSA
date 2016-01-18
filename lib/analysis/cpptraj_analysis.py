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
import inspect

the_list = ["lib","lib/analysis"]
for folders in the_list:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],str(folders))))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)

from variables import *

class Analysis:
    def __init__(self):
        self.prmtop = None
        
    def find_prmtop(self,root):
        for file in os.listdir("in_files/"):
           if file.endswith(".prmtop"):
               if file.startswith(""+protein+""):
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
                elif file.startswith("equil"):
                    name = file
                    mdcrd_files.append(name)
                elif file.startswith("prod"):
                    name = file
                    mdcrd_files.append(name)
        mdcrd_files = natural_sort(mdcrd_files)
        
        f = open("in_files/trajin.traj",'w')
        f.write("trajin md_files/heat1.mdcrd 1 last 1 \n")
        f.write("trajin md_files/heat2.mdcrd 1 last 1 \n")
        for names in mdcrd_files:
            f.write("trajin md_files/"+names+" 1 last 1 \n")
            f.write(' \n')
    #Cpptraj for stripping all the water
        f.write('\n')
        f.write('# Center \n')
        f.write('center :1-321 origin \n')
        f.write('image origin center familiar \n')
        f.write('\n')
        f.write('# Remove all water molecules \n')
        f.write('strip :WAT outprefix in_files/strip \n')
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
        f.write("trajin resultsDir/"+dcdname+" 1 last 1 \n")
#        if protein == "DiaminoAzobenzeneCis" or protein == "DiaminoAzobenzeneTrans":
#            f.write("trajin resultsDir/mergedResult_strip.dcd 1 last 1 \n")
#            f.write("rms first out data/rmsd.dat @S, S1 time 1 \n")
#            f.write("distance end_to_end :1@S :1@S1 out data/distance_S_S1.dat \n")
#        else: 
        f.write('rms first out data/rmsd.dat @N,CA,C time 1 \n')
        f.write("atomicfluct out data/backbone_RMSF.apf @C,CA,N \n")
        if protein == "pbpu" or protein == "pbpv":
            f.write("distance end_to_end :10@HD22 :147@HA3 out data/distance_10_147.dat \n")
            f.write("distance end_to_end1 :10@HD22 :63@OD1 out data/distance_10_63.dat \n")
            f.write("distance end_to_end2 :115@SG :160@SG out data/distance_disulfur1.dat \n")
            f.write("distance end_to_end3 :301@SG :364@SG out data/distance_disulfur2.dat \n")
        if protein == "2ABH" or protein == "1IXH":
            f.write("distance end_to_end :226@CG :297@CG out data/distance_226_297.dat \n")
            f.write("distance end_to_endP :10@CB :322@P out data/distance_10_P.dat \n")
        if insertAnion == "on":       
            if protein == "pbpu":
                f.write("distance end_to_endpbpuP :93@CG2 :376@P out data/distance.dat \n")
            if protein == "pbpv":
                f.write("distance end_to_endpbpvP :93@CG2 :373@P out data/distance.dat \n")
        f.write("cluster hieragglo epsilon "+epsilon_hier+" rms @CA,C,N sieve "+sieve_hier+" out data/cluster_hier_out.dat summary data/cluster_hier_summary_out.dat repout data/cluster/hier_centroid repfmt pdb \n")
        f.write("cluster dbscan minpoints 100 epsilon "+epsilon_dbscan+" rms @CA,C,N sieve "+sieve_dbscan+" out data/cluster_dbscan_out.dat summary data/cluster_dbscan_summary_out.dat repout data/cluster/dbscan_centroid repfmt pdb \n")     
        if MakeMutations == "on":
            f.write("distance end_to_end :"+Mutation1+"@SG :"+Mutation2+"@SG out data/distance_"+Mutation1+"_"+Mutation2+" \n")
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