#this file needs to be updated

# AMDSA

#Automated Molecular Dynammics Setup and Analysis is a modular program created in Python that creates the necessary files for running MD simulations in Amber. Therefore is it required to have a working version of Amber Installed. This program uses Amber14 and AmberTools15. Amber consists of many different tools that must be run through the commandline in order to run. All of these steps are run through the AMDSA program. 

#Through commandline arguments and configuration files, a simulation can be setup in a specific folder for a desired simulation type.

#The program is under constant development, so be aware of minor/major changes between different commits.

#Currently the program for setting up simulations is run through the Master_setup.py script that calls all the necessary modules in the library. The program is run by typing:

#python Master_setup.py -i <input_directory> -p <protein_name>

#If the folder is not already existing, the program will create it. The protein name is currently limited to pbpu and pbpv - but more proteins will be implemented later. 

#The configuration file - config.cfg, specifies more advanced settings for the simulation. A more detailed understanding of the variables should be known prior to changing certain variables - Ask Sigurd Friis Truelsen for help. A detailed description of the config file will be added later.

#The analysis is run through the Master_analysis.py script by

#python Master_analysis.py -i <input_directory> -p <protein_name> -q qsub -n nomerge

#Where -q and -n are optional command-line arguments. The -q specifies if the analysis should be performed on the hpc system, and the -n specifies if the trajectory files created should NOT be merged into a mergedResult.dcd file. When running this script the Ambertools cpptraj runs a trajectory analysis, and python modules will plot the data. An "R" script is also implemented, however currently outcommented as this is very memory consuming and requires specific nodes on the hpc system in order to avoid swapping. An update of this will be add soon.

