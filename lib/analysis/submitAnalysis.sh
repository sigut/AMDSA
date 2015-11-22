#!/bin/sh
#
#PBS -N R_analysis
#PBS -l nodes=1:ppn=8
#PBS -l walltime=72:00:00

# Run in the current working (submission) directory
if test X$PBS_ENVIRONMENT = XPBS_BATCH; then cd $PBS_O_WORKDIR; fi

# Load mpi
module load mpi/gcc-4.7.2-openmpi-1.6.3
module load python

# Run R script 
R < analysis.R --no-save
