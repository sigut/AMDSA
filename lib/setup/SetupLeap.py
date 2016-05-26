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


the_list = ["lib","lib/setup"]
for folders in the_list:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],str(folders))))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)

from variables import *
from CalcIonPos import CalcIonPosition
import Crosslinker


class SetupLeap(CalcIonPosition):
    def __init__(self): 
        if insertProtein == "on":
            if MakeMutations == "on":
                self.pdbFile = ""+absdir+"/in_files/"+protein+"_mutation.pdb"
            else:
                self.pdbFile = ""+absdir_home+"/lib/setup/TemplateFiles/pdb_files/"+protein+"/"+structure+""
        
        if insertAnion == "on":
            self.inputAnion = ""+absdir_home+"/lib/setup/TemplateFiles/ion/"+ionName+".mol2"
            self.frcmodAnion = ""+absdir_home+"/lib/setup/TemplateFiles/ion/"+ionName+".frcmod"
#            self.frcmodGAFF = ""+absdir_home+"/lib/setup/TemplateFiles/ion/"+frcmod+".dat"
        
        if insertAzobenzene == "on":
            self.inputAzobenzene = ""+absdir_home+"/lib/setup/TemplateFiles/"+azoName+"/"+azoConfig+"/"+azoConfig+".mol2"
            self.frcmodAzobenzene = ""+absdir_home+"/lib/setup/TemplateFiles/"+azoName+"/"+azoConfig+"/"+azoConfig+".frcmod"
            
        self.WaterBoxSize = ""+waterboxsize+""
        # If Crosslink == on
        # protein/pdbFile is found in 
        
    def leap_sequence(self,protein):
        name = "LEaP_sequence.ff"
        f = open(""+name+"",'w')
        f.write("source "+forcefield+" \n")
        #f.write("source leaprc.gaff \n")
        f.write("loadamberparams frcmod.ionsjc_spce \n")
        f.write(" \n")
        f.write(""+protein+" = loadpdb "+self.pdbFile+" \n")
        f.write("savepdb "+protein+" "+absdir+"/in_files/"+protein+"_sequence.pdb \n")
        f.write("quit \n")
        f.close()
        # Run the tleap to create the protein        
        os.system("tleap -f "+name+"")
        
        
    def leapProtein(self,protein):
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
        if crosslink == "on":
            f.write(""+protein+" = loadpdb "+absdir+"/in_files/"+protein+"_crosslink.pdb \n")
            f.write("loadAmberParams "+absdir_home+"/lib/setup/TemplateFiles/Azobenzene/"+configuration+"/Azobenzene.frcmod \n")
        else:
            f.write(""+protein+" = loadpdb "+absdir+"/in_files/"+protein+"_sequence.pdb \n")
        if protein == "pbpu" or protein == "pbpv":
            f.write("bond "+protein+".115.SG "+protein+".160.SG \n")
            f.write("bond "+protein+".301.SG "+protein+".364.SG \n")
        if insertAnion =="on":
            f.write("loadAmberParams "+self.frcmodAnion+" \n")            
            f.write("anion = loadmol2 "+self.inputAnion+" \n")
            f.write("translate anion {"+coordinates+"} \n")
            f.write(""+protein+" = combine{"+protein+" anion} \n")
            f.write(" \n")
