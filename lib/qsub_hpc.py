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
the_list = ["lib","lib/analysis","lib/plotting"]
for folders in the_list:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],str(folders))))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
        
from variables import *
import cpptraj_analysis, R_analysis, plot


class qsub():
    def init(self):
        self.prmtop = None
        self.complex_solvated   = "in_files/"+protein+".prmtop"
        self.complex_nowat      = "in_files/"+protein+"_nowat.prmtop"
        self.dcdname_solvated   = "resultsDir/"+dcdnameSolvated+""
        
        self.receptor_solvated  = ""+absdir_home+"/CUDA_Simulations/1IXH_aMD_1/in_files/1IXH.prmtop"        
        self.receptor_nowat     = ""+absdir_home+"/CUDA_Simulations/1IXH_aMD_1/in_files/1IXH_nowat.prmtop"
        self.receptor_dcd       = ""+absdir_home+"/CUDA_Simulations/1IXH_aMD_1/resultsDir/mergedResult_solvated.dcd"
        
        self.ligand_solvated    = ""+absdir_home+"/Phosphate_Simulations/HPO4_QM/in_files/HPO4.prmtop"
        self.ligand_nowat       = ""+absdir_home+"/Phosphate_Simulations/HPO4_QM/in_files/HPO4_nowat.prmtop"
        self.ligand_dcd         = ""+absdir_home+"/Phosphate_Simulations/HPO4_QM/resultsDir/mergedResult_solvated.dcd"
        
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
        f.write("#PBS -l nodes="+nodesAnalysis+":ppn="+coresAnalysis+"\n")
        f.write("#clock time\n")
        f.write("#PBS -l walltime="+walltimeAnalysis+" \n")
        f.write("cd $PBS_O_WORKDIR\n")
        if nomerge == None :
            if mergeTraj == "on":
                f.write("cpptraj -p in_files/"+prmtop+" -i in_files/trajin.traj \n")
            if mergeTrajSolvate == "on":
                f.write("cpptraj -p in_files/"+prmtop+" -i in_files/trajin_solvate.traj \n")
        if makeAnalysis == "on":    
            f.write("cpptraj -p in_files/strip."+prmtop+" -i in_files/analysis.traj \n")
        if R_Analysis == "on":
            f.write("R < in_files/analysis.R --no-save \n")            
        if MMPBSA == "on":
            f.write("$AMBERHOME/bin/MMPBSA.py -O -i in_files/mmpbsa.in -o data/MMPBSA.dat -sp "+self.complex_solvated+" -cp "+self.complex_nowat+" -y "+self.dcdname_solvated+" -rp "+self.receptor_nowat+"  -srp "+self.receptor_solvated+" -yr "+self.receptor_dcd+" -lp "+self.ligand_nowat+" -slp "+self.ligand_solvated+" -yl "+self.ligand_dcd+"  -eo data/MMPBSA.csv \n")
        if makePlots == "on":
            f.write("python "+home+"/lib/plotting/plot.py -i ./ -p "+protein+" \n")
        if makeHistPlots == "on":
            f.write("python "+home+"/lib/plotting/CombinedPlots.py -i "+absdir+" -p "+protein+" -m1 "+Mutation1+" -m2 "-+Mutation2+"  \n")
            
        f.close()        
        os.system("qsub cpptraj_submit.sh")
            
def main():
    os.chdir(""+root+"")
# Define the analysis constructor for cpptraj
    makeAnalysis = cpptraj_analysis.Analysis()
#Define the methods of the constructor    
    makeAnalysis.find_prmtop(root)
    makeAnalysis.makeTrajin(root,protein)
    if protein == "cis" or protein =="trans":
        makeAnalysis.analyse_azo()
    else:
        makeAnalysis.analyse()
# Define the analysis constructor for "R"
    if R_Analysis == "on":
        makeR_Analysis = R_analysis.R()
        #Define the methods of the constructor
        makeR_Analysis.write_R(root,protein)
        makeR_Analysis.write_R_sh(root)

    if MMPBSA == "on":
        mmpbsaAnalysis = MMPBSA_analysis()
        mmpbsaAnalysis.mmpbsa(root)
        mmpbsaAnalysis.qsubMMPBSA(root,protein)
    
#Define the qsub constructor   
    submit = qsub()
#Define the method of the constructor
    submit.find_prmtop(root)
    submit.cpp_qsub(root,qsub)
    
    os.chdir(""+home+"")
if __name__ == '__main__': main()