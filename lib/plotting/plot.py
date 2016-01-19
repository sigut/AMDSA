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
import numpy as np
import inspect

the_list = ["lib","lib/plotting"]
for folders in the_list:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],str(folders))))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)

#from variables import *

#Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--idir',
                    help = 'input directory of the simulation' )
parser.add_argument('-p', '--protein',
                    help = 'Protein specification, the current options are: pbpv, pbpu')
parser.add_argument('-q','--qsub',
                    help='if -q qsub is specified the setup or analysis will be submitted directly to the hpc-queue')
parser.add_argument('-n','--nomerge',
                    help='if -n nomerge is specified the cpptraj will not merge the mdcrd files into the dcd file')
                    
args = parser.parse_args()

#Command-line Variables:
root  = args.idir
protein = args.protein
qsub = args.qsub
nomerge = args.nomerge
# Directory Variables:
home = os.getcwd() #Specify the root directory
absdir = os.path.abspath(""+root+"")
absdir_home = os.path.abspath(""+home+"")
name = os.path.basename(os.path.normpath(""+absdir+""))
directory = "./lib/analysis/"

#Define the files to plot:

#files = ["rmsd","distance_226_297", "distance_10_147","distance_10_63","distance_disulfur1","distance_disulfur2"]
cluster_files = ["cluster_hier_out","cluster_dbscan_out"]
files = []

for file in os.listdir(""+absdir+"/data/"):
    if file.endswith(".dat"):
        files.append(file)


#Create plots folder if it doesn't exist
if not os.path.exists(""+root+"plots"):
    os.makedirs(""+root+"plots")

class Plot():
    def __init__(self,root,files):
        self.x = 0
        self.y = 0

    def read_datafile(self,root,files):
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
            
    def plot_datafile(self,root,files): # Plot for plotting the chosen files (rmsd, distance, etc)
        plt.figure(figsize=(12, 6))        
        ax = plt.subplot()
        ax.plot(self.x, self.y)
        ax.set_xlabel(u"Frame")
        ax.set_ylabel(u"Rmsd [Å]")
        ax.set_xlim(min(self.x), max(self.x))
        ax.set_ylim(min(self.y), max(self.y))
        plt.savefig("plots/"+files+".png")
        plt.clf()
        
    def cluster_label(self,root,cluster_files): #Plot for making rmsd colored according to the cluster
        data = open("data/"+cluster_files+".dat", "r")
        lines = data.readlines()[1:]
        data.close()
        y_c = []
        for line in lines:
            p = line.split()
            y_c.append(float(p[1]))
            yv = np.array(y_c)
        clusters = max(yv)
        number = int(clusters)+1
        
        #Write out what each frame corresponds to in clusters
        x_s = [0]*number
        for i in range(0,number):
            x_s[i] = []
            
        # Write out the cluster x-numbers for each cluster 
        for i,j in enumerate(yv):
            x_s[int(j)].append(i)
                     
        # Define the y-rms values for each cluster       
        y_s = [0]*number
        for i in xrange(number):
            y_s[i] = []
            y_s[i] = self.y[x_s[i]]
        
        colors = ['b','g','r','k','m','y','c','DarkBlue','LightGreen','DarkOrange','0.75','0.5','0.25','0.25','0.25','0.25','0.25','0.25','0.25','0.25','0.25','0.25','0.25','0.25','0.25','0.25','0.25','0.25']
        plt.figure(figsize=(12, 6))
        ax = plt.gca()
        size = 2.0
        for i in range(0,number):
            ax.scatter(x_s[i], y_s[i], label ="cluster "+str(i), color = colors[i], s= size)
        
        ax.set_xlim([0,max(self.x)]) 
        ax.set_ylim([0,max(self.y)])
        ax.set_xlabel('Frame Number')
        ax.set_ylabel('RMSd [$\AA$]')
        ax.legend(loc='lower center',ncol=5, bbox_to_anchor=(0.5,0))
        plt.savefig("plots/"+cluster_files+".png")
        plt.clf()
        
def main():
#    Enter the root directory
    os.chdir(""+root+"")         
    makePlot = Plot(root,files)
    
    for i in files: #loop through the files (rmsd, distance...) and make the data-analysis and plot.
        if os.path.exists("data/"+str(i)+".dat") == True:
            makePlot.read_datafile(root,""+str(i)+"")
            print "read datafile "+str(i)+""
            makePlot.plot_datafile(root,""+str(i)+"")
            print "plotting datafile "+str(i)+""
        else: 
            print "Warning --- "+str(i)+".dat does not exist. Cannot make plot"
        
    for j in cluster_files: # Loop through the different cluster_*_out files to make the colour cluster rmsd plot
        if os.path.exists("data/"+str(j)+".dat") == True:
            makePlot.read_datafile(root,"rmsd")  #Read the rmsd file
            print "read datafile "+str(j)+""
            makePlot.cluster_label(root,""+str(j)+"")
            print "plotting datafile "+str(j)+""
        else: 
            print "Warning --- "+str(j)+".dat does not exist. Cannot make rmsd-cluster colored plot"
                
    os.chdir(""+home+"")     
    
if __name__ == '__main__': main()