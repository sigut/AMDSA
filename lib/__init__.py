# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 21:17:34 2015

@author: sigurd
"""

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

__all__ = ["bar", "spam", "eggs"]

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

class CommandLine:
    def __init__(self):
        #Command-line Variables:
        self.root  = args.idir
        self.protein = args.protein
        self.qsub = args.qsub
        self.nomerge = args.nomerge
        # Directory Variables:
        self.home = os.getcwd() #Specify the root directory
        self.absdir = os.path.abspath(""+self.root+"")
        self.absdir_home = os.path.abspath(""+self.home+"")
        self.name = os.path.basename(os.path.normpath(""+self.absdir+""))
        self.directory = "./src/analysis/"
        
        

###############################################################################
#################            Config variables        ##########################
###############################################################################

class Config:
    def __init__(self):
        
        config = ConfigParser.ConfigParser()
        config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..','config.cfg'))
####### #System ################################
        self.method      = config.get('System','method')
        self.compiler    = config.get('System','compiler')
        
####### Submitvariables #######################
        self.md_steps    = config.get('Submit','md_steps')
        self.nodes       = config.get('Submit','nodes')
        self.cores       = config.get('Submit','cores')
        self.ptile       = config.get('Submit','ptile')
        self.gpus        = config.get('Submit','gpus')
        self.walltime    = config.get('Submit','walltime')
        #queue       = config.get('Submit','queue')
        
####### Leap parameters #######################
        self.forcefield      =   config.get('Leap','forcefield')
        self.waterboxsize    =   config.get('Leap','waterboxsize')
        self.solvate         =   config.get('Leap','solvation')
        self.structure       =   config.get('Leap','structure')
        self.insertAnion     =   config.get('Leap','insertAnion')
        self.ionName         =   config.get('Leap','ionName')
        
####### System parameters #####################
        # Regular parameters
        self.ntc         = config.get('in_files','ntc')
        self.ntf         = config.get('in_files','ntf')  
        self.timestep    = config.get('in_files','timestep')
        self.implicit    = config.get('in_files','implicit')
        self.igb         = config.get('in_files','igb')
        self.iamd        = config.get('in_files','iamd')
        #QM parameters 
        self.QM          = config.get('QM','QM') #If QM is set to "None" the rest of the specification will not be included
        self.qmcharge    = config.get('QM','qmcharge')
        self.qm_theory   = config.get('QM','qm_theory')
        self.qmshake     = config.get('QM','qmshake')
        self.qm_ewald    = config.get('QM','qm_ewald')
        self.qm_pme      = config.get('QM','qm_pme')
        
######## Analysis ##############################
        #Cluster Analysis:
        
        #nomerge             = config.get('Analysis','trajectoryMerge')
        self.dcdname             =   config.get('Analysis','dcdname')
        self.nodesAnalysis       =   config.get('Analysis','nodes')
        self.coresAnalysis       =   config.get('Analysis','cores')
        self.walltimeAnalysis    =   config.get('Analysis','walltime')
        self.epsilon_hier        =   config.get('Analysis','epsilon_hier')
        self.epsilon_dbscan      =   config.get('Analysis','epsilon_dbscan') 
        self.sieve_hier          =   config.get('Analysis','sieve_hier')
        self.sieve_dbscan        =   config.get('Analysis','sieve_dbscan')

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
#BSUB -o """+name+"""_%J.out
#BSUB -e """+name+"""_%J.err

# Temporary fix on DTU HPC
.  /etc/profile.d/machinetype.sh

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
#PBS -l nodes=1:ppn=1:gpus="""+gpus+"""
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