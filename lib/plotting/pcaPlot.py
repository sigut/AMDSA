# -*- coding: utf-8 -*-
"""
Created on Sun May  8 19:00:15 2016

@author: sigurd
"""
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
        self.x = 0
        self.y = 0
        self.t = 0
        self.pc1 = 0
        self.pc2 = 0
        self.pc3 = 0
def pcaPlot(self):
#        read_datafile 
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
        color = self.frame/len(self.frame)

        plt.figure(figsize=(12, 6))
        ax = plt.gca()
        plt.scatter(self.pc1, self.pc2, c=color)
        cb = plt.colorbar()
        cb.set_label('Frame')
        ax.set_xlabel('PC1')
        ax.set_ylabel('PC2')
        plt.savefig("plots/pca12_timelapse.png")
        plt.show()        
        plt.clf()
        
        heatmap, xedges, yedges = np.histogram2d(self.pc1, self.pc2, bins=10)
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        print xedges[0]
        cmap = matplotlib.cm.jet
        cmap.set_bad(color='white', alpha=None)
        plt.imshow(heatmap, extent=extent)        
        cb = plt.colorbar()
        cb.set_label('Occurances')
        ax.set_xlabel('PC1')
        ax.set_ylabel('PC2')
        plt.savefig("plots/pca12_heatmap.png")
        plt.show()
    def pcaClusterPlot(self):
        pass