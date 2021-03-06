# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 13:40:12 2015

@author: sigurd
"""
# This script writes the submit.sh file for submission to the hpc cluster.
# It takes the variables from variables.py (from command line and config.cfg file)
# In the config.cfg it is specified whether to use CUDA/sander and aMD/cMD.

import os, sys,inspect

the_list = ["lib","lib/setup"]
for folders in the_list:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],str(folders))))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)

from variables import *

class Create_Submit():

    def __init__(self):
    
        self.list = ["hpc","memento"]
        self.compilerList = ["pmemd","cuda","sander"]
        
    def makeSubmitFile(self,protein,method):
        for queue in self.list:
            for self.compiler in self.compilerList:
                if self.compiler == "pmemd":
                    self.CALCULATOR = "mpirun pmemd.MPI"
                if self.compiler == "cuda":
                    self.CALCULATOR = "pmemd.cuda"
                if self.compiler == "sander":
                    self.CALCULATOR = "mpirun sander.MPI"                
                
                f = open(""+absdir+"/submissionScripts/submit_"+self.compiler+"_"+queue+".sh",'w')
                buffer = Queue(queue,name, cores, ptile )
                buffer = buffer + """
# Number of MD steps
md_steps="""+md_steps+"""

######################

# Minimize the system, step 1
echo "Minimization 1"
if [[ -e md_files/min1.rst ]]; then
    echo '-- min1.rst file exists, skipping minimization 1'
else
    echo '-- Running Minimization 1'
    """+self.CALCULATOR+""" -O -i in_files/min1.in -o logs/min1.out -p in_files/"""+protein+""".prmtop -c in_files/"""+protein+""".inpcrd -r md_files/min1.rst -ref in_files/"""+protein+""".inpcrd -x md_files/min1.mdcrd
    
    # Create pdb file for the minimized structure
    ambpdb -p in_files/"""+protein+""".prmtop < md_files/min1.rst > pdb_files/"""+protein+"""_min1.pdb
fi

######################

# Minimize the system, step 2
echo "Minimization 2"
if [[ -e md_files/min2.rst ]]; then
    echo '-- min2.rst file exists, skipping minimization 2'
else
    echo '-- Running Minimization 2'
    """+self.CALCULATOR+""" -O -i in_files/min2.in -o logs/min2.out -p in_files/"""+protein+""".prmtop -c md_files/min1.rst -r md_files/min2.rst -ref md_files/min1.rst -x md_files/min2.mdcrd
    
    # Create pdb file for the minimized structure
    ambpdb -p in_files/"""+protein+""".prmtop < md_files/min2.rst > pdb_files/"""+protein+"""_min2.pdb
fi

######################

# Minimize the system, step 3
echo "Minimization 3"
if [[ -e md_files/min3.rst ]]; then
    echo '-- min3.rst file exists, skipping minimization 3'
else
    echo '-- Running Minimization 3'
    """+self.CALCULATOR+""" -O -i in_files/min3.in -o logs/min3.out -p in_files/"""+protein+""".prmtop -c md_files/min2.rst -r md_files/min3.rst -ref md_files/min2.rst -x md_files/min3.mdcrd
    
    # Create pdb file for the minimized structure
    ambpdb -p in_files/"""+protein+""".prmtop < md_files/min3.rst > pdb_files/"""+protein+"""_min3.pdb
fi

######################

# Heating the system, step 4
echo "Heating in NVT ensemble"
if [[ -e md_files/heat1.rst ]]; then
    echo '-- heat1.rst file exists, skipping heating 1'
else
    echo '-- Running heating NVT ensemble'
    """+self.CALCULATOR+""" -O -i in_files/heat1.in -o logs/heat1.out -p in_files/"""+protein+""".prmtop -c md_files/min3.rst -r md_files/heat1.rst -ref md_files/min3.rst -x md_files/heat1.mdcrd
    
    # Create pdb file for the minimized structure
    ambpdb -p in_files/"""+protein+""".prmtop < md_files/heat1.rst > pdb_files/"""+protein+"""_heat1.pdb
fi

######################

# Heating the system, step 5
echo "Equilibrating in NPT ensemble"
if [[ -e md_files/heat2.rst ]]; then
    echo '-- heat2.rst file exists, skipping heating 2'
