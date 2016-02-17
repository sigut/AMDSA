# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 11:14:13 2016

@author: sigurd
"""

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

files = ["trans","PBP_P","cis","PBP"]

#hier_files = []



class CombinedPlot():
    def __init__(self):
        self.x = 0
        self.y = 0
        
#    def find_files(self,absdir):
        

    def read_datafile(self,files):
        self.x = [0]*len(files)        
        self.y = [0]*len(files)
        n = 0
        for i in files:
            n+=1
            data = open(""+files+".dat", "r")
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
                self.x[n] = xv
                self.y[n] = yv
                
                

    def combined_histplot(self,files):
        plt.figure(figsize=(12, 6))   
        binwidth = 0.1
        color = ["dodgerblue","b","r","g"]
        
        # the histogram of the data
        for i in range(0,len(files)):        
            i = plt.hist(self.y[i], normed=1,color=color[i],bins=np.arange(min(self.y), max(self.y) + binwidth, binwidth))
        

#        plt.hist(self.y,fit,normed=1,bins=np.arange(min(self.y), max(self.y) + binwidth, binwidth),color=color)
        plt.xlabel(u"Distance [Å]")
        plt.ylabel(u"Probability")
#        title = "$\mathrm{Histogram\ of: \ "+files+"}$"
#        title = title.replace('_', '\_')
#        plt.title(r""+title+"$\ \ \mu=%.3f,\ \sigma=%.3f$" %(mu, sigma))
        plt.savefig("combined_hist.png")
        plt.clf()
            
            
            
def main():
#    Enter the root directory
    files = ["trans","PBP_P","cis","PBP"]
    
    makePlot = CombinedPlot()
    makePlot.read_datafile()
    makePlot.combined_histplot()
    
  
    
if __name__ == '__main__': main()