# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 11:37:27 2016

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
        
def main():
    makePlot = Plot(root)
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

    os.chdir(""+home+"")     
    
if __name__ == '__main__': main()