else
    echo '-- Running equilibration NPT ensemble'
    """+self.CALCULATOR+""" -O -i in_files/heat2.in -o logs/heat2.out -p in_files/"""+protein+""".prmtop -c md_files/heat1.rst -r md_files/heat2.rst -ref md_files/heat1.rst -x md_files/heat2.mdcrd
    
    # Create pdb file for the minimized structure
    ambpdb -p in_files/"""+protein+""".prmtop < md_files/heat2.rst > pdb_files/"""+protein+"""_heat2.pdb
fi

######################


# Equilibrate the system, step 6
echo "Equilabration NVT ensemble, step 6"
if [[ -e md_files/equil0.rst ]]; then
    echo '-- equil0.rst file exists, skipping equilibration'
elif [[ -e md_files/heat2.rst ]]; then    
    echo '-- Running Minimization 6'
    """+self.CALCULATOR+""" -O -i in_files/equil.in -o logs/equil0.out -p in_files/"""+protein+""".prmtop -c md_files/heat2.rst -r md_files/equil0.rst -x md_files/equil0.mdcrd
    
    # Create pdb file for the minimized structure
    ambpdb -p in_files/"""+protein+""".prmtop < md_files/equil0.rst > pdb_files/"""+protein+"""_equil0.pdb
    
fi

"""

                if method == "cMD":
                    buffer = buffer + """
######################      Beginning the cMD simulations           ######################      
# A function for running the cMD 
runMD(){

# define the local step nr, previous step nr, and new step nr
local cStep=$1
local pStep=$(($1-1))

# Start amber MD simulation
"""+self.CALCULATOR+""" -O -i in_files/cMD.in -o logs/md_${cStep}.log -c md_files/equil${pStep}.rst -p in_files/"""+protein+""".prmtop -r md_files/equil${cStep}.rst -x md_files/equil${cStep}.mdcrd

# Convert the resulting structure to a pdb-file
ambpdb -p in_files/"""+protein+""".prmtop < md_files/equil${cStep}.rst > pdb_files/equil${cStep}.pdb

}

