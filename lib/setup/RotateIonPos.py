# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 15:07:01 2016

@author: sigurd
"""


# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 16:31:08 2015

@author: sigurd
"""

# This script optimizes the position of a ligand in complex with a protein. This is done by calculating the average position of the binding site residues and placing the ligand there. 
# Subsequently the distance to the nearest atoms from the center of the ligand is calculated. If this value exceeds a threshold value the ion will be moved in a direction with a vector defined the ligand and the nearest atom. The distance to the nearest atoms is again evaluated. If the value is still below the threshold value the ligand will be moved again, in the same scheme as just described. 
# If the value exceeds the threshold the position of the ligand is optimized and the coordinates will be written to a coordinates.dat file. This will be read by the next script, that actually combines the protein and ligand. 
# If the ion cannot be exceed the threshold value within the limit of tries, the system will fail and send out an error message. 

import math
import numpy as np
from operator import itemgetter
import os,sys,inspect
import random

the_list = ["lib","lib/setup"]
for folders in the_list:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],str(folders))))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
        
from variables import *

closest = []
threshold = 3.2
tries = 200
increment = 0.25

class RotIonPosition():
    def __init__(self): 
        if MakeMutations == "on":
            self.pdbFile = ""+absdir+"/in_files/"+protein+"_mutation.pdb"
        else:
            self.pdbFile = ""+absdir_home+"/lib/setup/TemplateFiles/pdb_files/"+protein+"/"+structure+""
        
        self.ligandmol2File =  ""+absdir+"/in_files/HPO4_newPos.mol2"   
#        self.ligandmol2File = ""+absdir+"/in_files/HPO4_rotation.mol2"


        self.x,self.y,self.z = [],[],[]
        self.x_bind,self.y_bind,self.z_bind = [],[],[]
        self.x_ion,self.y_ion,self.z_ion = [],[],[]
        self.atomType = []
        self.data = []
        self.atomnumber = []
        self.atomname   = []
        self.residuename= []
        self.residuenumber= []
        self.threshold = threshold
        if protein in ("pbpu", "pbpv"):   
            self.list = [8,9,10,32,33,63,142,146,147,148]
        if protein in ("1IXH", "2ABH"): 
            self.list = [10,11,38,56,135,137,139,140,141,195,254]
