# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 15:16:12 2015

@author: sigurd
"""

import os
import argparse

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--idir')
parser.add_argument('-p', '--protein')
args = parser.parse_args()


# Variables:
home = os.getcwd() #Specify the root directory
root = args.idir
protein = args.protein


name = "LEaP_setup.ff"
f = open(""+name+"",'w')
f.write("source leaprc.ff14SB \n")
f.write("source leaprc.gaff \n")
f.write("loadamberparams frcmod.ionsjc_spce \n")
f.write("pbpu_protein = loadpdb \"4F1U_cleaned.pdb\" \n")
f.write("pbpu_ion = loadmol2 4F1U_PI.mol2 \n")
f.write("pbpu = combine{pbpu_protein pbpu_ion} \n")
f.write(" \n")
f.write("pbpv_protein = loadpdb \"4F1V_cleaned.pdb\" \n")
f.write("pbpv_ion = loadmol2 4F1V_PI.mol2 \n")
f.write("pbpv = combine{pbpv_protein pbpv_ion} \n")
f.write(" \n")
f.write("hpo4 = loadmol2 4F1V_PI.mol2 \n")
f.write(" \n")
f.write("addions pbpu Na+ 0 \n")
f.write("addions pbpu Cl- 0 \n")
f.write("addions pbpv Na+ 0 \n")
f.write("addions pbpv Cl- 0 \n")
f.write("saveamberparm pbpu pbpu_nowat.prmtop pbpu_nowat.inpcrd \n")
f.write("saveamberparm pbpv pbpv_nowat.prmtop pbpv_nowat.inpcrd \n")
f.write("saveamberparm hpo4 hpo4_nowat.prmtop hpo4_nowat.inpcrd \n")
f.write(" \n")
f.write("savepdb pbpu pbpu_finalLEAP_nowater.pdb \n")
f.write("savepdb pbpv pbpv_finalLEAP_nowater.pdb \n")
f.write("savepdb hpo4 hpo4_finalLEAP_nowater.pdb \n")
f.write("solvateoct pbpu TIP3PBOX 12 \n")
f.write("solvateoct pbpv TIP3PBOX 12 \n")
f.write("solvateoct hpo4 TIP3PBOX 12 \n")
f.write(" \n")
f.write("saveamberparm pbpu pbpu.prmtop pbpu.inpcrd \n")
f.write("saveamberparm pbpv pbpv.prmtop pbpv.inpcrd \n")
f.write("saveamberparm hpo4 hpo4.prmtop hpo4.inpcrd \n")
f.write(" \n")
f.write("savepdb pbpu pbpu_finalLEAP.pdb \n")
f.write("savepdb pbpv pbpv_finalLEAP.pdb \n")
f.write("savepdb hpo4 hpo4_finalLEAP.pdb \n")
f.close()

