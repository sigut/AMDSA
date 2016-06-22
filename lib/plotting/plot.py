# -*- coding: utf-8 -*-


import math,os,sys,getopt, string
import argparse
import matplotlib
matplotlib.use('Agg')
from matplotlib.ticker import MaxNLocator # added 
from matplotlib.backends.backend_pdf import PdfPages

def isLower(ch):
    return string.find(string.lowercase, ch) != -1
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.mlab as mlab
import numpy as np
import inspect

the_list = ["lib","lib/plotting"]
for folders in the_list:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],str(folders))))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
      
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from variables import * 

#Create plots folder if it doesn't exist
if not os.path.exists(""+root+"/plots"):
    os.makedirs(""+root+"/plots")

class Plot():
    def __init__(self,root):
        self.figsizeX, self.figsizeY = int(figSizeX), int(figSizeY)
        self.x = 0
        self.y = 0
        self.t = 0
        self.pc1 = 0
        self.pc2 = 0
        self.pc3 = 0
        self.colors = ['b','g','r','k','m','y','c','DarkBlue','LightGreen','DarkOrange','0.75','0.5','0.25','0.25','0.25','0.25','0.25','0.25','0.25','0.25','0.25','0.25','0.25','0.25','0.25','0.25','0.25','0.25']
        