#            self.list = [8,9,32,62,141,145,146,147]
        if protein in ("SGAGKT"):
            self.list = [1,2,3,4,5,6]
            
    def ReadProteinCoordinates(self): # Read the coordinates of the protein pdb file
        f = open(self.pdbFile,'r')
        pdb = f.readlines()[0:]
        f.close()
        n = 0
        for line in pdb[0:]: # Start coordinate handling when the atoms start
            if line[0:4] == "ATOM":
                break
            n+=1
        
        for line in pdb[n:]:
            coor = line.split()
            if line[0:3] == "TER": # Stop reading if the pdb contains a new molecule
                break
            if line [0:3] == "END": #Breakout if file ends
                break
            if str(coor[3]) == "WAT": # Stop reading if the pdb contain water
                break
            if line[0:4] == 'ATOM':
        # Coordinates of the entire protein                
                self.data.append(coor)
                self.atomnumber.append(int(coor[1]))
                self.atomname.append(str(coor[2]))
                self.residuename.append(str(coor[3]))
                
                # Write all protein coordinates to file
                try: # Try to read column 5. If it is a string, then append from other columns
                    if isinstance(int(coor[4]),int) == True : # Read column 5 from pdb file
                        self.residuenumber.append(int(coor[4]))
                        self.x.append(float(coor[5]))
                        self.y.append(float(coor[6]))
                        self.z.append(float(coor[7]))               
                except ValueError: # if the value is a string, it will yield an ValueError
                    self.residuenumber.append(int(coor[5]))
                    self.x.append(float(coor[6]))
                    self.y.append(float(coor[7]))
                    self.z.append(float(coor[8]))
            
            # Write only chosen residues to X_bind lists
            try:# Try to read column 5. If it is a string, then append from other columns
                if isinstance(int(coor[4]),int) == True :
                    for i in self.list: # Append the coordinates of the binding residues.
                        if int(coor[4]) == int(i):
                            self.x_bind.append(float(coor[5]))
                            self.y_bind.append(float(coor[6]))
                            self.z_bind.append(float(coor[7]))
            except ValueError:
                for i in self.list: # Append the coordinates of the binding residues.
                    if int(coor[5]) == int(i):
                        self.x_bind.append(float(coor[6]))
                        self.y_bind.append(float(coor[7]))
                        self.z_bind.append(float(coor[8]))
        

        # Coordinates of the center of the entire protein
        self.residues = zip(self.atomnumber, self.atomname, self.residuename,self.residuenumber)
        avgX = np.average(self.x)
        avgY = np.average(self.y)
        avgZ = np.average(self.z)
        self.CenterOfProtein = np.array([avgX,avgY,avgZ])
        self.ProteinCoordinates = np.array([self.x,self.y,self.z]) #The ProteinCoordinates contains the coordinates of the binding site atoms
        
        # Coordinates of the binding site
        self.Binding_center = np.array([np.average(self.x_bind),np.average(self.y_bind),np.average(self.z_bind)])
   
    def IonPos(self): # Find the position of the ligand from the pdb/mol2 file and place the ligand in the binding site.
        # Initial read of the mol2 file (Know when to start and stop reading the coordinates)           
        f = open(self.ligandmol2File,'r')
        mol2 = f.readlines()[0:]
        f.close()
        i = 0
        n, m = 0, 0
        
        for line in mol2:
            if "@<TRIPOS>ATOM" == line.strip():
                print "found @<TRIPOS>ATOM"
                n = i
                print n
            if "@<TRIPOS>BOND" == line.strip():
                print "found @@<TRIPOS>BOND"
                m = i
                print m
            i += 1
        # Read the coordinates and append to x-y and z -_ion
        f = open(self.ligandmol2File,'r')
        mol2 = f.readlines()[n+1:m]
        f.close()
        for line in mol2:
            coor_ion = line.split()
            print coor_ion[4]
            self.x_ion.append(float(coor_ion[2]))
            self.y_ion.append(float(coor_ion[3]))
            self.z_ion.append(float(coor_ion[4]))
            self.atomType.append(str(coor_ion[5]))
    
        # Coordinates of the ion
        ionX = np.average(self.x_ion)
        ionY = np.average(self.y_ion)
        ionZ = np.average(self.z_ion)
        self.ion = [ionX,ionY,ionZ]
        
        Binding_site = self.Binding_center - self.ion
                
        self.ionPosX = Binding_site[0] + random.random()*2-1
        self.ionPosY = Binding_site[1] + random.random()*2-1
        self.ionPosZ = Binding_site[2] + random.random()*2-1
        self.ionPos = [self.ionPosX,self.ionPosY,self.ionPosZ]
        return self.ionPos
    
    def CalcRotationVectors(self):
        #Define a vector from oh-ho
        print self.x_ion[0]
        self.p5 = np.array([self.x_ion[0],self.y_ion[0],self.z_ion[0]])
        self.o1 = np.array([self.x_ion[2],self.y_ion[0],self.z_ion[2]])
        self.oh = np.array([self.x_ion[4],self.y_ion[4],self.z_ion[4]])
        self.ho = np.array([self.x_ion[5],self.y_ion[5],self.z_ion[5]])
        
        self.p5oh = np.array(self.p5-self.oh)/np.linalg.norm(self.p5-self.oh)
        self.p5o1 = np.array(self.p5-self.o1)/np.linalg.norm(self.p5-self.o1)
        self.ohho = np.array(self.oh-self.ho)/np.linalg.norm(self.oh-self.ho)
        self.p5ho = np.array(self.p5-self.ho)/np.linalg.norm(self.p5-self.ho)
        #define a vector from CB to something of Asp56        
        n = 0        
        CB = []
        CG = []
        for i in self.residuenumber:
            n += 1
            if i == 56:
                if self.atomname[n] == "CB":
                    CB = np.array([self.x[n],self.y[n],self.z[n]])
                if self.atomname[n] == "CG":
                    CG = np.array([self.x[n],self.y[n],self.z[n]])
                if self.atomname[n] == "OD2":
                    OD2 = np.array([self.x[n],self.y[n],self.z[n]])
                    
        self.CgOd2 = np.array(OD2-CG)/np.linalg.norm(OD2-CG)
        self.CbCg  = np.array(CG-CB)/np.linalg.norm(CG-CB)
        self.Cgp5  = -np.array(CG-self.p5)/np.linalg.norm(CG-self.p5)
        
        
    def CalcRotationMatrix(self):
        I = np.array([[1,0,0],[0,1,0],[0,0,1]])
        
        v1 = self.p5oh
        v2 = self.Cgp5
        theta = np.arccos(np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)))
        k = np.cross(v1,v2)
        x = k/np.linalg.norm(k)

        #tensorproduct of rotation axis
        uxu = np.array([[x[0]*x[0], x[0]*x[1],   x[0]*x[2]],
                        [x[0]*x[1], x[1]*x[1],   x[1]*x[2]],
                        [x[0]*x[2], x[1]*x[2],   x[2]*x[2]]])
        
        
        ux = np.array([ [0,   -x[2], x[1]],
                        [x[2], 0,   -x[0]],
                        [-x[1],x[0], 0  ]])
                        
        
        # R = cos(theta)I+sin(theta)*u_x + (1-cos(theta))*u >cross> u
        self.R = I*np.cos(theta) + np.sin(theta)*ux + (1-np.cos(theta))*uxu
        
        print "this is the determinant of the rotation matrix"
        print np.linalg.det(self.R)  
        print ""
        print ""
        print ""
        print ""
        print ""
        print ""
        print ""
        print ""
        print ""
        
        f = open(""+absdir+"/in_files/rotation.dat",'w')
        f.write("{"+str(self.R[0][0])+" "+str(self.R[0][1])+" "+str(self.R[0][2])+" 0}")
        f.write("{"+str(self.R[1][0])+" "+str(self.R[1][1])+" "+str(self.R[1][2])+" 0}")
        f.write("{"+str(self.R[2][0])+" "+str(self.R[2][1])+" "+str(self.R[2][2])+" 0}")
        f.write("{       0               0               0             1}")
        f.close()
        
    def leapPosition(self):
        buffer = """#Created by CalcIonPos.py
        source leaprc.gaff
        
        HPO4 = loadmol2 """+self.ligandmol2File+"""
        
        transform HPO4 { { """+str(self.R[0][0])+""" """+str(self.R[0][1])+""" """+str(self.R[0][2])+""" 0}
                        { """+str(self.R[1][0])+""" """+str(self.R[1][1])+""" """+str(self.R[1][2])+""" 0}
                        { """+str(self.R[2][0])+""" """+str(self.R[2][1])+""" """+str(self.R[2][2])+""" 0}
                        {           0                   0                   0            1}}
                        
                        
        savemol2 HPO4 """+absdir+"""/in_files/HPO4_rotation.mol2 1
        quit
        """
                
        name = "LEaP_transform.ff"
        f = open(""+absdir+"/in_files/"+name+"",'w')
        f.write(buffer)
        f.close()
        
        os.system("tleap -f "+absdir+"/in_files/"+name+"")
    
    
        
def main():
    Rot = RotIonPosition()        
    Rot.ReadProteinCoordinates()  
    Rot.IonPos()
    Rot.CalcRotationVectors()
    Rot.CalcRotationMatrix() 
if __name__ == '__main__': main()
