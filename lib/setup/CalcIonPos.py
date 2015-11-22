# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 16:31:08 2015

@author: sigurd
"""
import math
import numpy as np
from operator import itemgetter
import os,sys,inspect

the_list = ["lib","lib/setup"]
for folders in the_list:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],str(folders))))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)

from variables import *

global closest        
closest = []
threshold = 3.5
tries = 20

class CalcIonPosition():
    def __init__(self):
        self.pdbFile = ""+absdir_home+"/lib/setup/TemplateFiles/pdb_files/"+protein+"/"+structure+""
        self.ligandpdbFile = ""+absdir_home+"/lib/setup/TemplateFiles/ion/"+ionName+".pdb"
        self.x,self.y,self.z = [],[],[]
        self.x_bind,self.y_bind,self.z_bind = [],[],[]
        self.x_ion,self.y_ion,self.z_ion = [],[],[]
        self.data = []
        self.atomnumber = []
        self.atomname   = []
        self.residuename= []
        self.residuenumber= []
        self.threshold = threshold
        self.distance = []
#        self.coordinates = str("0" "0" "0")        
    def ReadProteinCoordinates(self):
        f = open(self.pdbFile,'r')
        pdb = f.readlines()[0:]
        f.close()
        for line in pdb[0:]:
            coor = line.split()
            if line[0:4] == 'ATOM':
        # Coordinates of the entire protein                
                self.data.append(coor)
                self.atomnumber.append(int(coor[1]))
                self.atomname.append(str(coor[2]))
                self.residuename.append(str(coor[3]))
                self.residuenumber.append(int(coor[4]))
                self.x.append(float(coor[5]))
                self.y.append(float(coor[6]))
                self.z.append(float(coor[7]))
        # Append x,y,z coordinates for residue number (8,9,10,32,33,63,142,146,147,148)
        # If row 4 equals residue (8,9,10,32,33,63,142,146,147,148) , then append the coordinates
            if int(coor[4]) == int(8):
                self.x_bind.append(float(coor[5]))
                self.y_bind.append(float(coor[6]))
                self.z_bind.append(float(coor[7]))
            if int(coor[4]) == int(9):    
                self.x_bind.append(float(coor[5]))
                self.y_bind.append(float(coor[6]))
                self.z_bind.append(float(coor[7]))
            if int(coor[4]) == int(10):    
                self.x_bind.append(float(coor[5]))
                self.y_bind.append(float(coor[6]))
                self.z_bind.append(float(coor[7]))
            if int(coor[4]) == int(32):    
                self.x_bind.append(float(coor[5]))
                self.y_bind.append(float(coor[6]))
                self.z_bind.append(float(coor[7]))
            if int(coor[4]) == int(33):    
                self.x_bind.append(float(coor[5]))
                self.y_bind.append(float(coor[6]))
                self.z_bind.append(float(coor[7]))
            if int(coor[4]) == int(63):    
                self.x_bind.append(float(coor[5]))
                self.y_bind.append(float(coor[6]))
                self.z_bind.append(float(coor[7]))
            if int(coor[4]) == int(142):    
                self.x_bind.append(float(coor[5]))
                self.y_bind.append(float(coor[6]))
                self.z_bind.append(float(coor[7]))
            if int(coor[4]) == int(146):    
                self.x_bind.append(float(coor[5]))
                self.y_bind.append(float(coor[6]))
                self.z_bind.append(float(coor[7]))
            if int(coor[4]) == int(147):    
                self.x_bind.append(float(coor[5]))
                self.y_bind.append(float(coor[6]))
                self.z_bind.append(float(coor[7]))
            if int(coor[4]) == int(148):    
                self.x_bind.append(float(coor[5]))
                self.y_bind.append(float(coor[6]))
                self.z_bind.append(float(coor[7]))
        # Coordinates of the center of the entire protein
        self.residues = zip(self.atomnumber, self.atomname, self.residuename,self.residuenumber)
        avgX = np.average(self.x)
        avgY = np.average(self.y)
        avgZ = np.average(self.z)
        self.CenterOfProtein = np.array([avgX,avgY,avgZ])
        self.ProteinCoordinates = np.array([self.x,self.y,self.z])
        
        # Coordinates of the binding site
        self.Binding_center = np.array([np.average(self.x_bind),np.average(self.y_bind),np.average(self.z_bind)])
   
    def IonPos(self):
        if ionName == "HPO4":
            endline = 6
        if ionName == "H2PO4":
            endline = 7 
        if ionName == "H3PO4":
            endline = 7 
        f = open(self.ligandpdbFile,'r')
        pdb = f.readlines()[0:endline]
        f.close()
        for line in pdb:
            coor_ion = line.split()
            self.x_ion.append(float(coor_ion[5]))
            self.y_ion.append(float(coor_ion[6]))
            self.z_ion.append(float(coor_ion[7]))
        
        # Coordinates of the ion
        ionX = np.average(self.x_ion)
        ionY = np.average(self.y_ion)
        ionZ = np.average(self.z_ion)
        self.ion = [ionX,ionY,ionZ]
        
        Binding_site = self.Binding_center - self.ion
                
        self.ionPosX = Binding_site[0]
        self.ionPosY = Binding_site[1]
        self.ionPosZ = Binding_site[2]
        self.ionPos = [self.ionPosX,self.ionPosY,self.ionPosZ]
        return self.ionPos
    
    def Distance(self):
        self.dist = []
        self.vector = []
        self.q = []

        for i in range(0,len(self.x)):
            self.dist.append(math.sqrt((self.ionPos[0]-self.ProteinCoordinates[0][i])**2
                                        +(self.ionPos[1]-self.ProteinCoordinates[1][i])**2
                                        +(self.ionPos[2]-self.ProteinCoordinates[2][i])**2))

        for i in range(0,len(self.dist)): # Printing the closes residues - for information purposes
            if self.dist[i] < self.threshold:
                self.q.append(i)
                self.distance.append(self.dist[i])
                print self.residues[i], self.dist[i]
        
        closest_temp = min(self.dist)
        closest.append(closest_temp)
        print ""
        print "this is the closest list:"
        print closest
        return closest
         
    def FindNearestAtom(self):       
        Atom = min(enumerate(self.distance), key=itemgetter(1))[0]
        AtomNumber = self.q[Atom]
        AtomCoordinates = np.array([self.ProteinCoordinates[0][AtomNumber],
                                    self.ProteinCoordinates[1][AtomNumber],
                                    self.ProteinCoordinates[2][AtomNumber]])
        self.vector = np.array(self.ionPos-AtomCoordinates)/np.linalg.norm(self.ionPos-AtomCoordinates)
        print ""
        print "Moving Ligand with direction:" 
        print self.vector
        
    def MovePhosphate(self):
        print ""
        print "This is the old ion position:"
        print self.ionPos
        self.ionPos = self.ionPos + 0.1*self.vector
        print "This is the new ion Position:"    
        print self.ionPos
        return self.ionPos
                
    def Evaluate(self):
        print ""
        for i in range(0,len(self.x)):
            self.dist.append(math.sqrt((self.ionPos[0]-self.ProteinCoordinates[0][i])**2
                                        +(self.ionPos[1]-self.ProteinCoordinates[1][i])**2
                                        +(self.ionPos[2]-self.ProteinCoordinates[2][i])**2))
        self.criterion = min(self.dist)
        print "Evaluate: Distance to the closest atom is:"        
        print self.criterion
        coordinates = ""+str(round(self.ionPos[0],2))+" "+str(round(self.ionPos[1],2))+" "+str(round(self.ionPos[2],2))+""
        f = open(""+absdir+"/in_files/coordinates.dat",'w')
        f.write(""+coordinates+"")
        f.close()
        print coordinates
    
 
def main():
    Calc = CalcIonPosition()        
    Calc.ReadProteinCoordinates()    
    Calc.IonPos()
    n = 0
    print "Starting Optimizing the Ligand Position"
    print ""    
    print "###############################################"    
    print ""
    for i in range(0,tries):
        n +=1   
        print "Iteration number:"+str(n)+""
        Calc.Distance()            
        print ""
        print "this is the distance to the closest atom"        
        print closest[i]
        print "Optimizing Ligand Position"   
        
        if closest[i] > threshold:
            print "Distance to nearest atom is larger than the threshold value"
            break
        else: 
            Calc.FindNearestAtom()
            Calc.MovePhosphate()
            Calc.Evaluate()
        print ""
        print "###############################################"
        print ""
        if n == tries-1:
             raise Exception('The ion cannot be positioned in the protein')

        
    Calc.Evaluate()

            
if __name__ == '__main__': main()
