# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 13:04:29 2015

@author: sigurd
"""

import argparse
import os
# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-i','--inputDir')
parser.add_argument('-p','--protein')
parser.add_argument('-q', '--inputFile')
parser.add_argument('-w','--waters')
args = parser.parse_args()

root = args.inputDir
protein = args.protein
inputFile = args.inputFile
waters = args.waters
print args

home = os.getcwd() #Specify the root directory
absdir = os.path.abspath(""+root+"")
absdir_home = os.path.abspath(""+home+"")

class pdb():
    def init(self,protein):
        if ""+protein+"" == "pbpu":
            self.res = "376"
        if ""+protein+"" == "pbpv":
            self.res = "372"
        if ""+protein+"" == None:
            print "Error - must specify protein name"
        
    def pdb_strip(self,inputFile,waters):
        f = open(""+absdir+"/"+inputFile+".traj",'w')                
        f.write("trajin "+absdir+"/"+inputFile+" \n")
        f.write(' \n')
        #Cpptraj for stripping all the water
        f.write('# Center \n')
        f.write('center origin :1 \n')
        f.write('image origin center \n')
        f.write('\n')
        f.write('# Keep closest "-w" water molecules, remove the rest \n')
        f.write('strip :Cl-,Na+ \n')
        f.write("closest "+waters+" :1-"+self.res+" closestout  outprefix "+absdir+"/closest  \n")
        f.write("outtraj closest_"+inputFile+" pdb \n")
        f.write("go \n")        
        f.write('strip :WAT,Cl-,Na+ \n')
        f.write("outtraj strip_"+inputFile+" pdb \n")
        f.write('go')           
        f.close()
    def run_pdb_strip(self,inputFile,protein):
        os.system("cpptraj -i "+absdir+"/"+inputFile+".traj -p "+protein+".prmtop")
        
        
def main():
    run_pdb = pdb()
    run_pdb.init(protein)
    run_pdb.pdb_strip(inputFile,waters)
    run_pdb.run_pdb_strip(inputFile,protein)
if __name__ == '__main__': main()