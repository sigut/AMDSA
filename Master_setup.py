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

#class Check_folder():
#    def __init__(self):
#        self.prmtop_list = []
#        
#    def find_prmtop(self,root):
#        for file in os.listdir(""+root+"/in_files/"):
#           if file.endswith(".prmtop"):
#               self.prmtop_list.append(file)
#        print self.prmtop_list
#        return self.prmtop_list
#    
#    
#    def ask_user(self):
##        def ask_ok(prompt, retries=4, complaint='Yes or no, please!'):
#        
#        print 'These files already exist in the in_files folder'
#        print self.prmtop_list
#        while True:
##            try:
#            answer = str(raw_input("Do you wish to replace them? "))
#            if answer in ('y', 'ye', 'yes'):
#                print("Overwriting existing files!")
#                return True
#                return answer
##                break
#            if answer in ('n', 'no', 'nop', 'nope'):
#                return False
#                return answer
##                break
##             if retries < 0:
##            raise IOError('refusenik user')
##        print complaint
##        ok = raw_input(prompt)
##        if ok in ('y', 'ye', 'yes'):
##            return True
##        if ok in ('n', 'no', 'nop', 'nope'):
##            return False
        
def main():
#    check = Check_folder()
#    check.find_prmtop(root)
#    check.ask_user()
    
#    if answer == "y":
            
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
#        else:
        if insertAnion == "on":
            Calc = CalcIonPos.main()
        Runleap = SetupLeap.main()
        Setup = SetupInfiles.main()
        MakeSubmissionFile = SetupSubmit.main()
#    else:
#        print 'Aborting'
if __name__ == '__main__': main()
