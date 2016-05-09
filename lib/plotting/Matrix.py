# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 19:13:38 2015

@author: sigut
"""
import os, math, argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputPlot',
                    help = 'input structure for onclick',
                    default = "Delta")
                    
args = parser.parse_args()
plot = args.inputPlot


pdbList = ["2ABH","1OIB"]
atomAlign = "CB"

class MatrixDistance():
            
    def __init__(self,pdbList):
        self.data = []
        self.atomnumber = []
        self.atomname   = []
        self.residuename = []
        self.residuenumber = []
        self.x,self.y,self.z = [],[],[]
        
        self.xA, self.yA, self.zA = [],[],[]
        self.xB, self.yB, self.zB = [],[],[]
        self.xC, self.yC, self.zC = [],[],[]
        
        self.listA, self.listB, self.listC = [], [], []
        for i in [221,222,223,226,229,248,]: #range(221,230): #220,231 []
            self.listA.append(i)
        
        for i in range(275,284): # 268,291
            self.listB.append(i)
        for i in range(285,289):
            self.listB.append(i)
        
        for i in range(293,307): # 297,307
            self.listC.append(i)
            
        
        self.listABC = []
        self.listABC.append(self.listA)        
        self.listABC.append(self.listB)
        self.listABC.append(self.listC)
    
        
    def ReadPDP(self,pdbList):
        self.xABC, self.yABC, self.zABC = [],[],[]
        f = open(""+pdbList+"_sequence.pdb",'r')
        print "Read in pdb file: " +pdbList+""
        pdb = f.readlines()[0:]
        f.close()
        for line in pdb[0:]:
            coor = line.split()
            if line[0:3] == "TER": # Stop reading if the pdb contains a new molecule
                break
            if str(coor[3]) == "WAT": # Stop reading if the pdb contain water
                break
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

        
    def FindCoordinates(self):
        n = 0
        self.namesListA = [] 
        self.namesListB = [] 
        self.namesListC = []
        self.namesListABC =[]
        for i in self.residuenumber: #Loop over residues in the protein, with i being the index (1-321)
            n += 1
        #####################################################################################
            for j in self.listA: #Loop over residues in helix A                             #
                if i == j:                                                                  #
                    if self.atomname[n] == atomAlign:                                            #
                        self.xA.append(self.x[n])                                           #
                        self.yA.append(self.y[n])                                           #
                        self.zA.append(self.z[n])                                           #
                        self.namesListA.append(self.residuename[n])                         #
                                                                                            #
            for j in self.listB: #Loop over residues in helix B                             #
                if i == j:                                                                  #
                    if self.atomname[n] == atomAlign:                                           # ! Currently not used!
                        self.xB.append(self.x[n])                                           #
                        self.yB.append(self.y[n])                                           #
                        self.zB.append(self.z[n])                                           #        
                        self.namesListB.append(self.residuename[n])                         #
                                                                                            #    
            for j in self.listC: #Loop over residues in helix C                             #
                if i == j:                                                                  #        
                    if self.atomname[n] == atomAlign:                                            #
                        self.xC.append(self.x[n])                                           #
                        self.yC.append(self.y[n])                                           #
                        self.zC.append(self.z[n])                                           #        
                        self.namesListC.append(self.residuename[n])                         #
        #####################################################################################
            
            for k in range(0,len(self.listABC)): #Loop over residues in helix A, B and C
                for j in self.listABC[k]:
                    if i == j:
                        if self.atomname[n] == atomAlign:
                            self.xABC.append(self.x[n])
                            self.yABC.append(self.y[n])
                            self.zABC.append(self.z[n])        
                            self.namesListABC.append(self.residuename[n])  
        
    def CalcDistance(self,pdbList):
               
        self.matrixAB = []
        self.matrixAC = []
        self.matrixBC = []
        f = open("Distance_"+pdbList+".dat",'w')
        for i in range(0,len(self.listA)): # Iterate over all residues in the listA
            self.distAB = []
            n = 0 # For writing to a data file
            for j in range(0,len(self.listB)): # Iterate over all residues in listB
                self.distAB.append(math.sqrt((self.xA[i]-self.xB[j])**2 + (self.yA[i]-self.yB[j])**2 + (self.zA[i]-self.zB[j])**2)) #Calculate the distance between alle elements
                f.write(""+str(self.listA[i])+" "+self.namesListA[i]+" - "+str(self.listB[j])+" "+self.namesListB[j]+" = "+str(self.distAB[n])+" \n") # Write values to data file:
                n += 1
            
            self.matrixAB.append(self.distAB) #Write to matrix AB for every finished j iteration
        
    
            self.distAC = []
            n = 0
            for k in range(0,len(self.listC)):
                self.distAC.append(math.sqrt((self.xA[i]-self.xC[k])**2 + (self.yA[i]-self.yC[k])**2 + (self.zA[i]-self.zC[k])**2))
                f.write(""+str(self.listA[i])+" "+self.namesListA[i]+" - "+str(self.listC[k])+" "+self.namesListC[k]+" = "+str(self.distAC[n])+" \n") # Write values to data file:
                n += 1
            self.matrixAC.append(self.distAC)
        
            # Close the data file
        
            
        for i in range(0,len(self.listB)): # Make matrix over listB - listC
            self.distBC = []
            n = 0
            for j in range(0,len(self.listC)):
                self.distBC.append(math.sqrt((self.xB[i]-self.xC[j])**2 + (self.yB[i]-self.yC[j])**2 + (self.zB[i]-self.zC[j])**2))
                f.write(""+str(self.listB[i])+" "+self.namesListB[i]+" - "+str(self.listC[j])+" "+self.namesListC[j]+" = "+str(self.distBC[n])+" \n") # Write values to data file:
                n += 1
            self.matrixBC.append(self.distBC)
            
        f.close()
            
        self.matrixBA = np.transpose(self.matrixAB)
        self.matrixBA = self.matrixBA[::-1]
        
        self.matrixCA = np.transpose(self.matrixAC)
        self.matrixCA = self.matrixCA[::-1]
        
        self.matrixCB = np.transpose(self.matrixBC)
        self.matrixCB = self.matrixCA[::-1]
    

        
    def Matrix(self,pdbList):
        self.matrixABC = []
        self.matrixCBA = []
        self.distABC = []
        self.distCBA = []

        n = -1
        for k in range(0,len(self.listABC)):                # Loop over the three lists (A, B and C) in listABC: k = 0,1,2
            for i in range(0,len(self.listABC[k])):         # Loop over the residues in listABC[0], listABC[1] and listABC[2]
                self.distABC = []                           # Restart the distABC list 
                m = 0
                n += 1
                for l in range(0,len(self.listABC)):        # Loop over the three lists (A, B and C) in listABC: l = 0,1,2
                    for j in range(0,len(self.listABC[l])): # Loop over the elements in listABC[0], listABC[1] and listABC[2]
                        self.distABC.append(math.sqrt((self.xABC[n]-self.xABC[m])**2 + (self.yABC[n]-self.yABC[m])**2 + (self.zABC[n]-self.zABC[m])**2))
                        m += 1
                                        
                self.matrixABC.append(self.distABC) # Original data matrix for plotting

        
        # Save to numpy data file for reading in another script        
        np.save("Matrix_"+str(pdbList)+"",self.matrixABC)
        f = open("Matrix_"+str(pdbList)+".dat",'w')        
        f.write(str(self.matrixABC))
        f.close()
        
    def Ticks(self):
                   
        self.x_axisLength, self.y_axisLength = [] , []
        self.x_axis, self.y_axis = [], []
               
        # Define the length of the plot
        n = 0
        for l in range(0,len(self.listABC)):
            for i in range(0,len(self.listABC[l])):
                self.x_axisLength.append(n)
                self.y_axisLength = self.x_axisLength
                n += 1
        
        # Define the ticks, corresponding to the matrix 
        n = 0
        for j in range(0,len(self.listABC)):
            for i in range(0,len(self.listABC[j])):
                self.x_axis.append(str(self.listABC[j][i]) + " " + str(self.namesListABC[n]))
                n += 1
        
        namesListReverse = []      
        namesListReverse = self.namesListABC #[::-1]
        n = 0 # Index for counting correcly in the loop        
        for j in range(0,len(self.listABC)): #Reverse the y-axis to get the correct labelling
            for i in range(0,len(self.listABC[j])):
                self.y_axis.append(str(self.listABC[j][i]) + " " + str(namesListReverse[n])) 
                n += 1
                
        np.save("axisLength",self.x_axisLength) #Save for other python file plot
        np.save("x_axis",self.x_axis)
        np.save("y_axis",self.y_axis)
        
        
    def PlotDistance(self,pdbList):
        plt.figure(figsize=(12, 8), dpi=80)
        plt.imshow(self.matrixABC,interpolation='nearest', cmap=plt.cm.jet, aspect = 'auto',origin="lower") 
        cb = plt.colorbar()
        cb.set_label('Displacement [$\AA$]')
        plt.title("Distance between "+atomAlign+" atoms of "+pdbList+"")
        plt.xticks(self.x_axisLength,self.x_axis, rotation = 90)
        plt.yticks(self.y_axisLength,self.y_axis)
        plt.savefig("matrix_"+pdbList+".png")    

    
    def DifferenceMatrix(self,pdbList):
        self.__init__(self)
        self.ReadPDP(pdbList[0])
        self.FindCoordinates()
        self.Matrix(pdbList)
        matrix0 = self.matrixABC
                
        self.__init__(self)
        self.ReadPDP(pdbList[1])
        self.FindCoordinates()
        self.Matrix(pdbList)
        matrix1 = self.matrixABC
        
        self.matrixABC = abs(np.array(matrix0)) - abs(np.array(matrix1))
        
        #Write matrix to data file:
        np.save("Matrix_Delta",self.matrixABC)
        f = open("Matrix_Delta_"+pdbList[0]+"_"+pdbList[1]+".dat",'w')        
        f.write(str(self.matrixABC))
        f.close()
        
        
        self.Ticks()
        plt.figure(figsize=(12, 8), dpi=80)
        plt.imshow(self.matrixABC,interpolation='nearest', cmap=plt.cm.jet, aspect = 'auto',origin="lower") 
        cb = plt.colorbar()
        cb.set_label('Displacement [$\AA$]')
        plt.title("Displacement between "+atomAlign+" in 2ABH and 1OIB")
        plt.xticks(self.x_axisLength,self.x_axis, rotation = 90)
        plt.yticks(self.y_axisLength,self.y_axis)
        plt.savefig("matrix_difference.png")
      
    
def main():  
    for name in pdbList:
        MD = MatrixDistance(pdbList)    
        MD.ReadPDP(""+str(name)+"")
        MD.FindCoordinates()
        MD.CalcDistance(""+str(name)+"")
        MD.Matrix(""+str(name)+"")
        MD.Ticks()
        MD.PlotDistance(""+str(name)+"")
        
#        os.system("python2.7 MatrixPlot.py -i "+str(name)+"")    
        
    matrix = MatrixDistance(pdbList)
    matrix.DifferenceMatrix(pdbList)
    
#    os.system("python2.7 MatrixPlot.py -i "+plot+"")    
    
if __name__ == '__main__': main()


def cpptrajDistance():
    listA, listB, listC = [], [], []
    for i in range(220,231):
        listA.append(i)
    
    for i in range(297,307):
        listB.append(i)
        
    for i in range(268,291):
        listC.append(i)
        
    
    for name in pdbList:
        f = open("ResidueDistance_"+name+".traj",'w')
        f.write("trajin "+name+"_sequence.pdb 1 1 1 \n")
        for i in listA:
            for j in listB:
                f.write("distance "+str(i)+"_to_"+str(j)+" :"+str(i)+"@CA :"+str(j)+"@CA out data/distance_"+name+".dat \n")
            for k in listC:
                f.write("distance "+str(i)+"_to_"+str(k)+" :"+str(i)+"@CA :"+str(k)+"@CA out data/distance_"+name+".dat \n")
        f.close()
    
        os.system("cpptraj -i ResidueDistance_"+name+".traj -p "+name+"_nowat.prmtop ")