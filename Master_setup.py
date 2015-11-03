# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 17:09:03 2015

@author: sigut
"""

# This is the master script for setup of MD/QM simulations with PBPs. Currently it calls <3> scripts: 
#   1) SetupLeap.py that sets up the prmtop, inpcrd and pdb files.  
#   2) SetupInfiles that creates the in files for the simulation
#   3) SetupSubmit that creates the submit.sh file that specifies the simulation submission parameters such as number of cores, gpu usage and so on. 
#   All the scripts above uses the variables defined in the config.cfg file in the root folder.

####-----------------------------------------------#####
# Usage: python R_analysis.py -i <inputdir> -p <protein>
####-----------------------------------------------#####

# Variables are loaded from the file src/variables.py. Any new variable must be entered in this file. The variables.py also calls the config.py file that specifies more rigid/fixed simulation variables for the setup and submit environment.

import sys,inspect
import os

# The two following functions adds subfolders to the python-path and allows import of the modules into this program
# use this if you want to include modules from a subfolder
the_list = ["src","src/setup"]
for folders in the_list:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],str(folders))))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)

from variables import *
import SetupInfiles, SetupLeap, SetupSubmit, CalcIonPos

def main():
    if not os.path.exists(""+root+""):
        os.mkdir(""+root+"")    
    
    os.chdir(""+root+"")
    # Make necessary folders
    if not os.path.exists("in_files"):
        os.mkdir("in_files")
    if not os.path.exists("md_files"):
        os.mkdir("md_files")
    if not os.path.exists("logs"):
        os.mkdir("logs")
    if not os.path.exists("resultsDir"):
        os.mkdir("resultsDir")
    if not os.path.exists("pdb_files"):
        os.mkdir("pdb_files")
          
    os.chdir(""+home+"") #Return home because the other script automatically enter the folder
    
    # Define the constructor and the method
    if iamd == "3": # iamd is specified in the config file. If specified it will be taken care of in the setupInfiles module
        Setup = SetupInfiles.main()
        MakeSubmissionFile = SetupSubmit.main()
    else:
#        if insertAnion == "HPO4":
#            Calc = CalcIonPos.main()
        Runleap = SetupLeap.main()
        Setup = SetupInfiles.main()
        MakeSubmissionFile = SetupSubmit.main()
if __name__ == '__main__': main()
