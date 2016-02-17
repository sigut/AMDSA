# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 14:08:09 2015

@author: sigurd
"""

# This script parses the variables between the Master_setup script and into the individual modules.
# It uses the command-line arguments for protein and folder specification
# More technical parameters/settings are specified in the config.cfg file in the root folder.
import os
import argparse
import ConfigParser


#Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--idir',
                    help = 'input directory of the simulation' )
parser.add_argument('-p', '--protein',
                    help = 'Specification of the prmtop and inpcrd name')
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

#How many residues including the phosphate?
if protein == "pbpu": 
    resi_protein = "376"
    NumberOfResidues = 375
    P_protein = "5325"
if protein == "pbpv":
    resi_protein = "373"
    NumberOfResidues = 372
    P_protein = "5290"
if protein == "1IXH":
    resi_protein = "322"
    NumberOfResidues = 321
if protein == "2ABH":
    resi_protein = "322"
    NumberOfResidues = 321   
if protein == "1OIB":
    resi_protein = "322"
    NumberOfResidues = 321
if protein == "AzobenzeneTrans":
    resi_protein = "1"
    NumberOfResidues = 1

config = ConfigParser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..','config.cfg'))

###############################################################################
#################            Config variables        ##########################
###############################################################################


####### #System ################################
#ion         = config.get('System', 'ion')
method      = config.get('System','method')
compiler    = config.get('System','compiler')

####### Submitvariables #######################
md_steps    = config.get('Submit','md_steps')
nodes       = config.get('Submit','nodes')
cores       = config.get('Submit','cores')
ptile       = config.get('Submit','ptile')
gpus        = config.get('Submit','gpus')
gpu_cores   = config.get('Submit','gpu_cores')
walltime    = config.get('Submit','walltime')
#queue       = config.get('Submit','queue')

####### Leap parameters #######################
insertProtein   =   config.get('Leap','insertProtein')
crosslink       =   config.get('Leap','crosslink')
link1           =   config.get('Leap','link1')
link2           =   config.get('Leap','link2')
configuration   =   config.get('Leap','configuration')
forcefield      =   config.get('Leap','forcefield')
waterboxsize    =   config.get('Leap','waterboxsize')
solvate         =   config.get('Leap','solvation')
structure       =   config.get('Leap','structure')
insertAnion     =   config.get('Leap','insertAnion')
ionName         =   config.get('Leap','ionName')
frcmod          =   config.get('Leap','frcmod')
insertAzobenzene=   config.get('Leap','insertAzobenzene')
azoName         =   config.get('Leap','azoName')

####### Mutations ##############################
MakeMutations   =   config.get('Mutations','MakeMutations')
Mutation1       =   config.get('Mutations','Mutation1')
Mutation2       =   config.get('Mutations','Mutation2')

####### System parameters #####################
# Regular parameters
ntc         = config.get('in_files','ntc')
ntf         = config.get('in_files','ntf')  
timestep    = config.get('in_files','timestep')
implicit    = config.get('in_files','implicit')
igb         = config.get('in_files','igb')
epsilon     = config.get('in_files','epsilon')
#gamma       = config.get('in_files','gamma')
aMD         = config.get('in_files','aMD')
iamd        = config.get('in_files','iamd')
DISANG      = config.get('in_files','DISANG')
#QM parameters 
QM          = config.get('QM','QM') #If QM is set to "None" the rest of the specification will not be included
qmcharge    = config.get('QM','qmcharge')
qmmask      = config.get('QM','qmmask')
qm_theory   = config.get('QM','qm_theory')
qmshake     = config.get('QM','qmshake')
qm_ewald    = config.get('QM','qm_ewald')
qm_pme      = config.get('QM','qm_pme')

######## Analysis ##############################
#Cluster Analysis:
deleteOldData       =   config.get('Analysis','deleteOldData')
dcdname             =   config.get('Analysis','dcdname')
includeHeat         =   config.get('Analysis','includeHeat')
includeEquil        =   config.get('Analysis','includeEquil')
interval            =   config.get('Analysis','interval')
removeWaters        =   config.get('Analysis','removeWaters')
clusterAnalysis     =   config.get('Analysis','clusterAnalysis')
nodesAnalysis       =   config.get('Analysis','nodes')
coresAnalysis       =   config.get('Analysis','cores')
walltimeAnalysis    =   config.get('Analysis','walltime')
epsilon_hier        =   config.get('Analysis','epsilon_hier')
epsilon_dbscan      =   config.get('Analysis','epsilon_dbscan') 
sieve_hier          =   config.get('Analysis','sieve_hier')
sieve_dbscan        =   config.get('Analysis','sieve_dbscan')
R_Analysis          =   config.get('Analysis','R_analysis')

###############################################################################
###############################################################################
###############################################################################

def Queue(queue,name, cores, ptile):
    if queue == "memento": 
        buffer = """