#            f.write(" \n")
#            f.write("addions "+protein+" Na+ 0 \n")
#            f.write("addions "+protein+" Cl- 0 \n")            
            f.write(" \n")
        if implicit == "on":
            f.write("saveamberparm "+protein+" "+absdir+"/in_files/"+protein+".prmtop "+absdir+"/in_files/"+protein+".inpcrd \n")
            f.write("\n")
            if insertAnion =="on":        
                f.write("saveamberparm "+ionName+" "+absdir+"/in_files/"+ionName+"_nowat.prmtop "+absdir+"/in_files/"+ionName+"_nowat.inpcrd \n")
            f.write(" \n")
        else:
            f.write("savepdb "+protein+" "+absdir+"/in_files/"+protein+"_finalLEAP_nowat.pdb \n")            
            f.write("saveamberparm "+protein+" "+absdir+"/in_files/"+protein+"_nowat.prmtop "+absdir+"/in_files/"+protein+"_nowat.inpcrd \n")
            f.write(" \n")
            
            #Solvate the protein
            f.write(""+solvate+" "+protein+" TIP3PBOX "+self.WaterBoxSize+" \n")
            f.write("addionsRand "+protein+" Na+ 0 \n")
            f.write("addionsRand "+protein+" Cl- 0 \n")            
            f.write(" \n")
            f.write("saveamberparm "+protein+" "+absdir+"/in_files/"+protein+".prmtop "+absdir+"/in_files/"+protein+".inpcrd \n")
            f.write("savepdb "+protein+" "+absdir+"/in_files/"+protein+"_finalLEAP.pdb \n")
        f.write("quit \n")
        f.close()
        # Run the tleap to create the protein        
        os.system("tleap -f "+name+"")
    
    def leapAnion(self):
        name = "LEaP_setupAnion.ff"
        f = open(""+name+"",'w')
        f.write("source "+forcefield+" \n")
        f.write("source leaprc.gaff \n")
        f.write("loadamberparams frcmod.ionsjc_spce \n")
        f.write(" \n")
        f.write("loadAmberParams "+self.frcmodAnion+" \n")            
        f.write(""+ionName+" = loadmol2 "+self.inputAnion+" \n")
        f.write("addions "+ionName+" Na+ 0 \n")
        f.write("addions "+ionName+" Cl- 0 \n")
        f.write("saveamberparm "+ionName+" "+absdir+"/in_files/"+ionName+"_nowat.prmtop "+absdir+"/in_files/"+ionName+"_nowat.inpcrd \n")
        f.write("savepdb "+ionName+" "+absdir+"/in_files/"+ionName+"_finalLEAP_nowater.pdb \n")
        #solvation
        f.write(""+solvate+" "+ionName+" TIP3PBOX "+self.WaterBoxSize+" \n")
        f.write("saveamberparm "+ionName+" "+absdir+"/in_files/"+ionName+".prmtop "+absdir+"/in_files/"+ionName+".inpcrd \n")
        f.write("savepdb "+ionName+" "+absdir+"/in_files/"+ionName+"_finalLEAP.pdb \n")
        f.write("quit  \n")
        f.close()
        os.system("tleap -f "+name+"")
        
    def leapAzobenzene(self):
        name = "LEaP_setupAzobenzene.ff"
        f = open(""+name+"",'w')
        f.write("source "+forcefield+" \n")
        f.write("source leaprc.gaff \n")
        f.write("loadamberparams frcmod.ionsjc_spce \n")
        f.write("loadAmberParams "+self.frcmodAzobenzene+" \n")            
        f.write(""+protein+" = loadmol3 "+self.inputAzobenzene+" \n")
        f.write("addions "+protein+" Na+ 0 \n")
        f.write("addions "+protein+" Cl- 0 \n")
        f.write("saveamberparm "+protein+" "+absdir+"/in_files/"+protein+"_nowat.prmtop "+absdir+"/in_files/"+protein+"_nowat.inpcrd \n")
        f.write("savepdb "+protein+" "+absdir+"/in_files/"+protein+"_finalLEAP_nowater.pdb \n")
        #solvation
        f.write(""+solvate+" "+protein+" TIP3PBOX "+self.WaterBoxSize+" \n")
        f.write("saveamberparm "+protein+" "+absdir+"/in_files/"+protein+".prmtop "+absdir+"/in_files/"+protein+".inpcrd \n")
        f.write("savepdb "+protein+" "+absdir+"/in_files/"+proteine+"_finalLEAP.pdb \n")
        f.write("quit  \n")
        f.close()
        os.system("tleap -f "+name+"")
       
        
def main():
    os.chdir(""+root+"")
    run_leap = SetupLeap()
        
    if insertProtein == "on":
        if crosslink == "on":
            Crosslink = Crosslinker.main() # Run the script that crosslinks the azobenzene to the protein.
            run_leap.leapProtein(protein)  
        else:
            run_leap.leap_sequence(protein)
            run_leap.leapProtein(protein)
    
    if insertProtein == "off":
        if insertAnion == "on":
            run_leap.leapAnion()
        if insertAzobenzene == "on":
            run_leap.leapAzobenzene()
            
    #Copy mol2 and frcmod file into folder 
    if insertAnion == "on":
        os.system("cp "+absdir_home+"/lib/setup/TemplateFiles/ion/"+ionName+".mol2"" "+absdir+"/in_files/"  )
        os.system("cp "+absdir_home+"/lib/setup/TemplateFiles/ion/"+ionName+".frcmod"" "+absdir+"/in_files/"  )
        
    os.chdir(""+home+"")
    print "Finished creating the prmtop, inpcrd and pdb files for the simulation"
if __name__ == '__main__': main()