# Run the MD simulations. Figure out last stop, and take "md_steps" runs from that
arr=( md_files/equil*.rst )  # * is list of all file and dir names
m=${#arr[@]}
n=$(($n-1))
echo "Molecular Dynamics"
echo "-- Number of previous MD runs: "$(($n))

startI=$n
endI=$md_steps

while [ $startI -lt $endI ]
do
    if [[ -e md_files/equil$(($startI+1)).rst ]]; then
        echo "-- #"$startI" MD already run, skipping to next"
    elif [[ -e md_files/equil$(($startI-1)).rst ]]; then
        echo "-- Running script #"$startI
        runMD $startI
    else
        echo '-- previous equil file not found, skipping equilibration #'$startI
    fi
    startI=`expr $startI + 1`
done
            """
#                f.write(buffer)
#                f.close()
            
                if sMD == "on" and newSim == "on":
                    buffer = buffer + """    
######################      Beginning the sMD simulations           ######################      
# sMD: steer the system
echo "steer NPT ensemble"

# Find the number of cMD runs and continue the sMD from that.
arr=( md_files/equil*.rst )  # * is list of all file and dir names
n=${#arr[@]}
m=$(($n-1))
echo "Molecular Dynamics"
echo "-- Number of previous MD runs: "$(($n-1))

if [[ -e md_files/sMD_0.rst ]]; then
    echo '-- sMD_0.rst file exists, proceeding to phase 1'
else
    echo '-- starting sMD phase 0'
    """+self.CALCULATOR+""" -O -i in_files/sMD_0.in -o logs/sMD_0.log -p in_files/"""+protein+""".prmtop -c md_files/equil$m.rst -r md_files/sMD_0.rst -x md_files/sMD_0.mdcrd
    
    # Create pdb file for the minimized structure
    ambpdb -p in_files/"""+protein+""".prmtop < md_files/sMD_0.rst > pdb_files/"""+protein+"""_sMD_0.pdb
    
fi

######################      Beginning the sMD equilibration         ######################                        
                        
                        
# A function for running another step of the script
runMD(){

# define the local step nr, previous step nr, and new step nr
local cStep=$1
local pStep=$(($1-1))

#Move the RST file to avoid it being overwritten!
mv data/dist.sMD.RST data/dist.sMD_${pstep}.RST

# Start amber MD simulation
"""+self.CALCULATOR+""" -O -i in_files/sMD_equil.in -o logs/sMD_${cStep}.log -c md_files/sMD_${pStep}.rst -p in_files/"""+protein+""".prmtop -r md_files/sMD_${cStep}.rst -x md_files/sMD_${cStep}.mdcrd

# Convert the resulting structure to a pdb-file
ambpdb -p in_files/"""+protein+""".prmtop < md_files/sMD_${cStep}.rst > pdb_files/sMD_${cStep}.pdb

}

# Run the MD simulations. Figure out last stop, and take "md_steps" runs from that
arr=( md_files/sMD_*.rst )  # * is list of all file and dir names
m=${#arr[@]}
n=$(($n-1))
echo "Molecular Dynamics"
echo "-- Number of previous sMD runs: "$(($n))

NumberOfsMDruns = """+NumberOfsMDRuns+"""

startI=$n
endI=$(($NumberOfsMDRuns))

while [ $startI -lt $endI ]
do
    if [[ -e md_files/sMD_$(($startI+1)).rst ]]; then
        echo "-- #"$startI" sMD already run, proceeding to next"
    elif [[ -e md_files/sMD_$(($startI-1)).rst ]]; then
        echo "-- Running script #"$startI
        runMD $startI
    else
        echo '-- previous equil file not found, skipping equilibration #'$startI
    fi
    startI=`expr $startI + 1`
done
            """
                f.write(buffer)
                f.close()
                
    def amd_submit(self,protein,method):
        for queue in self.list:
            for self.compiler in self.compilerList:
                if self.compiler == "pmemd":
                    self.CALCULATOR = "mpirun pmemd.MPI"
                if self.compiler == "cuda":
                    self.CALCULATOR = "pmemd.cuda"
                if self.compiler == "sander":
                    self.CALCULATOR = "mpirun sander.MPI"  
                    
                f = open(""+absdir+"/submissionScripts/aMD_submit_"+self.compiler+"_"+queue+".sh",'w')                
                buffer = Queue(queue,name, cores, ptile )        
                buffer = buffer + """
# Number of MD steps
md_steps="""+md_steps+"""

# A function for running another step of the script
runMD(){

# define the local step nr, previous step nr, and new step nr
local cStep=$1
echo "this is the current step" $((cStep))
local pStep=$(($1-1))

# Start amber MD simulation
"""+self.CALCULATOR+""" -O -i in_files/aMD.in -o logs/outAMD${cStep}.log -amd logs/aMD${cStep}.log -c md_files/equil${pStep}.rst -p in_files/"""+protein+""".prmtop -r md_files/equil${cStep}.rst -x md_files/equil${cStep}.mdcrd

# Create pdb file from results
ambpdb -p in_files/"""+protein+""".prmtop < md_files/equil${cStep}.rst > pdb_files/equil${cStep}.pdb
}

# Run the MD simulations. Figure out last stop, and take "md_steps" runs from that
arr=( md_files/equil*.rst )  # * is list of all file and dir names
m=${#arr[@]}
n=$(($n-1))
echo "Molecular Dynamics"
echo "-- Number of previous MD runs: "$(($n))

startI=$n
endI=$md_steps

while [ $startI -lt $endI ]
do
    if [[ -e md_files/equil$(($startI+1)).rst ]]; then
        echo "-- #"$startI" MD already run, skipping to next"
    elif [[ -e md_files/equil$(($startI-1)).rst ]]; then
        echo "-- Running script #"$startI
        runMD $startI
    else
        echo '-- previous equil file not found, skipping equilibration #'$startI
    fi
    startI=`expr $startI + 1`
done

"""
                f.write(buffer)
                f.close()
            
    def smd_submit(self,protein,method):
        for queue in self.list:
            for self.compiler in self.compilerList:
                if self.compiler == "pmemd":
                    self.CALCULATOR = "mpirun pmemd.MPI"
                if self.compiler == "cuda":
                    self.CALCULATOR = "pmemd.cuda"
                if self.compiler == "sander":
                    self.CALCULATOR = "mpirun sander.MPI"  
                    
                f = open(""+absdir+"/submissionScripts/sMD_submit_"+self.compiler+"_"+queue+".sh",'w')                
                buffer = Queue(queue,name, cores, ptile )        
                buffer = buffer + """              
                        
######################      Beginning the sMD simulations           ######################      
# sMD: steer the system
echo "steer NPT ensemble"

# Find the number of cMD runs and continue the sMD from that.
arr=( md_files/equil*.rst )  # * is list of all file and dir names
n=${#arr[@]}
m=$(($n-1))
echo "Molecular Dynamics"
echo "-- Number of previous MD runs: "$(($n-1))

if [[ -e md_files/sMD_0.rst ]]; then
    echo '-- sMD_0.rst file exists, proceeding to phase 1'
else
    echo '-- starting sMD phase 0'
    """+self.CALCULATOR+""" -O -i in_files/sMD_0.in -o logs/sMD_0.log -p in_files/"""+protein+""".prmtop -c md_files/equil$m.rst -r md_files/sMD_0.rst -x md_files/sMD_0.mdcrd
    
    # Create pdb file for the minimized structure
    ambpdb -p in_files/"""+protein+""".prmtop < md_files/sMD_0.rst > pdb_files/"""+protein+"""_sMD_0.pdb
    
fi

######################      Beginning the sMD equilibration         ######################                        
                        
                        
# A function for running another step of the script
runMD(){

# define the local step nr, previous step nr, and new step nr
local cStep=$1
local pStep=$(($1-1))

#Move the RST file to avoid it being overwritten!
mv data/dist.sMD.RST data/dist.sMD_${pstep}.RST

# Start amber MD simulation
"""+self.CALCULATOR+""" -O -i in_files/sMD_equil.in -o logs/sMD_${cStep}.log -c md_files/sMD_${pStep}.rst -p in_files/"""+protein+""".prmtop -r md_files/sMD_${cStep}.rst -x md_files/sMD_${cStep}.mdcrd

# Convert the resulting structure to a pdb-file
ambpdb -p in_files/"""+protein+""".prmtop < md_files/sMD_${cStep}.rst > pdb_files/sMD_${cStep}.pdb

}

# Run the MD simulations. Figure out last stop, and take "md_steps" runs from that
arr=( md_files/sMD_*.rst )  # * is list of all file and dir names
m=${#arr[@]}
n=$(($n-1))
echo "Molecular Dynamics"
echo "-- Number of previous sMD runs: "$(($m-1))

NumberOfsMDruns = """+NumberOfsMDRuns+"""

startI=$n
endI=$(($NumberOfsMDRuns))

while [ $startI -lt $endI ]
do
    if [[ -e md_files/sMD_$(($startI+1)).rst ]]; then
        echo "-- #"$startI" sMD already run, proceeding to next"
    elif [[ -e md_files/sMD_$(($startI-1)).rst ]]; then
        echo "-- Running script #"$startI
        runMD $startI
    else
        echo '-- previous equil file not found, skipping equilibration #'$startI
    fi
    startI=`expr $startI + 1`
done
            """
                f.write(buffer)
                f.close()
    

def main():
#    os.chdir(""+absdir_home+"/lib/setup/TemplateFiles/")
    # Define the constructor
    CreateSubmit = Create_Submit()
    if aMD == "on":
        CreateSubmit.amd_submit(protein,method)
    if sMD == "on" and newSim == "off":
        CreateSubmit.smd_submit(protein,method)          
    else:
        CreateSubmit.makeSubmitFile(protein,method)
    
    # Move the submission scripts
    if os.path.isfile(""+absdir+"/submissionScripts/submit_"+compiler+"_"+computingSystem+".sh") == True:
        os.system("mv "+absdir+"/submissionScripts/submit_"+compiler+"_"+computingSystem+".sh "+absdir+" ")
    if os.path.isfile(""+absdir+"/submissionScripts/submit_cuda_memento.sh") == True:
        os.system("rm "+absdir+"/submissionScripts/submit_cuda_memento.sh ")
        
    if aMD == "on":
        os.system("mv "+absdir+"/submissionScripts/aMD_submit_"+compiler+"_"+computingSystem+".sh "+absdir+" ")
        os.system("rm "+absdir+"/submissionScripts/aMD_submit_cuda_memento.sh ")
    if sMD == "on":
        if os.path.isfile(""+absdir+"/submissionScripts/sMD_submit_"+compiler+"_"+computingSystem+".sh") == True:        
            os.system("mv "+absdir+"/submissionScripts/sMD_submit_"+compiler+"_"+computingSystem+".sh "+absdir+" ")
        #os.system("rm "+absdir+"/submissionScripts/sMD_submit_cuda_memento.sh ")
    print "finished writing submission scripts"
    print "next step is to submit the simulation"
    
if __name__ == '__main__': main()