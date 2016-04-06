# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-


import os,sys,string
import argparse
import matplotlib
matplotlib.use('Agg')

def isLower(ch):
    return string.find(string.lowercase, ch) != -1
import matplotlib.pyplot as plt
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
#from .lib.variables import *

class CombinedPlot():
    def __init__(self):
        self.fontsize = 20

    def read_datafile(self,files):
        print files
        self.x = [0]*len(files)
        self.y = [0]*len(files)
        
        n = 0
        for i in files:
            data = open(""+str(i)+".dat", "r")
            lines = data.readlines()[1:40000]
            data.close()
            x = []
            y = []
            
            for line in lines:
                p = line.split()
                x.append(float(p[0]))
                y.append(float(p[1]))
                xv = np.array(x)
                yv = np.array(y)
                self.x[n] = xv*0.002
                self.y[n] = yv
            print np.average(y)
            
            n+=1
            
            
    def combined_rmsdplot(self,files):
        color = ["darkblue","g","g","darkmagenta","0.75","blue","violet","lavender","darkorchid"]        
        plt.figure(figsize=(12, 6))
        for i in range(0,len(files)):
#            CombinedPlot.read_datafile(""+str(i)+"")                    
            ax = plt.subplot()
            ax.plot(self.x[i], self.y[i],color = color[i],label=[""+str(files[i])+""],alpha=0.5)
        ax.set_xlabel(u"Time [ns]",fontsize = self.fontsize )
        ax.set_ylabel(u"RMSD [Å]",fontsize = self.fontsize)
    #        ax.set_xlim(min(self.x[i]), max(self.x))
    #        ax.set_ylim(min(self.y[i]), max(self.y))
        ax.xaxis.set_tick_params(labelsize=self.fontsize)
        ax.yaxis.set_tick_params(labelsize=self.fontsize)
        plt.savefig("combined_rmsd.png",bbox_inches='tight')
        plt.clf()
                

    def combined_histplot(self,files):
        
        plt.figure(figsize=(12, 6))   
        binwidth = 0.1
        color = ["r","0.75","violet","r","0.75","darkblue","0.75","blue","violet","lavender","darkorchid"]
        
        # the histogram of the data
        print "Beginnning plot"
        for i in range(0,len(files)):                    
            plt.hist(self.y[i], normed=1,color=color[i],bins=np.arange(min(self.y[i]), max(self.y[i]) + binwidth, binwidth),label=[""+str(files[i].split("/")[-1])+""],alpha=0.5)

#        plt.hist(self.y,fit,normed=1,bins=np.arange(min(self.y), max(self.y) + binwidth, binwidth),color=color)
        plt.xlabel(u"Distance between S1-S2 [Å]",fontsize = self.fontsize)
        plt.ylabel(u"Probability",fontsize = self.fontsize)
        ax = plt.subplot()
        ax.xaxis.set_tick_params(labelsize=self.fontsize)
        ax.yaxis.set_tick_params(labelsize=self.fontsize)
        plt.tick_params(labelsize=14)
#        title = "$\mathrm{Histogram\ of: \ "+files+"}$"
#        title = title.replace('_', '\_')
#        plt.title(r""+title+"$\ \ \mu=%.3f,\ \sigma=%.3f$" %(mu, sigma))
        plt.legend(loc=2)
        plt.savefig(""+absdir+"/plots/1IXH_"+Mutation1+"_"+Mutation2+".png",bbox_inches='tight')
        plt.savefig("/SCRATCH/sigut/phd/PBP_simulations/Mutations/plots/1IXH_"+Mutation1+"_"+Mutation2+".png",bbox_inches='tight')
        plt.clf()
            
            
            
def main():
#    Enter the root directory
    files = ["/SCRATCH/sigut/phd/PBP_simulations/Azobenzene/QM_cis_2/data/distance_S_S1",
             "/SCRATCH/sigut/phd/PBP_simulations/Azobenzene/QM_cis_2/data/distance_C_C15",
             ""+absdir+"/data/distance_"+Mutation1+"_"+Mutation2+"",
             "/SCRATCH/sigut/phd/PBP_simulations/Azobenzene/QM_trans_2/data/distance_S_S1",
             "/SCRATCH/sigut/phd/PBP_simulations/Azobenzene/QM_trans_2/data/distance_C_C15",
             ""+absdir+"_inP/data/distance_"+Mutation1+"_"+Mutation2+""]
    #["QM_trans","distance_226_298_P","distance_226_299_P","QM_cis","distance_226_298_open","distance_226_299_open"]
#    files = ["rmsd_226_298","rmsd_226_298_P"]
    
    makePlot = CombinedPlot()
    makePlot.read_datafile(files)
    makePlot.combined_histplot(files)
#    makePlot.combined_rmsdplot(files)
#    makePlot.write_file(files)
  
    
if __name__ == '__main__': main()