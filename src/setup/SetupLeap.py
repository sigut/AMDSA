# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 15:16:12 2015

@author: sigurd
"""
# This script creates the prmtop, inpcrd and pdb files of the simulations - eg. it puts the protein and ion together where the position of the anion is specified in the methods below.
# If the config.cfg file has an empty string for the anion, the system will setup an isolated protein.
import os
import numpy as np
import sys,inspect
import math

the_list = ["src","src/setup"]
for folders in the_list:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],str(folders))))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)

from variables import *
import CalcIonPos
from CalcIonPos import CalcIonPosition


class SetupLeap(CalcIonPosition):
    def init(self,CalcIonPosition): 
        self.inputCrystalStructure = ""+absdir_home+"/src/setup/TemplateFiles/pdb_files/"+protein+"/"+structure+""
        self.inputAnion = ""+absdir_home+"/src/setup/TemplateFiles/ion/HPO4.mol2"
        self.WaterBoxSize = ""+waterboxsize+""
#        self.coordinates = str("")
        
        
                
        
    def leap(self,protein,CalcIonPosition):
        if insertAnion == "HPO4":
            f = open(""+absdir+"/in_files/coordinates.dat",'r')
            coordinates = f.readlines()[0]
            f.close()
        name = "LEaP_setup.ff"
        f = open(""+name+"",'w')
        f.write("source leaprc.ff14SB \n")
        f.write("source leaprc.gaff \n")
        f.write("loadamberparams frcmod.ionsjc_spce \n")
        f.write(" \n")
        f.write(""+protein+" = loadpdb "+self.inputCrystalStructure+" \n")
        if insertAnion =="HPO4":
            f.write("anion = loadmol2 "+self.inputAnion+" \n")
            f.write("translate anion {"+coordinates+"} \n")
            f.write(""+protein+" = combine{"+protein+" anion} \n")
            f.write(" \n")
            f.write("HPO4 = loadmol2 "+self.inputAnion+" \n")
        f.write(" \n")
        f.write("addions "+protein+" Na+ 0 \n")
        f.write("addions "+protein+" Cl- 0 \n")
        f.write(" \n")
        if implicit == "on":
            f.write("saveamberparm "+protein+" "+absdir+"/in_files/"+protein+".prmtop "+absdir+"/in_files/"+protein+".inpcrd \n")
            if insertAnion =="HPO4":        
                f.write("saveamberparm HPO4 "+absdir+"/in_files/HPO4_nowat.prmtop "+absdir+"/in_files/HPO4_nowat.inpcrd \n")
            f.write(" \n")
            f.write("savepdb "+protein+" "+absdir+"/in_files/"+protein+"_finalLEAP_nowater.pdb \n")
            if insertAnion =="HPO4":
                f.write("savepdb HPO4 "+absdir+"/in_files/HPO4_finalLEAP_nowater.pdb \n")
            f.write("\n")
        else:
            f.write("saveamberparm "+protein+" "+absdir+"/in_files/"+protein+"_nowat.prmtop "+absdir+"/in_files/"+protein+"_nowat.inpcrd \n")
            if insertAnion =="HPO4":        
                f.write("saveamberparm HPO4 "+absdir+"/in_files/HPO4_nowat.prmtop "+absdir+"/in_files/HPO4_nowat.inpcrd \n")
            f.write(" \n")
            f.write("savepdb "+protein+" "+absdir+"/in_files/"+protein+"_finalLEAP_nowater.pdb \n")
            if insertAnion =="HPO4":
                f.write("savepdb HPO4 "+absdir+"/in_files/HPO4_finalLEAP_nowater.pdb \n")
            f.write("\n")
            #Solvate the protein
            f.write("solvateoct "+protein+" TIP3PBOX "+self.WaterBoxSize+" \n")
            if insertAnion =="HPO4":
                f.write("solvateoct HPO4 TIP3PBOX "+self.WaterBoxSize+" \n")
            f.write(" \n")
            f.write("saveamberparm "+protein+" "+absdir+"/in_files/"+protein+".prmtop "+absdir+"/in_files/"+protein+".inpcrd \n")
            if insertAnion =="HPO4":
                f.write("saveamberparm HPO4 "+absdir+"/in_files/HPO4.prmtop "+absdir+"/in_files/HPO4.inpcrd \n")
            f.write(" \n")
            f.write("savepdb "+protein+" "+absdir+"/in_files/"+protein+"_finalLEAP.pdb \n")
            if insertAnion =="HPO4":  
                f.write("savepdb HPO4 "+absdir+"/in_files/HPO4_finalLEAP.pdb \n")
        f.write("quit \n")
        f.close()
        # Run the tleap to create the protein        
        os.system("tleap -f "+name+"")
       
        
def main():
    os.chdir(""+root+"")
    run_leap = SetupLeap()
    run_leap.init(CalcIonPosition)
    #    run_leap.init(ion)
    if insertAnion == "HPO4":
        CalcIonPos.main()
#        coordinates = CalcIonPos.main()
#        print "Will place the anion in the binding site"
#        CalcIonPos.main()
#        run_leap.FindCoordinates(protein)
    
    run_leap.leap(protein,CalcIonPosition)
    os.chdir(""+home+"")
if __name__ == '__main__': main()