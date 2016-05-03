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

the_list = ["lib","lib/setup"]
for folders in the_list:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],str(folders))))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
        
from variables import *

closest = []
threshold = 3.2
tries = 100
increment = 0.5

class CalcIonPosition():
    def __init__(self): 
        if MakeMutations == "on":
            self.pdbFile = ""+absdir+"/in_files/"+protein+"_mutation.pdb"
        else:
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
        self.threshold = threshold + 0.5
        if protein in ("pbpu", "pbpv"):   
            self.list = [8,9,10,32,33,63,142,146,147,148]
        if protein in ("1IXH", "2ABH"): 
            self.list = [10,11,38,56,135,137,139,140,141]
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
    
    def Distance(self): # Find the distance of the ligand to the nearest atoms in the protein
        self.distance = []        
        self.dist = []
        self.vector = []
        self.Atomnumber = []

        for i in range(0,len(self.x)): #Find the distance to each atom of the binding site atoms, and append to the dist list.
            self.dist.append(math.sqrt((self.ionPos[0]-self.ProteinCoordinates[0][i])**2
                                        +(self.ionPos[1]-self.ProteinCoordinates[1][i])**2
                                        +(self.ionPos[2]-self.ProteinCoordinates[2][i])**2))

        for i in range(0,len(self.dist)): # Of the binding site atoms which are below a threshold value? Print these values for information purposes.
            if self.dist[i] < self.threshold:
                self.Atomnumber.append(i)
                self.distance.append(self.dist[i])
                print self.residues[i], self.dist[i]
        
        closest_temp = min(self.dist) # What is the distance to the nearest atom?
        closest.append(closest_temp)
        print ""
        print "this is the history of the closest atoms:"
        print closest
        return closest
         
    def FindNearestAtom(self):
        #Find the nearest atom from the distance list.
        self.NearestAtom = min(enumerate(self.distance), key=itemgetter(1))[0]
        #Find the coordinates of the nearest atom!
        AtomCoordinates = np.array([self.ProteinCoordinates[0][self.Atomnumber[self.NearestAtom ]], 
                                    self.ProteinCoordinates[1][self.Atomnumber[self.NearestAtom ]],
                                    self.ProteinCoordinates[2][self.Atomnumber[self.NearestAtom ]]])
        # Find a vector to move the ligand with
        self.vector = np.array(self.ionPos-AtomCoordinates)/np.linalg.norm(self.ionPos-AtomCoordinates)
        print ""
        print "Moving Ligand with direction:" 
        print self.vector
        
    def MovePhosphate(self): # Move the postition of the ion with the vector multiplied by a small value
        print ""
        print "This is the old ion position:"
        print self.ionPos
        self.ionPos = self.ionPos + increment*self.vector
        print "This is the new ion Position:"    
        print self.ionPos
        return self.ionPos
                
    def Evaluate(self): # Evaluate the distance to the nearest atom and write the coordinates to the coordinates.dat file. This value is overwritten for each iteration
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
        print "Iteration number: "+str(n)+""
        Calc.Distance()            
        print ""
        print "this is the distance to the closest atom"        
        print closest[i]
        print "Optimizing Ligand Position"   
        
        if closest[i] > threshold: #If the nearest atom exceeds the threshold value the position optimization is complete
            print "Success!! Distance to nearest atom is larger than the threshold value"
            break
        else: # Repeat the process of finding the nearest atom, move the phosphate and evaluate the new distance
            Calc.FindNearestAtom()
            Calc.MovePhosphate()
            Calc.Evaluate()
        print ""
        print "###############################################"
        print ""
        if n == tries-1:
             raise Exception('Failure!: The ion cannot be positioned in the protein within the number of iterations \n'
                             'Are you sure you specified the right protein and ligand? \n'
                             'If yes!: You can try to increase the number of iterations or decrease the threshold limit to the nearest atom!'
                             'Good luck!')

        
    Calc.Evaluate()
    print "Done Optimizing the ligand position"
    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
                
if __name__ == '__main__': main()
