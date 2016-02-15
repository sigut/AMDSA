# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 14:41:40 2016

@author: sigurd
"""
import os
import numpy as np
import sys,inspect


the_list = ["lib","lib/setup"]
for folders in the_list:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],str(folders))))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)

from variables import *

class Crosslinker():
    def __init__(self):
        self.pdbFile = ""+absdir_home+"/lib/setup/TemplateFiles/pdb_files/"+protein+"/"+structure+""
        self.azoFile = ""+absdir_home+"/lib/setup/TemplateFiles/Azobenzene/"+configuration+"/Azobenzene.mol2"
        self.res1 = link1
        self.res2 = link2
        
    def readPDB(self):
        f = open(""+self.pdbFile+"",'r')
        pdb = f.readlines()[0:]
        f.close()
        n = 0
        for line in pdb[0:]: # Start coordinate handling when the atoms start
            if line[0:4] == "ATOM":
                break
            n+=1
        
        SGx, SGy , SGz  = [], [], []
        front, back = [], []
        for line in pdb[n:]:          
            coor = line.split()
            
            if coor[2] == "SG":
                SGx.append(float(coor[5]))
                SGy.append(float(coor[6]))
                SGz.append(float(coor[7]))
            # The back and front coordinates are used to calculates the direction away from the protein.
            if coor[4] == "175":
                if coor[2] == "CA":
                    front.append(float(coor[5]))
                    front.append(float(coor[6]))   
                    front.append(float(coor[7]))
            if coor[4] == "226":
                if coor[2] == "CA":
                    back.append(float(coor[5]))
                    back.append(float(coor[6]))
                    back.append(float(coor[7]))
                    
                
            if line[0:3] == "TER": # Stop reading if the pdb contains a new molecule
                break
            if line [0:3] == "END": #Breakout if file ends
                break
            if coor[2] == "OXT":
                break
        
        self.SG1 = np.array([SGx[0],SGy[0],SGz[0]])
        self.SG2 = np.array([SGx[1],SGy[1],SGz[1]])
        self.vector_cyx = np.array(self.SG1-self.SG2)/np.linalg.norm(self.SG1-self.SG2)
        
        push = np.array([back[0]-front[0],back[1]-front[1],back[2]-front[2]])
        self.vector_push = 3.5*push/np.linalg.norm(push)

    def readAzo(self): #READ the Azobenzene mol2 file
        f = open(self.azoFile,'r')
        mol2 = f.readlines()[0:]
        f.close()
        
        Sx,S1x = [],[]
        Sy,S1y = [],[] 
        Sz,S1z = [],[]
        
        k=1
        for line in mol2[0:]: # Start coordinate handling when the atoms start
            if line[0:13] == "@<TRIPOS>ATOM":
                break
            k+=1
                
        for line in mol2[k:]:          
            if line[0:13] == "@<TRIPOS>BOND": # Stop reading if the pdb contains a new molecule
                break
            
            coor = line.split()
            if coor[1] == "S":
                Sx = float(coor[2])
                Sy = float(coor[3])
                Sz = float(coor[4])
                
            if coor[1] == "S1":
                S1x = float(coor[2])
                S1y = float(coor[3])
                S1z = float(coor[4])
                    
        S = np.array([Sx,Sy,Sz])
        S1 = np.array([S1x,S1y,S1z])
        
        self.vector_azo = np.array(S-S1)/np.linalg.norm(S-S1)

    def CalcRotMatrix(self): #Calculate the rotation matrix

        I = np.array([[1,0,0],[0,1,0],[0,0,1]])
        
        theta = np.arccos(np.dot(self.vector_azo,self.vector_cyx)/(np.linalg.norm(self.vector_azo)*np.linalg.norm(self.vector_cyx)))
        print theta*57.7
        
        k = np.cross(self.vector_azo,self.vector_cyx)
        x = k/np.linalg.norm(k)
        #tensorproduct of rotation axis
        uxu = np.array([[x[0]**2,   x[0]*x[1], x[1]*x[2]],
                        [x[0]*x[1], x[1]**2,   x[1]*x[2]],
                        [x[0]*x[2], x[1]*x[2], x[2]**2]])
        
        
        ux = np.array([  [0,   -x[2], x[1]],
                        [x[2], 0,   -x[0]],
                        [-x[1],x[0], 0  ]])
                        
        
        
        self.R = I*np.cos(theta) + np.sin(theta)*ux + (1-np.cos(theta))*uxu
        print "This is the calculated Rotation matrix:"
        print self.R
        print ""
        print ""
        print ""
        print "using this matrix the Azobenzene is rotated to align with the SG-SG vector of the CYX residues if the protein."
        print "This is the old azo vector"
        print self.vector_azo
        print "this is the new azo vector"
        vector = np.dot(self.R,self.vector_azo)
        print vector
        print "this is the cyx vector"
        print self.vector_cyx


    def leapTemp(self):# The LeapTemp function is used to calculate the coordinates of the rotated Azobenzene. Thus the translation coordinates are calculated in the next function.
        
        buffer = """#Created by Crosslinker.py
        source leaprc.ff14SB
        source leaprc.gaff
        
        protein = loadpdb """+self.pdbFile+"""
        azo = loadmol2 """+self.azoFile+"""
        
        transform azo { { """+str(self.R[0][0])+""" """+str(self.R[0][1])+""" """+str(self.R[0][2])+""" 0}
                        { """+str(self.R[1][0])+""" """+str(self.R[1][1])+""" """+str(self.R[1][2])+""" 0}
                        { """+str(self.R[2][0])+""" """+str(self.R[2][1])+""" """+str(self.R[2][2])+""" 0}
                        {           0                   0                   0            1}}
                        
                        
        protein = combine {protein azo}
        savepdb protein """+absdir+"""/in_files/temp.pdb
        """
                
        name = "LEaP_transform.ff"
        f = open(""+name+"",'w')
        f.write(buffer)
        f.close()
        
        os.system("tleap -f LEaP_transform.ff")
        
    def CalcTranslation(self):
        f = open(""+absdir+"/in_files/temp.pdb",'r')
        pdb = f.readlines()[0:]
        f.close()
        n = 0
        for line in pdb[0:]: # Start coordinate handling when the atoms start
            if line[0:4] == "ATOM":
                break
            n+=1
            
        k = 1
        for line in pdb[n:]:          
            k+=1    
            if line[0:3] == "TER": # Stop reading if the pdb contains a new molecule
                break
            
        for line in pdb[k:]:
            if line[0:3] == "TER": # Stop reading if the pdb contains a new molecule
                break
            coor = line.split()
            if coor[2] == "S":
                Sx = float(coor[5])
                Sy = float(coor[6])
                Sz = float(coor[7])
                
            if coor[2] == "S1":
                S1x = float(coor[5])
                S1y = float(coor[6])
                S1z = float(coor[7])
                
        S = np.array([Sx,Sy,Sz])
        S1 = np.array([S1x,S1y,S1z])
        
        self.TranslationAzo = self.SG1-S

    def leapCrosslink(self):
        buffer = """#Created by Crosslinker.py
        source leaprc.ff14SB
        source leaprc.gaff
        
        protein = loadpdb """+self.pdbFile+"""
        azo = loadmol2 """+self.azoFile+"""
        
        transform azo { { """+str(self.R[0][0])+""" """+str(self.R[0][1])+""" """+str(self.R[0][2])+""" 0}
                        { """+str(self.R[1][0])+""" """+str(self.R[1][1])+""" """+str(self.R[1][2])+""" 0}
                        { """+str(self.R[2][0])+""" """+str(self.R[2][1])+""" """+str(self.R[2][2])+""" 0}
                        {           0                   0                   0            1}}
                        
        translate azo {"""+str(self.TranslationAzo[0])+""" """+str(self.TranslationAzo[1])+""" """+str(self.TranslationAzo[2])+"""}
        translate azo {"""+str(self.vector_push[0])+""" """+str(self.vector_push[1])+""" """+str(self.vector_push[2])+"""}
        
        protein = combine {protein azo}
        bond protein."""+self.res1+""".SG protein.LIG.S
        bond protein."""+self.res2+""".SG protein.LIG.S1
        savepdb protein """+absdir+"""/in_files/"""+protein+"""_crosslink.pdb
        """
                
        name = "LEaP_translate.ff"
        f = open(""+name+"",'w')
        f.write(buffer)
        f.close()
        os.system("tleap -f LEaP_translate.ff")


def main():
    Crosslink = Crosslinker()        
    Crosslink.readPDB()
    Crosslink.readAzo()
    Crosslink.CalcRotMatrix()
    Crosslink.leapTemp()
    Crosslink.CalcTranslation()
    Crosslink.leapCrosslink()                    
if __name__ == '__main__': main()
            

