# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 10:47:28 2016

@author: sigurd
"""
import os,sys,inspect

the_list = ["lib","lib/setup"]
for folders in the_list:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],str(folders))))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
        
from variables import *

class MakeMutations():
    def __init__(self): 
        self.pdbFile = ""+absdir_home+"/lib/setup/TemplateFiles/pdb_files/"+protein+"/"+structure+""
        self.x,self.y,self.z = [],[],[]
        self.data = []
        self.atomnumber = []
        self.atomname   = []
        self.residuename= []
        self.residuenumber= []
        self.list = [Mutation1, Mutation2]
        self.Mutationlines1 = []
        self.Mutationlines2 = []
        self.MutationNames1 = []
        self.MutationNames2 = []
        self.Mutationlines = []
        
    def ReadProteinCoordinates(self): # Read the coordinates of the protein pdb file
        f = open(self.pdbFile,'r')
        pdb = f.readlines()[0:]
        f.close()

        n = 0
        for line in pdb[0:]: # Start coordinate handling when the atoms start
            if line[0:4] == "ATOM":
                break
            n+=1
        print "this is the n value"
        print n
        k = 0
        
        for line in pdb[n:]:
            k +=1            
            coor = line.split()
            if line[0:3] == "TER": # Stop reading if the pdb contains a new molecule
                break
            if line [0:3] == "END": #Breakout if file ends
                break
            if str(coor[3]) == "WAT": # Stop reading if the pdb contains water
                break
            if line[0:4] == 'ATOM':
               
                try: # If the pdb-file contains the residue number on column 4 then append, otherwise an error will occur and the script will enter the exception and write column 5 instead.
                    if isinstance(int(coor[4]),int) == True: 
#                        for i in self.list: # Append the coordinates of the binding residues.
                        if int(coor[4]) == int(Mutation1):
                            self.Mutationlines1.append(k+n)
                            self.MutationNames1.append(coor[3])
                        if int(coor[4]) == int(Mutation2):
                            self.Mutationlines2.append(k+n)
                            self.MutationNames2.append(coor[3])
                                
                except ValueError:
#                    for i in self.list: # Append the coordinates of the binding residues.
                        if int(coor[5]) == int(Mutation1):
                            self.Mutationlines1.append(k+n)
                            self.MutationNames1.append(coor[3])
                            self.Mutationlines.append(k+n)
                        if int(coor[5]) == int(Mutation2):
                            self.Mutationlines2.append(k+n)
                            self.MutationNames2.append(coor[3])
                            self.Mutationlines.append(k+n)
                            
                        
            
        print self.Mutationlines1, self.MutationNames1
        print self.Mutationlines2, self.MutationNames2
        l = 0
        with open(""+absdir+"/in_files/"+protein+"_mutation.pdb",'w') as new_file:
            with open(self.pdbFile) as old_file:
                for line in old_file:
                    line1 = line.split()
                    l += 1                   
                    if l == self.Mutationlines1[0]:
                        new_file.write(line.replace(line1[3], "CYX"))
                        
                    if l == self.Mutationlines2[0]:
                        new_file.write(line.replace(line1[3], "CYX"))
                    
                    if l not in self.Mutationlines:
                        new_file.write(line)                                     
                        
    def Note(self):
        f = open(""+root+"/README_"+Mutation1+"_"+Mutation2+".txt",'w')
        f.write("This folder contains files for simulations of the initial crystalstructure of "+structure+", with mutations on residues "+Mutation1+" and "+Mutation2+" ")
        f.close()

def main():
    Mutations = MakeMutations()        
    Mutations.ReadProteinCoordinates()
    Mutations.Note()    
                    
if __name__ == '__main__': main()
            