#!/bin/bash

args=("$@")

#check the correct num of args
if [[ ${#args[@]} == 0 ]] || [[ ${#args[@]} > 2 ]]; then
  echo "create_ASMDinputs.sh {NUM of trajectories} {NUM of MDsteps}"
  exit
fi

num_asmd_sim=${args[0]}
mdsteps=${args[1]}

#create the ASMD directories
counter=1
for ((counter=1; counter<=$num_asmd_sim; counter++)); do
  if [ ! -d ASMD_$counter ]; then
    mkdir ASMD_$counter
  fi
done


#create the MDIN inputs & dist RST files for the ASMD simulation
for ((counter=1; counter<=$num_asmd_sim;counter++));do
  start_distance=13
  end_distance=17
  for stage in {1..5};do
    cat >>asmd_$counter.$stage.mdin<<EOF
ASMD simulation
 &cntrl
   imin = 0, nstlim = $mdsteps, dt = 0.002,
   ntx = 1, temp0 = 300.0,
   ntt = 3, gamma_ln=5.0
   ntc = 2, ntf = 2, ntb =1,
   ntwx =  1000, ntwr = $mdsteps, ntpr = 1000,
   cut = 8.0, ig=-1, ioutfm=1,
   irest = 0, jar=1, 
 /
 &wt type='DUMPFREQ', istep1=1000 /
 &wt type='END'   /
DISANG=dist.RST.dat.$stage
DUMPAVE=asmd_$counter.work.dat.$stage
LISTIN=POUT
LISTOUT=POUT
EOF
  mv asmd_$counter.$stage.mdin ASMD_$counter/
  done
done

#create the distance RST files
start_distance=13
end_distance=17
for stage in {1..5}; do
    cat >>dist.RST.dat.$stage<<EOF
 &rst
        iat=9,99,
        r2=$start_distance,
        r2a=$end_distance,
        rk2=7.2,

 &end
EOF
  start_distance=$((start_distance+4))
  end_distance=$((end_distance+4))
done

