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
from CalcIonPos import CalcIonPosition


class SetupLeap(CalcIonPosition):
    def init(self,CalcIonPosition): 
        self.inputCrystalStructure = ""+absdir_home+"/src/setup/TemplateFiles/pdb_files/"+protein+"/"+structure+""
        self.inputAnion = ""+absdir_home+"/src/setup/TemplateFiles/ion/"+ionName+".mol2"
        self.WaterBoxSize = ""+waterboxsize+""
#        self.coordinates = str("")
        
        
                
        
    def leap_sequence(self,protein):
        name = "LEaP_sequence.ff"
        f = open(""+name+"",'w')
        f.write("source "+forcefield+" \n")
        f.write("source leaprc.gaff \n")
        f.write("loadamberparams frcmod.ionsjc_spce \n")
        f.write(" \n")
        f.write(""+protein+" = loadpdb "+self.inputCrystalStructure+" \n")
        f.write("savepdb "+protein+" "+absdir+"/in_files/"+protein+"_sequence.pdb \n")
        f.write("quit \n")
        f.close()
        # Run the tleap to create the protein        
        os.system("tleap -f "+name+"")
        
        
    def leap_CYX(self,protein,CalcIonPosition):
        if insertAnion == "on":
            f = open(""+absdir+"/in_files/coordinates.dat",'r')
            coordinates = f.readlines()[0]
            f.close()
        name = "LEaP_setup.ff"
        f = open(""+name+"",'w')
        f.write("source "+forcefield+" \n")
        f.write("source leaprc.gaff \n")
        f.write("loadamberparams frcmod.ionsjc_spce \n")
        f.write(" \n")
        f.write(""+protein+" = loadpdb "+absdir+"/in_files/"+protein+"_sequence.pdb \n")
        f.write("bond "+protein+".115.SG "+protein+".160.SG \n")
        f.write("bond "+protein+".301.SG "+protein+".364.SG \n")
        if insertAnion =="on":
            f.write("anion = loadmol2 "+self.inputAnion+" \n")
            f.write("translate anion {"+coordinates+"} \n")
            f.write(""+protein+" = combine{"+protein+" anion} \n")
            f.write(" \n")
            f.write(""+ionName+" = loadmol2 "+self.inputAnion+" \n")
            f.write(" \n")
            f.write("addions "+protein+" Na+ 0 \n")
            f.write("addions "+protein+" Cl- 0 \n")            
            f.write("addions "+ionName+" Na+ 0 \n")
            f.write("addions "+ionName+" Cl- 0 \n")
            f.write(" \n")
        if implicit == "on":
            f.write("saveamberparm "+protein+" "+absdir+"/in_files/"+protein+".prmtop "+absdir+"/in_files/"+protein+".inpcrd \n")
            if insertAnion =="on":        
                f.write("saveamberparm "+ionName+" "+absdir+"/in_files/"+ionName+"_nowat.prmtop "+absdir+"/in_files/"+ionName+"_nowat.inpcrd \n")
            f.write(" \n")
            f.write("savepdb "+protein+" "+absdir+"/in_files/"+protein+"_finalLEAP_nowater.pdb \n")
            if insertAnion =="on":
                f.write("savepdb "+ionName+" "+absdir+"/in_files/"+ionName+"_finalLEAP_nowater.pdb \n")
            f.write("\n")
        else:
            f.write("saveamberparm "+protein+" "+absdir+"/in_files/"+protein+"_nowat.prmtop "+absdir+"/in_files/"+protein+"_nowat.inpcrd \n")
            if insertAnion =="on":        
                f.write("saveamberparm "+ionName+" "+absdir+"/in_files/"+ionName+"_nowat.prmtop "+absdir+"/in_files/"+ionName+"_nowat.inpcrd \n")
            f.write(" \n")
            f.write("savepdb "+protein+" "+absdir+"/in_files/"+protein+"_finalLEAP_nowater.pdb \n")
            if insertAnion =="on":
                f.write("savepdb "+ionName+" "+absdir+"/in_files/"+ionName+"_finalLEAP_nowater.pdb \n")
            f.write("\n")
            #Solvate the protein
            f.write(""+solvate+" "+protein+" TIP3PBOX "+self.WaterBoxSize+" \n")
            if insertAnion =="on":
                f.write(""+solvate+" "+ionName+" TIP3PBOX "+self.WaterBoxSize+" \n")
            f.write(" \n")
            f.write("saveamberparm "+protein+" "+absdir+"/in_files/"+protein+".prmtop "+absdir+"/in_files/"+protein+".inpcrd \n")
            if insertAnion =="on":
                f.write("saveamberparm "+ionName+" "+absdir+"/in_files/"+ionName+".prmtop "+absdir+"/in_files/"+ionName+".inpcrd \n")
            f.write(" \n")
            f.write("savepdb "+protein+" "+absdir+"/in_files/"+protein+"_finalLEAP.pdb \n")
            if insertAnion =="on":  
                f.write("savepdb "+ionName+" "+absdir+"/in_files/"+ionName+"_finalLEAP.pdb \n")
        f.write("quit \n")
        f.close()
        # Run the tleap to create the protein        
        os.system("tleap -f "+name+"")
            
       
        
def main():
    os.chdir(""+root+"")
    run_leap = SetupLeap()
    run_leap.init(CalcIonPosition)
    #    run_leap.init(ion)
#    if insertAnion == "on":
#        CalcIonPos.main()
    
    run_leap.leap_sequence(protein)
    run_leap.leap_CYX(protein,CalcIonPosition)
    os.chdir(""+home+"")
if __name__ == '__main__': main()