## Commands 

 
# Clear all 

rm(list=ls()) 

# Load bio3d Library 

library(bio3d) 

setup.ncore(8) 

# Location of PDB files 

id_pdb =   c("/home/sigurd/Dropbox/AMDSA/pbpu_test/pbpu_1/in_files/pbpu_sequence.pdb") 

# Location of mdcrd files 

folderNames =   c("/home/sigurd/Dropbox/AMDSA/pbpu_test/pbpu_1/resultsDir/") 

# Trajectory file names 

id_dcd =   c("mergedResult_strip.dcd") 
