# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 13:21:14 2017

@author: sigurd
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

class PCA_combined:
    def __init__(self):
        self.folder = None
        self.newName = None 
        
    def getFolders(self,root):
        f = open("configPCA.cfg",'r')
        PCAvar = f.readlines()[1:]
        f.close()
        n = 0
        for line in PCAvar[0:]: # Find the number of folders
            if line[0:6] == "folder":
                n += 1
        self.folder = [0]*n
        self.newName = [0]*n
        # Assign each folder name to a variable
        i = 0
        for line in PCAvar[0:]:
            self.folder[i] = line[10:]
            self.folder[i] = self.folder[i].rstrip('\n') #Strip whitespace newline
            i+=1
        print self.folder
        
    def copyDCD(self,root):

        j = 0
        for name in self.folder:
            self.newName[j] = os.path.basename(os.path.normpath(""+name+""))    
            #os.system("cp "+name+"/resultsDir/"+dcdname+" "+root+"/data/"+self.newName[j]+".dcd")
            os.system("cp "+name+"/in_files/strip."+protein+".prmtop "+root+"/data/strip."+protein+".prmtop")
            j+=1
        print self.newName
        
        
        
    def cpptraj(self,root):

        f = open(""+root+"/PCA.in",'w')
        for i in range (0,len(self.folder)):
            f.write("trajin "+name+"/resultsDir/"+dcdname+" 1 100000 1 ["+self.newName[i]+"] \n")
            
        f.write("rms first @CA \n")
        f.write("createcrd combined-trajectories \n")
        f.write("average avg.pdb \n")
        f.write("run \n\n")
        f.write("\n")
        
        f.write("parm avg.pdb                                                                   \n")
        f.write("reference avg.pdb parm avg.pdb                                                 \n")
        f.write("\n")
    
        f.write("crdaction combined-trajectories rms reference @CA                              \n")
        f.write("crdaction combined-trajectories matrix covar name combined-covar @CA           \n")
        f.write("\n")
        f.write("runanalysis diagmatrix combined-covar out combined-evecs.dat vecs 3 name myEvecs \n")
        f.write("\n")
        
        for i in range(0,len(self.folder)):
            f.write("crdaction combined-trajectories projection "+self.newName[i]+" modes myEvecs out pca-"+str(i+1)+".dat beg 1 end 3 @CA crdframes "+str(1+int(i)*100000)+","+str(100001+int(i)*100000)+"\n")
        f.write("\n")
            
        for i in range(0,len(self.folder)):    
            f.write("hist "+self.newName[i]+":1 bins 200 out amd.agr norm name "+self.newName[i]+"-1 \n" )
            f.write("hist "+self.newName[i]+":2 bins 200 out amd.agr norm name "+self.newName[i]+"-2 \n" )
            f.write("hist "+self.newName[i]+":3 bins 200 out amd.agr norm name "+self.newName[i]+"-3 \n" )
            f.write("\n")

        for i in range(0,len(self.folder)):
            for j in range(0,len(self.folder)):
                if j > i:
                    f.write("kde "+self.newName[i]+":1 bins  200 kldiv "+self.newName[j]+":1 klout KLD_"+self.newName[i]+"_"+self.newName[j]+".dat \n" )
                else:
                    pass
            f.write("\n")
            
        f.write("run \n")
        
        f.write("clear all \n")
        f.write("parm strip."+protein+".prmtop \n")
        f.write("parmstrip !(@CA) \n")
        f.write("parmwrite out PCA.prmtop \n")
        f.write("runanalysis modes name Evecs trajout aMD_combined-mode1.nc pcmin -100 pcmax 100 tmode 1 trajoutmask @CA trajoutfmt netcdf \n")
        f.close()
            
        
def main():
    combinePCA = PCA_combined()
    combinePCA.getFolders(root)
    combinePCA.copyDCD(root)
    combinePCA.cpptraj(root)
if __name__ == '__main__': main()