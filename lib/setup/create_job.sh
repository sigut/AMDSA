#!/bin/bash

args=("$@")

#check the correct num of args
if [[ ${#args[@]} == 0 ]] || [[ ${#args[@]} > 3 ]]; then
  echo "create_ASMDjobfile.sh {NUM of trajectories} {Coord/RST7} {Stage Num}"
  exit
fi

num_asmd_sim=${args[0]}


if [ ! -f ${args[1]} ]; then
  echo The file ${args[1]} does not exist
  exit
else
  coord=${args[1]}
  
fi

stage=${args[2]}

cat >>_job.sh<<EOF
#!/bin/sh
#PBS -m abe
#PBS -M username@gatech.edu
#PBS -N ASMD_stage$stage
#PBS -l walltime=4:00:00
#PBS -l nodes=2:ppn=8
#PBS -j oe

cd SSSPBS_O_WORKDIR

do_parallel="mpirun -np 16 pmemd.MPI"
prmtop="ala.asmd.prmtop"
coord="$coord"

EOF

for ((counter=1;counter<=$num_asmd_sim;counter+=1)); do
  echo SSSdo_parallel -O -i ASMD_$counter/asmd_$counter.$stage.mdin -p SSSprmtop -c SSScoord -r ASMD_$counter/ASMD_$counter.$stage.rst7 -o ASMD_$counter/ASMD_$counter.$stage.mdout -x ASMD_$counter/ASMD_$counter.$stage.nc -inf ASMD_$counter/ASMD_$counter.$stage.info >>_job.sh
done

sed 's/SSS/$/g' _job.sh > job.$stage.sh; rm -f _job.sh


