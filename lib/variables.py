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
parser.add_argument('-m1','--mutation1',
                    help='Specifies the first mutation site to CYX of the protein')
parser.add_argument('-m2','--mutation2',
                    help='Specifies the first mutation site to CYX of the protein')
                    
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

configSetup = ConfigParser.ConfigParser()
configSetup.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..','configSetup.cfg'))

###############################################################################
#################         Config setup variables     ##########################
###############################################################################


####### #System ################################
#ion         = configSetup.get('System', 'ion')
method      = configSetup.get('System','method')
compiler    = configSetup.get('System','compiler')
computingSystem = configSetup.get('System','computingSystem')

####### Submitvariables #######################
md_steps    = configSetup.get('Submit','md_steps')
nodes       = configSetup.get('Submit','nodes')
cores       = configSetup.get('Submit','cores')
ptile       = configSetup.get('Submit','ptile')
gpus        = configSetup.get('Submit','gpus')
gpu_cores   = configSetup.get('Submit','gpu_cores')
walltime    = configSetup.get('Submit','walltime')
#queue       = configSetup.get('Submit','queue')

####### Leap parameters #######################
insertProtein   =   configSetup.get('Leap','insertProtein')
crosslink       =   configSetup.get('Leap','crosslink')
link1           =   configSetup.get('Leap','link1')
link2           =   configSetup.get('Leap','link2')
configuration   =   configSetup.get('Leap','configuration')
forcefield      =   configSetup.get('Leap','forcefield')
waterboxsize    =   configSetup.get('Leap','waterboxsize')
solvate         =   configSetup.get('Leap','solvation')
structure       =   configSetup.get('Leap','structure')
insertAnion     =   configSetup.get('Leap','insertAnion')
ionName         =   configSetup.get('Leap','ionName')
frcmod          =   configSetup.get('Leap','frcmod')
insertAzobenzene=   configSetup.get('Leap','insertAzobenzene')
azoName         =   configSetup.get('Leap','azoName')
azoConfig       =   configSetup.get('Leap','azoConfig')

####### Mutations ##############################
MakeMutations   =   configSetup.get('Mutations','MakeMutations')
Mutation1       =   args.mutation1
Mutation2       =   args.mutation2

if args.mutation1 == None:
    Mutation1       =   configSetup.get('Mutations','Mutation1')
if args.mutation1 == None:
    Mutation2       =   configSetup.get('Mutations','Mutation2')


####### System parameters #####################
# Regular parameters
ntc         = configSetup.get('in_files','ntc')
ntf         = configSetup.get('in_files','ntf')  
timestep    = configSetup.get('in_files','timestep')
implicit    = configSetup.get('in_files','implicit')
igb         = configSetup.get('in_files','igb')
epsilon     = configSetup.get('in_files','epsilon')
#gamma       = configSetup.get('in_files','gamma')
aMD         = configSetup.get('in_files','aMD')
iamd        = configSetup.get('in_files','iamd')
DISANG      = configSetup.get('in_files','DISANG')
#QM parameters 
QM          = configSetup.get('QM','QM') #If QM is set to "None" the rest of the specification will not be included
qmcharge    = configSetup.get('QM','qmcharge')
qmmask      = configSetup.get('QM','qmmask')
qm_theory   = configSetup.get('QM','qm_theory')
qmshake     = configSetup.get('QM','qmshake')
qm_ewald    = configSetup.get('QM','qm_ewald')
qm_pme      = configSetup.get('QM','qm_pme')

#Steered MD parameters
sMD            = configSetup.get('Steered','sMD')
newSim         = configSetup.get('Steered','newSim')
NumberOfsMDRuns= configSetup.get('Steered','NumberOfsMDRuns')

SteeredRes1    = configSetup.get('Steered','SteeredRes1')
AtomType1      = configSetup.get('Steered','AtomType1')

SteeredRes2    = configSetup.get('Steered','SteeredRes2')
AtomType2      = configSetup.get('Steered','AtomType2')

initialDistance= configSetup.get('Steered','initialDistance')
finalDistance  = configSetup.get('Steered','finalDistance')
r2k            = configSetup.get('Steered','r2k')

###############################################################################
#################         Config analysis variables  ##########################
###############################################################################

configAnalysis = ConfigParser.ConfigParser()
configAnalysis.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..','configAnalysis.cfg'))

#Cluster Analysis:
mergeTraj           =   configAnalysis.get('Analysis','mergeTraj')
deleteOldData       =   configAnalysis.get('Analysis','deleteOldData')
dcdname             =   configAnalysis.get('Analysis','dcdname')
mergeTrajSolvate    =   configAnalysis.get('Analysis','mergeTrajSolvate')
dcdnameSolvated     =   configAnalysis.get('Analysis','dcdnameSolvated')
includeHeat         =   configAnalysis.get('Analysis','includeHeat')
includeEquil        =   configAnalysis.get('Analysis','includeEquil')
interval            =   configAnalysis.get('Analysis','interval')
#removeWaters        =   configAnalysis.get('Analysis','removeWaters')

makeAnalysis        =   configAnalysis.get('Analysis','makeAnalysis')
makePlots           =   configAnalysis.get('Analysis','makePlots')
makeHistPlots       =   configAnalysis.get('Analysis','makeHistPlots')

clusterAnalysis     =   configAnalysis.get('Analysis','clusterAnalysis')
nodesAnalysis       =   configAnalysis.get('Analysis','nodesAnalysis')
coresAnalysis       =   configAnalysis.get('Analysis','coresAnalysis')
walltimeAnalysis    =   configAnalysis.get('Analysis','walltimeAnalysis')
epsilon_hier        =   configAnalysis.get('Analysis','epsilon_hier')
epsilon_dbscan      =   configAnalysis.get('Analysis','epsilon_dbscan') 
sieve_hier          =   configAnalysis.get('Analysis','sieve_hier')
sieve_dbscan        =   configAnalysis.get('Analysis','sieve_dbscan')

R_Analysis          =   configAnalysis.get('Analysis','R_analysis')

MMPBSA              =   configAnalysis.get('Analysis','MMPBSA')
intervalMMPBSA      =   configAnalysis.get('Analysis','intervalMMPBSA')
qmcharge_ion        =   configAnalysis.get('Analysis','qmcharge_ion')
qmcharge_protein    =   configAnalysis.get('Analysis','qmcharge_protein')
qmcharge_complex    =   configAnalysis.get('Analysis','qmcharge_complex')
qm_residues         =   configAnalysis.get('Analysis','qm_residues')

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
        if compiler == "cuda":
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