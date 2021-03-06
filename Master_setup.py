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
# Usage: python R_analysis.py -i <inputdir> -p <protein> -m1 <mutation1> -m2 <mutation2>
####-----------------------------------------------#####

# Variables are loaded from the file lib/variables.py. Any new variable must be entered in this file. The variables.py also calls the config.py file that specifies more rigid/fixed simulation variables for the setup and submit environment.

import sys,inspect
import os

# The two following functions adds subfolders to the python-path and allows import of the modules into this program
# use this if you want to include modules from a subfolder
the_list = ["lib","lib/setup"] #put the path into the config file, and pull the config file down into the specific folder (and copy the config file into the folder for debugging purposes)
for folders in the_list:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],str(folders))))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
from variables import *
import SetupInfiles, SetupLeap, SetupSubmit, CalcIonPos, Mutations, Crosslinker, RotateIonPos


class CreateFolders():
#    def __init__():
#        from variables import *
    def create_folder(self,root):
            # Make necessary folders
            if not os.path.exists(""+root+""):
                os.mkdir(""+root+"")    
            if not os.path.exists(""+root+"/in_files"):
                os.mkdir(""+root+"/in_files")
            if not os.path.exists(""+root+"/md_files"):
                os.mkdir(""+root+"/md_files")
            if not os.path.exists(""+root+"/logs"):
                os.mkdir(""+root+"/logs")
            if not os.path.exists(""+root+"/resultsDir"):
                os.mkdir(""+root+"/resultsDir")
            if not os.path.exists(""+root+"/pdb_files"):
                os.mkdir(""+root+"/pdb_files")
            if not os.path.exists(""+root+"/data"):
                os.mkdir(""+root+"/data")
            if not os.path.exists(""+root+"/submissionScripts"):
                os.mkdir(""+root+"/submissionScripts")
                
    def warning(Self,root):   
        if sMD == "on" and method == "aMD":
            var = raw_input("Both aMD and sMD is specified - this is not advised. Press 'y' to continue and 'n' to discontinue")
            if var == 'n':
                raise Exception('You opted not to continue with aMD and sMD simulations')
            if var == 'y':
                pass
            
    def check_folder(self,root):
        if os.path.isdir(""+str(root)+"") == True:
            print "Trying to create the folder "+root+""
            var = raw_input("This will overwrite any previous parameter files in the "+root+" folder. Confirm with any key press. Press 'n' to discontinue ")
            if var == 'n':
                raise Exception('You opted not to overwrite in the '+root+' folder')
            if var == 'y':    
                CreateFolders.create_folder(self,root)
        else:
            print "Creating new folder"
            CreateFolders.create_folder(self,root)
          

        
        
        
def main():
    if aMD == "on": # iamd is specified in the config file. If specified it will be taken care of in the setupInfiles module
        Setup = SetupInfiles.main()
        MakeSubmissionFile = SetupSubmit.main()
        
    elif sMD == "on" and newSim == "off": #If continuing another simulation with sMD then make only the setup and submission files
        Setup = SetupInfiles.main()
        MakeSubmissionFile = SetupSubmit.main()

    else:
        CheckFolder = CreateFolders()
        CheckFolder.warning(root)
        CheckFolder.check_folder(root)        
        if MakeMutations == "on":
            RunMutations = Mutations.main()
        if insertAnion == "on" and insertProtein == "on":
            Calc = CalcIonPos.main()
            if rotation == "on":
                Rot = RotateIonPos.main()
        Runleap = SetupLeap.main() #Create the parameter topology files
        Setup = SetupInfiles.main()
        MakeSubmissionFile = SetupSubmit.main()
    os.system("cp configSetup.cfg "+root+"/") # copy the cfg file into the folder for debugging
    print ""
    print "\"May the Force(Field) be with you\""
    
if __name__ == '__main__': main()
