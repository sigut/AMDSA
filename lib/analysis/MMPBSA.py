# -*- coding: utf-8 -*-
"""
Created on Wed Nov 19 13:55:10 2014

@author: sigurd
"""
import os, os.path
import sys
import argparse
import inspect

the_list = ["lib","lib/analysis"]
for folders in the_list:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],str(folders))))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)

from variables import *

class MMPBSA():
    def __init__(self): #Relative from inputdir
        self.complex_solvated   = "in_files/"+protein+".prmtop"
        self.complex_nowat      = "in_files/"+protein+"_nowat.prmtop"
        self.dcdname_solvated   = "resultsDir/"+dcdnameSolvated+""
        
        self.receptor_solvated  = ""+absdir_home+"/CUDA_Simulations/1IXH_aMD_1/in_files/1IXH.prmtop"        
        self.receptor_nowat     = ""+absdir_home+"/CUDA_Simulations/1IXH_aMD_1/in_files/1IXH_nowat.prmtop"
        self.receptor_dcd       = ""+absdir_home+"/CUDA_Simulations/1IXH_aMD_1/resultsDir/mergedResult_solvated.dcd"
        
        self.ligand_solvated    = ""+absdir_home+"/Phosphate_Simulations/HPO4_QM/in_files/HPO4.prmtop"
        self.ligand_nowat       = ""+absdir_home+"/Phosphate_Simulations/HPO4_QM/in_files/HPO4_nowat.prmtop"
        self.ligand_dcd         = ""+absdir_home+"/Phosphate_Simulations/HPO4_QM/resultsDir/mergedResult_solvated.dcd"
        
        
        
	
    def mmpbsa(self):
        name_inputfile = "in_files/mmpbsa.in"  # Name of text file coerced with +.sh
        print("Creating new sh file: "+name_inputfile+"")             
        f = open(name_inputfile,'w')   # Trying to create a new file or open one
        f.write("#Input file for running PB and GB \n")            
        f.write("#\n")
        f.write("&general\n")
        f.write("   interval = "+intervalMMPBSA+", \n") #Do not change the syntax of '=' signs - the plotting scripts depend on this.
        f.write("   keep_files = 0, \n")
        f.write("   receptor_mask = :1-6 \n")
        f.write("   entropy = 1, \n")
        f.write("/ \n")
        f.write("&gb \n")
        f.write("   igb = 5,\n")
        f.write("   ifqnt = 1,\n")
        f.write("   qmcharge_com = "+qmcharge_complex+",\n")
        f.write("   qmcharge_rec = "+qmcharge_protein+", \n")
        f.write("   qmcharge_lig = "+qmcharge_ion+", \n")
        f.write("   qm_residues = "+qm_residues+", \n")
        f.write("   qm_theory = 'PM6-D',\n")
        f.write(" / ")
        f.close()
    
#    def removeOldFiles(self):
#        #Use ante-MMPBSA to create the neccesary prmtop files and subsequently running the MMPBSA.py script
#                
#        
#        print("Creating new sh file: "+name+"")             
#        
#        os.system("rm -rf "+name+".*")
##        os.system("rm -rf ligand.prmtop receptor.prmtop complex.prmtop")
#        os.system("rm -rf _MMPBSA* ")
#        os.system("rm -rf MMPBSA_MTP.dat MMPBSA_Energy_MTP.dat")
#        
#        os.system("$AMBERHOME/bin/ante-MMPBSA.py -p peptide.prmtop -c complex.prmtop -r receptor.prmtop -l ligand.prmtop -m :1-6 -s :WAT")
    def qsubMMPBSA(self):
        name = "MMPBSA.sh"  # Name of text file coerced with +.sh
        f = open(name,'w')   # Trying to create a new file or open one
        f.write("#!/bin/sh\n")            
        f.write("#\n")
        f.write("# job name\n")
        f.write("#PBS -N "+name+"\n")
        f.write("# request cores\n")
        f.write("#PBS -l nodes="+cores+":ppn="+nodes+"\n")
        f.write("#clock time\n")	
        f.write("#PBS -l walltime="+walltime+"\n")
        f.write("cd $PBS_O_WORKDIR\n")
        f.write("$AMBERHOME/bin/MMPBSA.py -O -i in_files/mmpbsa.in -o data/MMPBSA.dat -sp "+self.complex_solvated+" -cp "+self.complex_nowat+" -y /"+self.dcdname_solvated+" -rp "+self.receptor_nowat+"  -srp "+self.receptor_solvated+" -yr "+self.receptor_dcd+" -lp "+self.ligand_nowat+" -slp "+self.ligand_solvated+" -yl "+self.ligand_dcd+"  -eo data/MMPBSA.csv \n")
#        f.write("$AMBERHOME/bin/MMPBSA.py -O -i in_files/mmpbsa_STP.in -o data/MMPBSA/MMPBSA_STP.dat -sp "+self.complex_solvated+" -cp "+self.complex_nowat+" -rp "+self.receptor_nowat+" -lp "+self.ligand_nowat+" -y /"+dcdnameSolvated+" -srp "+self.receptor_solvated+" -yr "+self.receptor_dcd+" -eo data/MMPBSA_Energy_MTP.csv \n")
        f.close()
        #Submitting the script to the server
#        os.system("qsub "+name+"")
        
        
def main():
    if not os.path.exists(""+root+"/data"):
        os.mkdir(""+root+"/data")    
    os.chdir(""+root+"")
    
    # Define the constructor
    mmpbsaAnalysis = MMPBSA()
    #Define the methods of the constructor    
    mmpbsaAnalysis.mmpbsa(root)
    mmpbsaAnalysis.qsubMMPBSA(root,protein)
    

    os.chdir(""+home+"")
if __name__ == '__main__': main()