#    def find_files(self,absdir):
        

    def read_datafile(self,files):
        data = open("data/"+files+".dat", "r")
        lines = data.readlines()[1:]
        data.close()
        x = []
        y = []
        for line in lines:
            p = line.split()
            x.append(float(p[0]))
            y.append(float(p[1]))
            xv = np.array(x)
            yv = np.array(y)
            self.x = xv
            self.y = yv
            
    def plot_datafile(self,files): # Plot for plotting the chosen files (rmsd, distance, etc)
        plt.figure(figsize=(self.figsizeX, self.figsizeY))        
        ax = plt.subplot()
        ax.plot(self.x, self.y)
        ax.set_xlabel(u"Frame")
        ax.set_ylabel(u"Rmsd [Å]")
        ax.set_xlim(min(self.x), max(self.x))
        ax.set_ylim(min(self.y), max(self.y))
        plt.savefig("plots/"+files+".png")
        plt.close()
        
    def plot_histplot(self,files):
        # best fit of data
        (mu, sigma) = norm.fit(self.y)        
        print "mu and sigma: "+str(mu)+", "+str(sigma)+""
        #Make the hist plot
        plt.figure(figsize=(12, 6))   
        binwidth = 0.1
        color = "dodgerblue"
        
        # the histogram of the data
        n, bins, patches = plt.hist(self.y, normed=1,color=color,bins=np.arange(min(self.y), max(self.y) + binwidth, binwidth))        #
        
        # add a 'best fit' line
        fit = mlab.normpdf( bins, mu, sigma)
        l = plt.plot(bins, fit, 'b--', linewidth=2)

        plt.xlabel(u"Distance [Å]")
        plt.ylabel(u"Probability")
        title = "$\mathrm{Histogram\ of: \ "+files+"}$"
        title = title.replace('_', '\_')
        plt.title(r""+title+"$\ \ \mu=%.3f,\ \sigma=%.3f$" %(mu, sigma))
        plt.savefig("plots/"+files+"_hist.png")
        plt.close()
        
        
    def label_clusters(self,cluster_files): #Plot for making rmsd colored according to the cluster
        data = open("data/"+cluster_files+".txt", "r")
        lines = data.readlines()[1:]
        data.close()
        y_c = []
        for line in lines:
            p = line.split()
            y_c.append(float(p[1]))
            yv = np.array(y_c)
        clusters = max(yv)
        self.number = int(clusters)+1
        
        #Write out what each frame corresponds to in clusters
        self.x_s = [0]*self.number
        for i in range(0,self.number):
            self.x_s[i] = []
            
        # Write out the cluster x-numbers for each cluster 
        for i,j in enumerate(yv):
            self.x_s[int(j)].append(i)
        
        if PCA == "on":             
            # Define the y-rms values for each cluster       
            self.y_rmsd = [0]*self.number
            self.y_pc1 = [0]*self.number
            self.y_pc2 = [0]*self.number
            for i in xrange(self.number):
                self.y_rmsd[i] = []
                self.y_rmsd[i] = self.y[self.x_s[i]]
                self.y_pc1[i] = []
                self.y_pc1[i] = self.pc1[self.x_s[i]]
                self.y_pc2[i] = []
                self.y_pc2[i] = self.pc2[self.x_s[i]]
            
            
    def plot_clusters(self,cluster_files):
        plt.figure(figsize=(self.figsizeX, self.figsizeY))
        ax = plt.gca()
        size = 2.0
        for i in range(0,self.number):
            ax.scatter(self.x_s[i], self.y_rmsd[i], label ="cluster "+str(i), color = self.colors[i], s= size)
        ax.set_xlim([0,max(self.x)]) 
        ax.set_ylim([0,max(self.y)])
        ax.set_xlabel('Frame Number')
        ax.set_ylabel('RMSd [$\AA$]')
        ax.legend(loc='lower center',ncol=5, bbox_to_anchor=(0.5,0))
        plt.savefig("plots/"+cluster_files+".png")
        plt.close()
        
    def read_pca(self):
        pcaFiles = ""+absdir+"/data/pca/pca-ca"
        data = open(""+pcaFiles+".dat", "r")
        lines = data.readlines()[1:]
        data.close()
        
        time = []
        mode1= []
        mode2= []
        mode3= []
        for line in lines:
            p = line.split()
            time.append(float(p[0]))
            mode1.append(float(p[1]))
            mode2.append(float(p[2]))
            mode3.append(float(p[3]))
            t = np.array(time)
            PC1 = np.array(mode1)
            PC2 = np.array(mode2)
            PC3 = np.array(mode3)
            self.frame = t
            self.pc1 = PC1
            self.pc2 = PC2
            self.pc3 = PC3
            
    def pcaSCREE(self):
        
        eigenValue = []
        eigenNumber = []
        n = 0
        with open('data/pca/evecs-ca.dat') as f:
            for line in f:
                nextLine = next(f)
                if "****" == line.strip():
                    line = nextLine.split()
                    eigenNumber.append(int(line[0]))
                    eigenValue.append(float(line[1])) 
        
        plt.figure(figsize=(self.figsizeX, self.figsizeY))
        ax = plt.gca()
        plt.scatter(eigenNumber, eigenValue, color = 'b')
        ax.set_xlabel('Eigenvalue number')
        ax.set_ylabel('Eigenvalue')
        plt.savefig("plots/ScreePlot.png")
        plt.close()
        
        
    def plot_pca(self):
        color = self.frame/len(self.frame)
        plt.figure(figsize=(self.figsizeX, self.figsizeY))
        ax = plt.gca()
        plt.scatter(self.pc1, self.pc2, c=color)
        cb = plt.colorbar()
        cb.set_label('Frame')
        ax.set_xlabel('PC1')
        ax.set_ylabel('PC2')
        plt.savefig("plots/pca12_timelapse.png")
        plt.close()
               
        #######################################################################################    
               
        from scipy.stats import gaussian_kde
        xy = np.vstack([self.pc1,self.pc2])
        z = gaussian_kde(xy)(xy)       
        # Sort the points by density, so that the densest points are plotted last
        idx = z.argsort()
        self.pc1, self.pc2, z = self.pc1[idx], self.pc2[idx], z[idx]

        plt.figure(figsize=(self.figsizeX, self.figsizeY))
        ax = plt.gca()
        plt.scatter(self.pc1, self.pc2, c=z, s=50, edgecolor='')
        cb = plt.colorbar()
        cb.set_label('Distribution')
        ax.set_xlabel('PC1')
        ax.set_ylabel('PC2')
        plt.savefig("plots/pca12_gaussian.png")  
        plt.close()

        #######################################################################################

        plt.figure(figsize=(self.figsizeX, self.figsizeY))
        plt.hist2d(self.pc1, self.pc2, (100, 100), cmap=plt.cm.jet)
        ax = plt.gca()
        cb = plt.colorbar()
        cb.set_label('Occurances')
        ax.set_xlabel('PC1')
        ax.set_ylabel('PC2')
        plt.savefig("plots/pca12_hist.png") 
        plt.close()
        
        #######################################################################################        
