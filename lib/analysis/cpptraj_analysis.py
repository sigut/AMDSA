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
        print "found"
        print len(mdcrd_files)
        print "mdcrd files"
                
        f = open("in_files/trajin.traj",'w')
        if includeHeat == "on":
            f.write("trajin md_files/heat1.mdcrd 1 last 1 \n")
            f.write("trajin md_files/heat2.mdcrd 1 last 1 \n")
        if includeEquil == "on":
            f.write("trajin md_files/equil0.mdcrd 1 last 1 \n")
        for names in mdcrd_files[1:]:
            f.write("trajin md_files/"+names+" 1 last "+interval+" \n")
            f.write(' \n')
    #Cpptraj for stripping all the water
        f.write('\n')
        f.write('# Center \n')
        f.write('center :1 origin \n')
        f.write('image origin center familiar \n')
        f.write('\n')
        f.write('# Remove all water molecules \n')
        f.write('strip :WAT outprefix in_files/strip \n')
        f.write('\n')
        f.write('# Create output \n')
        f.write("trajout resultsDir/"+dcdname+" charmm nobox \n")
        f.write('go')
        f.close()
        
        
        f = open("in_files/trajin_solvate.traj",'w')
        if includeHeat == "on":
            f.write("trajin md_files/heat1.mdcrd 1 last 1 \n")
            f.write("trajin md_files/heat2.mdcrd 1 last 1 \n")
        if includeEquil == "on":
            f.write("trajin md_files/equil0.mdcrd 1 last 1 \n")
        for names in mdcrd_files[1:]:
            f.write("trajin md_files/"+names+" 1 last "+interval+" \n")
            f.write(' \n')
    #Cpptraj for stripping all the water
        f.write('\n')
        f.write('# Center \n')
        f.write('center :1 origin \n')
        f.write('image origin center familiar \n')
        f.write('\n')
        f.write('# Create output \n')
        f.write("trajout resultsDir/"+dcdnameSolvated+" charmm nobox \n")
        f.write('go')
    # Make cpptraj keep nearest water molecules  
        f.write('\n')
        f.write('# Keep closest 100 water molecules, remove the rest \n')
        f.write('closest 100 :1-321 closestout data/closestmols.dat outprefix in_files/closest \n')
        f.write('\n')
        f.write('# Create output \n')
        f.write('trajout resultsDir/mergedResult_closest.dcd charmm nobox \n')
        f.write('go')
        f.close()
    
    def cpptrajScript(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists("data/cluster"):
            os.makedirs("data/cluster")
        if not os.path.exists("data/pca"):
            os.makedirs("data/pca")
            
        f = open("in_files/analysis.traj",'w')
        f.write("trajin resultsDir/"+dcdname+" 1 last 1 \n")
        f.write('rms first out data/rmsd.dat @N,CA,C time 1 \n')
        f.write('\n')
        if ligand == "on":
            f.write('rms first out data/rmsdPhosphate.dat @P,O1,O2,O3,H time 1 \n')
            f.write('angle OH-P-O out data/angle_OH-P-O.dat @O3 @P @O time 1  \n')
            f.write('angle O-P-O out data/angle_O-P-O.dat @O @P @O1 time 1  \n')
            f.write('angle HO-OH-P out data/angle_HO-OH-P.dat @H @O3 @P time 1  \n')
            f.write('dihedral dihedral out data/dihedral_HO-OH-P-O.dat @H @O3 @P @O1 time 1 \n')
            f.write('go \n')            
            f.write('\n')
        if clusterAnalysis == "on":
            f.write("cluster hieragglo epsilon "+epsilon_hier+" rms @CA,C,N sieve "+sieve_hier+" out data/cluster_hier_out.txt summary data/cluster_hier_summary_out.txt repout data/cluster/hier_centroid repfmt pdb \n")
            f.write("cluster dbscan minpoints 100 epsilon "+epsilon_dbscan+" rms @CA,C,N sieve "+sieve_dbscan+" out data/cluster_dbscan_out.txt summary data/cluster_dbscan_summary_out.txt repout data/cluster/dbscan_centroid repfmt pdb \n")
            f.write("go \n")
            f.write('\n')
        if AnalyseMutations == "on":
            f.write("distance end_to_endSG :"+MutationAnalysis1+"@SG :"+MutationAnalysis2+"@SG out data/distance_"+MutationAnalysis1+"_"+MutationAnalysis2+".dat \n")
            f.write('\n')
            
        if PCA == "on":
            f.write("matrix mwcovar name matrixdat @CA out data/pca/covmat-ca.dat  \n")
            f.write('\n')
            f.write("diagmatrix matrixdat out data/pca/evecs-ca.dat name data/pca/evecs-ca vecs 10 reduce \n")
#            f.write('nmwiz nmwizvecs 10 nmwizfile data/pca/nmwiz.nmd \n')            
            f.write('\n')
            f.write("analyze modes fluct out data/pca/analyzemodesfluct.dat name data/pca/evecs-ca beg 1 end 10  \n")
            f.write("analyze modes displ out data/pca/analyzemodesdispl.dat name data/pca/evecs-ca beg 1 end 10 \n")
            f.write('\n')
            f.write("go \n")
            f.write('\n')
            f.write("projection modes data/pca/evecs-ca.dat out data/pca/pca-ca.dat beg 1 end 3 @CA  \n")
            f.write('\n')
            f.write("go \n")
        
        f.close()
    
#    def analyse_azo(self):
#        if protein == "cis" or protein == "trans":
#            f = open("in_files/analysis.traj",'w')
#            f.write("trajin resultsDir/"+dcdname+" 1 last 1 \n")
#            f.write('rms first out data/rmsd.dat @S,S1 time 1 \n')
#            f.write("distance end_to_endSG :1@S :1@S1 out data/distance_S_S1.dat \n")        
#            f.close()
           
    # If specified the calculation is submitted to the hpc queue
    def run_Script(self,root,qsub):
        prmtop = self.prmtop        
        # If qsub is not specified in the commandline, the cpptraj merge should be done locally.
        if qsub == None:
            print 
            if nomerge == None:
                print "--- Merging the mdcrd files manually"
                if mergeTraj == "on":
                    print "merging the mdcrd files to a dcd file and removing the waters"
                    os.system("cpptraj -p in_files/"+prmtop+" -i in_files/trajin.traj")

                if mergeTrajSolvate == "on": #Make the solvatede dcd file
                    print "merging the mdcrd files to a solvated dcd file"
                    os.system("cpptraj -p in_files/"+prmtop+" -i in_files/trajin_solvate.traj")
            if makeAnalysis == "on":
                print "starting the cpptraj analysis"
                os.system("cpptraj -p in_files/strip."+prmtop+" -i in_files/analysis.traj")
            else:
                print '--- Will not merge the mdcrd files ---'
#                os.system("cpptraj -p in_files/strip."+prmtop+" -i in_files/analysis.traj")
        else:
            print "--- submitting the cpptraj analysis to the hpc queue"
       
        
def main():
    if not os.path.exists(""+root+"/data"):
        os.mkdir(""+root+"/data")    
    os.chdir(""+root+"")
    
    # Define the constructor
    makeAnalysis = Analysis()
    
    makeAnalysis.find_prmtop(root)
    makeAnalysis.makeTrajin(root,protein)
    makeAnalysis.cpptrajScript()
    makeAnalysis.run_Script(root,qsub)
        
    os.chdir(""+home+"")
if __name__ == '__main__': main()