#!/bin/sh
#BSUB -J """+root+"""
#BSUB -q memento
#BSUB -n """+cores+"""
#BSUB -R "span[ptile="""+ptile+"""]"
#BSUB -W 720:00
#BSUB -u sigut@env.dtu.dk
#BSUB -B
#BSUB -N
#BSUB -o """+name+""".o%J
#BSUB -e """+name+""".e%J

# Temporary fix on DTU HPC
.  /etc/profile.d/b_machinetype.sh 

# load the necessary modules
module purge
module load gcc/4.8.4
module load mpi/gcc-openmpi-1.6.5-lsfib
module load amber/14-gcc-4.8.4

echo "CURRENT CPU TYPE"
echo $CPUTYPEV
echo "AMBER HOME DIRECTORY:"
echo $AMBERHOME
    """
        return buffer
    if queue == "hpc":
        if compiler == "pmemd.cuda":
            buffer = """
#!/bin/sh
#
#PBS -N """+root+"""
#PBS -l nodes=1:ppn="""+gpu_cores+""":gpus="""+gpus+"""
#PBS -l walltime="""+walltime+"""

cd $PBS_O_WORKDIR

# The CUDA device reserved for you by the batch system
CUDADEV=`cat $PBS_GPUFILE | rev | cut -d"-" -f1 | rev | tr -cd [:digit:]`
echo "CUDA Devices"
echo $CUDADEV
export CUDA_VISIBLE_DEVICES=$CUDADEV
echo "CUDA Visible Devices"
echo $CUDA_VISIBLE_DEVICES

# load the required modules
module load cuda/5.5
export CUDA_HOME=/opt/cuda/5.5
            """
            
        if compiler == "pmemd.cuda.MPI":
            buffer = """
#!/bin/sh
#
#PBS -N """+root+"""
#PBS -l nodes=1:ppn="""+gpu_cores+""":gpus="""+gpus+"""
#PBS -l walltime="""+walltime+"""

cd $PBS_O_WORKDIR

# The CUDA device reserved for you by the batch system
CUDADEV=`cat $PBS_GPUFILE | rev | cut -d"-" -f1 | rev | tr -cd [:digit:]`
echo "CUDA Devices"
echo $CUDADEV
export CUDA_VISIBLE_DEVICES=$CUDADEV
echo "CUDA Visible Devices"
echo $CUDA_VISIBLE_DEVICES

# load the required modules
module load cuda/5.5
module load mpi/gcc
export CUDA_HOME=/opt/cuda/5.5
            """
        if compiler == "sander" or compiler == "pmemd":
            buffer = """
#!/bin/sh
#
#PBS -N """+root+"""
#PBS -l nodes="""+nodes+""":ppn="""+cores+"""
#PBS -l walltime="""+walltime+"""
            
# load the necessary modules
module purge
module load gcc/4.8.4
module load amber/14-gcc-4.8.4

echo "CURRENT CPU TYPE"
echo $CPUTYPEV
echo "AMBER HOME DIRECTORY:"
echo $AMBERHOME
    

cd $PBS_O_WORKDIR


# Load mpi
module load mpi/gcc-4.7.2-openmpi-1.6.3
            """
       
        return buffer