#        #Create arrays specifying the bin edges
#        nbins = 10
#        xmin, xmax  =  min(self.pc1), max(self.pc1)
#        ymin, ymax =  min(self.pc2), max(self.pc2)
#        xbins = np.linspace(min(self.pc1), max(self.pc1), nbins)
#        ybins = np.linspace(min(self.pc2), max(self.pc2), nbins)
#        
#        plt.figure(figsize=(self.figsizeX, self.figsizeY))
#        data, _, _ = np.histogram2d(self.pc1, self.pc2, bins=(xbins, ybins))
#        plt.imshow(data.T, origin='lower', extent=[xmin, xmax, ymin, ymax])
#        matplotlib.cm.jet
#        plt.colorbar()
#        ax.axis([xmin-5, xmax+5, ymin-5, ymax-5])   
#        plt.savefig("plots/pca12_blue.png")
#        plt.close()
   
    def plot_pcaCluster(self,cluster_files):
        plt.figure(figsize=(self.figsizeX, self.figsizeY))
        ax = plt.gca()
        size = 2.0
        for i in range(0,self.number):
            ax.scatter(self.y_pc1[i], self.y_pc2[i], label ="cluster "+str(i), color = self.colors[i], s= size)
        ax.set_xlabel('PC1')
        ax.set_ylabel('PC2')
        ax.legend(loc='lower center',ncol=5, bbox_to_anchor=(0.5,0))
        plt.savefig("plots/pca12_"+cluster_files+".png")
        plt.close()
        
def main():
    makePlot = Plot(root)
    cluster_files = ["cluster_hier_out","cluster_dbscan_out"]
    files = []
    print absdir
    for file in os.listdir(""+absdir+"/data/"):
        if file.endswith(".dat"):
            temp = os.path.splitext(file)[0]
            print temp
            files.append(temp)
    
    if not os.path.exists(""+root+"/plots"):
        os.mkdir(""+root+"/plots")
    os.chdir(""+root+"")         

    for i in files: #loop through the files (rmsd, distance...) and make the data-analysis and plot.
        if os.path.exists("data/"+str(i)+".dat") == True:
            makePlot.read_datafile(""+str(i)+"")
            print "read datafile "+str(i)+""
            makePlot.plot_datafile(""+str(i)+"")
            
            print "Making hist plot"
            makePlot.plot_histplot(""+str(i)+"")
            print "plotting datafile "+str(i)+""
        else: 
            print "Warning --- "+str(i)+" does not exist. Cannot make plot"

    
    if PCAPlot == "on":
        makePlot.read_pca()
        makePlot.pcaSCREE()
        makePlot.plot_pca()
        
    if clusterAnalysis == "on":
        for j in cluster_files: # Loop through the different cluster_*_out files to make the colour cluster rmsd plot
            if os.path.exists("data/"+str(j)+".txt") == True:
                makePlot.read_datafile("rmsd")  #Read the rmsd file
                print "read datafile "+str(j)+".dat"
                makePlot.label_clusters(""+str(j)+"")
                print "plotting datafile "+str(j)+".txt"
                makePlot.plot_clusters(""+str(j)+"")
                if PCAPlot == "on":
                    makePlot.plot_pcaCluster(""+str(j)+"")
            else: 
                print "Warning --- "+str(j)+".txt does not exist. Cannot make rmsd-cluster colored plot"
    
    os.chdir(""+home+"")     
    
if __name__ == '__main__': main()