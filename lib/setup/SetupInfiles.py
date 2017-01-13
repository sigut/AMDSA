# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 17:12:58 2015

@author: sigut
"""

# This is a script for setting up the in files for the AMBER simulation. Currently it creates:
# 3 minimization files
# 1 heating file
# 1 equil file
# 1 cMD production run or aMD file- However the aMD must read the energies given by the equil simulation.

import os, sys,inspect

the_list = ["lib","lib/setup"]
for folders in the_list:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],str(folders))))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)

from variables import *

class SetupInfiles:
    
    def __init__(self):
         self.QMMM = """  ifqnt = 1,
/
&qmmm
  qmmask="""+qmmask+""",
  qmcharge="""+qmcharge+""",
  qm_theory="""+qm_theory+""",
  qmshake="""+qmshake+""",
  qm_ewald="""+qm_ewald+""",
  qm_pme="""+qm_pme+"""
/ 
"""        
         self.implicit = """  igb = """+igb+""",  ntb = 0, cut = 16,
         extdiel ="""+epsilon+""", """
        
#The “proper” default for ntb is chosen (ntb=0 when igb > 0, ntb=2 when ntp > 0, and ntb=1 otherwise).        #
    def setup_min(self):
        #Minimize only the water, restraining the protein (20000 cycles)
        
        f = open("in_files/min1.in",'w')
        f.write(" Minimize water \n")
        f.write("System minimization:\n")
        f.write("&cntrl\n")
        f.write("  imin=1, ntmin=1          \n")    # Perform energy minimization, Steepest decent method, Do not performe nmr type analysis
        if implicit == "on":
            f.write(""+self.implicit+"\n")
        else: 
            f.write("  ntb=1,           \n")    # Constant volume (for explicit simulations) Periodic boundary conditions of non-bonded interactions: 
            f.write("  cut=10.0,        \n")    # Specify the nonbonded cutoff in Angstroms        
        f.write("  drms=0.1         \n")    # Convergence criterion ffor the energy gradient
        f.write("  maxcyc=10000,    \n")    # Maximum number of cycles of minimization.
        f.write("  ncyc=5000,       \n")    # If NTMIN is 1 then the method of minimization will be switched from steepest descent to conjugate gradient after NCYC cycles
        f.write("  ntx=1,           \n")    # inpcrd file is read without initial velocity information
        f.write("  irest=0,         \n")    # Do not restart simulation - run new simulation
        f.write("  ntpr=100,        \n")    # Write mdout for every ntpr steps
        f.write("  ntwr=100,        \n")    # Write restrt file for every ntwr steps
        f.write("  ntwx=100,        \n")    # Write restrt file for every ntwr steps
        f.write("  iwrap=0,         \n")    # No wrapping of restart files (see p. 287)
        f.write("  ntf=1,           \n")    # Force evaluation: Complete interaction
        f.write("  nsnb=20,         \n")    # Frequency of nonbonded list updates
        if not implicit == "on":
            f.write("  ntr=1,            \n")    # lag for restraining specified atoms in Cartesian space using a harmonic potential, if ntr > 0
            f.write("  restraintmask=\'!:WAT\',\n")# String that specifies the restrained atoms when ntr = 1 
            f.write("  restraint_wt = 10.0,\n")  # Weight of the positional restraints
        if QM == "on":
            f.write(""+self.QMMM+"")
        f.write("&end\n")
        f.write(" / \n")
        f.close()
        
        #Let water move (NTP, 300K), restraining the protein
        f = open("in_files/min2.in",'w')
        f.write("LET WATER MOVE \n")
        f.write("&cntrl \n")
        f.write("  ntx    = 1, irest  = 0,    \n")      # inpcrd file is read without initial velocity information, Do not restart simulation - run new simulation, Do not performe nmr type analysis
        if implicit == "on":
            f.write(""+self.implicit+"\n")
        else: 
            f.write("  ntb = 2, ntp = 1 , taup   = 1.0,           \n")    # Constant Pressure
            f.write("  cut=10.0,        \n")    # Specify the nonbonded cutoff in Angstroms       
            f.write("  iwrap  = 1,     \n")      # setting Iwrap =1 is good for ascii written outputs
        f.write("  ntrx   = 1,     \n")
        f.write("  ntxo   = 1,     \n")     # Format of restrt file --> ASCII
        f.write("  ntpr   = 100, ntwx   = 100, ntwr   = 100,  \n")      # Write mdout for every ntpr steps, Write restrt file for every ntwr steps
        f.write("  nscm   = 2500,  \n")      # For non-periodic simulations, after every NSCM steps, translational and rotational motion will be removed.
        f.write("  ntf    = "+ntf+",     \n")      # Force evaluation: bond interactions involving H-atoms omitted (use with NTC=2)
        f.write("  ntc    = "+ntc+",     \n")      # Flag for shake --> =2 bonds involving hydrogen are constained
        f.write("  nsnb   = 20,    \n")      # Frequency of nonbonded list updates
        if timestep == "0.002":
            f.write("  nstlim = 250000, \n")      # Number of MD-steps to be performed
            f.write("  dt     = 0.002, \n")      # Time step in ps
        if timestep == "0.001":
            f.write("  nstlim = 500000, \n")      # Number of MD-steps to be performed
            f.write("  dt     = 0.001, \n")      # Time step in ps
        f.write("  t      = 0.0,   \n")      # The time of start
        f.write("  temp0  = 300.0, \n")      # Refernce temperature
        f.write("  tempi  = 200.0, \n")      # Initial temperature
        f.write("  tautp  = 0.5,   \n")      # Time constant in ps for heat bath coupling
        f.write("  ntt    = 1,     \n")      # Constant temperature using the weak-coupling algorithm
        f.write("  tol    = 0.00001,\n")     #
        if DISANG == "on":
            f.write("  nmropt = 1,                      \n")
        if not implicit == "on":
            f.write("  ntr=1,           \n")     # flag for restraining specified atoms in Cartesian space using a harmonic potential, if ntr > 0
            f.write("  restraintmask=\'!:WAT\',\n") # String that specifies the restrained atoms when ntr = 1
            f.write("  restraint_wt = 10.0,  \n")# Weight of the positional restraints
        if QM == "on":
            f.write(""+self.QMMM+"")
        if DISANG == "on":
            f.write("&wt type=’DUMPFREQ’, istep1=100, \n")        
            f.write("&wt type=’END’, \n")   
            f.write(" DISANG=distFile.RST\n")
            f.write(" DUMPAVE=logs/disFile.dat\n")
            f.write(" LISTIN=POUT\n")
            f.write(" LISTOUT=POUT\n")
            
        f.close()
        
        # Minimize water and protein (20000 cycles)
        f = open("in_files/min3.in",'w')
        f.write(" System minimization:\n")
        f.write("&cntrl               \n")
        f.write("  imin=1, ntmin=1,          \n")   
        if implicit == "on":
             f.write(""+self.implicit+"\n")
        else: 
           f.write("  ntb=1, cut=10.0, iwrap = 0,   \n")    # Specify the nonbonded cutoff in Angstroms
        f.write("  drms=0.1          \n")   
        f.write("  maxcyc=2000,      \n")
        f.write("  ncyc=1500,        \n")
        f.write("  ntx=1,            \n")
        f.write("  irest=0,          \n")
        f.write("  ntpr=100,         \n")
        f.write("  ntwr=100,         \n")
        f.write("  ntwx=100,         \n")    # Write restrt file for every ntwr steps
        f.write("  ntf=1,            \n")
        f.write("  ntc=1,            \n")
        f.write("  cut=10.0,         \n")
        f.write("  nsnb=20,          \n")
        if not implicit == "on":
            f.write("  ntr=1,           \n")     # flag for restraining specified atoms in Cartesian space using a harmonic potential, if ntr > 0
            f.write("  restraintmask=\'!:WAT\',\n")# String that specifies the restrained atoms when ntr = 1 
            f.write("  restraint_wt = 10.0,\n")  # Weight of the positional restraints
        if DISANG == "on":
            f.write("DISANG=distFile.RST                      \n")
        if QM == "on":
            f.write(""+self.QMMM+"")
        f.write("&end                 \n")
        f.write(" / \n")
        f.close()

     
    def setup_heat(self):
        # Heat the system, restraining the protein (NVT 0 to 300K)
        f = open("in_files/heat1.in",'w') 
        f.write(" Heating System NVT 0.5 ns             \n")
        f.write("&cntrl                                 \n")
        f.write("  ntx=1, irest=0,                      \n")
        if implicit == "on":
            f.write(""+self.implicit+"                  \n")
        else: 
            f.write("  ntb=1, cut=10.0, iwrap=1,         \n")    # Specify the nonbonded cutoff in Angstroms
        f.write("  ntpr=500, ntwr=500, ntwx=500,         \n")
        f.write("  ntc="+ntc+", ntf="+ntf+", nsnb=20,    \n")
        if timestep == "0.002":
            f.write("  nstlim=250000,dt=0.002,           \n") # heat for 500000*0.002 ps = 1000 ps
        if timestep == "0.001": 
            f.write("  nstlim=500000,dt=0.001,          \n") # Heat for 1000000*0.001 ps = 1000 ps         
        f.write("  nscm=500, ntt=1,                     \n") # Constant temperature using the weak-coupling algorithm
        f.write("  tempi=0.0, temp0=300.0, tautp=0.5      \n")
        f.write("/ \n")
        if QM == "on":
            f.write(""+self.QMMM+"")
        f.write("/ \n")
        if not implicit == "on":
            f.write("  ntr=1,           \n")     # flag for restraining specified atoms in Cartesian space using a harmonic potential, if ntr > 0
            f.write("  restraintmask=\'!:WAT\', \n")
            f.write("  restraint_wt=10.0,                   \n")
        f.write("  nmropt = 1,                      \n")
        f.write("/                 \n")
        # Type defines quantity that is begin varied
        if timestep == "0.002":
            f.write("  &wt type='REST', istep1 = 0, istep2=0, value1=1.0, value2=1.0, &end \n") #Rest for relative weights of all the NMR restraint energy terms
            f.write("  &wt type='TEMP0', istep1=0, istep2=250000, value1=0.0, value2=300, &end \n")       # Varies the target temperature
        if timestep == "0.001":
            f.write("  &wt type='REST', istep1 = 0, istep2=0, value1=1.0, value2=1.0, &end \n") #Rest for relative weights of all the NMR restraint energy terms
            f.write("  &wt type='TEMP0', istep1=0, istep2=500000, value1=0.0, value2=300, &end \n")       # Varies the target temperature
        f.write("  &wt type='END' \n")
        if DISANG == "on":
            f.write("&wt type=’DUMPFREQ’, istep1=100, \n")        
            f.write("&wt type=’END’, \n")   
            f.write(" DISANG=distFile.RST\n")
            f.write(" DUMPAVE=logs/disFile.dat\n")
            f.write(" LISTIN=POUT\n")
            f.write(" LISTOUT=POUT\n")  
        f.close()
        
        f = open("in_files/heat2.in",'w')
        f.write("equil NTP 0.5 ns \n")
        f.write(" heat                                   \n")
        f.write(" &cntrl                                 \n")
        f.write("  irest=1,ntx=5,                        \n")
        if implicit == "on":
            f.write(""+self.implicit+"\n")
        else:
            f.write("  cut=10.0, ntb=2, ntp=1, taup=1.0, iwrap=1, \n")
        if timestep == "0.002":
            f.write("  nstlim=250000,dt=0.002,           \n")
        if timestep == "0.001":
            f.write("  nstlim=500000,dt=0.001,           \n")
        f.write("  ntc="+ntc+",ntf="+ntf+",              \n")        
        f.write("  ntpr=500, ntwx=500,                   \n")
        f.write("  ntt=3, gamma_ln=2.0,                  \n")
        f.write("  temp0=300.0,                  \n")
        if not implicit == "on":
            f.write("  ntr=1,           \n")     # flag for restraining specified atoms in Cartesian space using a harmonic potential, if ntr > 0
            f.write("  restraintmask=\'!:WAT\', \n")
            f.write("  restraint_wt=5.0,                    \n")
        if DISANG == "on":
            f.write("  nmropt = 1,                      \n")
        if QM == "on":
            f.write(""+self.QMMM+"")
        f.write("/ \n")
        if DISANG == "on":
            f.write("&wt type=’DUMPFREQ’, istep1=100, \n")        
            f.write("&wt type=’END’, \n")   
            f.write(" DISANG=distFile.RST\n")
            f.write(" DUMPAVE=logs/disFile.dat\n")
            f.write(" LISTIN=POUT\n")
            f.write(" LISTOUT=POUT\n")  
        f.close()
    
     
    # Relax the system (NPT, 300K, 5ns)
    def equil(self):
        f = open("in_files/equil.in",'w')
        f.write("equil NPT 5 ns                         \n")
        f.write("&cntrl                                 \n")
        f.write("  irest=1,ntx=5,                \n")
        if timestep == "0.002":
            f.write("  nstlim=2500000,dt=0.002,          \n") # Equilibrate for 250000*0.002 ps = 5000 ps = 5 ns 
        if timestep == "0.001": 
            f.write("  nstlim=5000000,dt=0.001,          \n") # Equilibrate for 500000*0.001 ps = 5000 ps = 5 ns 
        if implicit == "on":
            f.write(""+self.implicit+"\n")
        else:
            f.write("  cut=10.0, ntb=2, ntp=1, taup=2.0,    \n")
        f.write("  ntc="+ntc+",ntf="+ntf+",ig=-1,       \n")
        f.write("  ntpr=1000, ntwx=1000,                \n")
        f.write("  ntt=3, gamma_ln=2.0,                 \n")
        f.write("  temp0 = 300.0,                       \n")
        if DISANG == "on":
            f.write("  nmropt = 1,                      \n")
        if QM == "on":
            f.write(""+self.QMMM+"")
        f.write("/ \n")
        if DISANG == "on":
            f.write("&wt type=’DUMPFREQ’, istep1=100, \n")        
            f.write("&wt type=’END’, \n")   
            f.write(" DISANG=distFile.RST\n")
            f.write(" DUMPAVE=logs/disFile.dat\n")
            f.write(" LISTIN=POUT\n")
            f.write(" LISTOUT=POUT\n")  
        f.close()
        
    def cMD(self):
        #Relax the system (NPT, 300K, 5ns)
        f = open("in_files/cMD.in",'w')
        f.write(" production run 2 ns     \n")
        f.write(" &cntrl                    \n")
        f.write("  irest=1,ntx=5,    \n")
        if implicit == "on":
            f.write(""+self.implicit+"\n")
        else:
            f.write("  cut=10.0, ntb=1, ntp=0,  \n")
        f.write("  nstlim="+nstlim+",dt="+timestep+", ,iwrap=1 \n")     # Production run for 100000*0.002 ps = 2000 ps = 2 ns (repeated in submit.sh)
        f.write("  ntc="+ntc+",ntf="+ntf+",ig=-1,       \n")
        f.write("  ntpr=1000, ntwx=1000,    \n")
        f.write("  ntt=3, gamma_ln=2.0,     \n")
        f.write("  temp0=300.0,ioutfm=1, \n")
        if DISANG == "on":
            f.write("  nmropt = 1,                      \n")
        if QM == "on":
            f.write(""+self.QMMM+"")
        f.write("/ \n")
        if DISANG == "on":
            f.write("&wt type=’DUMPFREQ’, istep1=100, \n")        
            f.write("&wt type=’END’, \n")   
            f.write(" DISANG=distFile.RST\n")
            f.write(" DUMPAVE=logs/disFile.dat\n")
            f.write(" LISTIN=POUT\n")
            f.write(" LISTOUT=POUT\n")  
        f.close()
    
    def sMD(self):
        f = open("in_files/sMD_0.in",'w')
        f.write(" #steered MD run     \n")
        f.write(" &cntrl                    \n")
        f.write("  irest=1,ntx=5,    \n")
        if implicit == "on":
            f.write(""+self.implicit+"\n")
        else:
            f.write("  cut=10.0, ntb=2, ntp=1,  \n") # The steering should be done in a NPT ensemble with constant pressure and periodic boundary conditions
        f.write("  nstlim="+sMDSteps+" ,dt="+timestep+", ,iwrap=1 \n")     # Production run for 100000*0.002 ps = 2000 ps = 2 ns (repeated in submit.sh)
        f.write("  ntc="+ntc+",ntf="+ntf+",ig=-1,       \n")
        f.write("  ntpr=1000, ntwx=1000,    \n")
        f.write("  ntt=3, gamma_ln=2.0,     \n")
        f.write("  temp0=300.0,ioutfm=1, \n")
        f.write("  jar = 1, \n")
        if DISANG == "on":
            f.write("  nmropt = 1,                      \n")
        if QM == "on":
            f.write(""+self.QMMM+"")
        f.write("/ \n")
        if DISANG == "on":
            f.write("DISANG=distFile.RST                      \n")
        
        f.write("&wt type=’DUMPFREQ’, istep1=100, \n")        
        f.write("&wt type=’END’, \n")        
        f.write("DISANG=in_files/sMD_0.RST \n")        
        f.write("DUMPAVE=data/sMD_0.RST \n")        
        f.write("LISTIN=POUT \n")        
        f.write("LISTOUT=POUT \n")        
        f.close()
        
        f = open("in_files/sMD_0.RST",'w')
        f.write("&rst \n" )
        f.write("   iat= "+str(self.AtomNumber1)+","+str(self.AtomNumber2)+" , \n")
        f.write("   r2="+initialDistance+", r2a="+finalDistance+", \n")
        f.write("   r2k="+sMDForce+" \n")
        f.write("&end \n" )
        f.close()

# Write the sMD equilibration files
        
        f = open("in_files/sMD_equil.in",'w')
        f.write(" #steered MD run     \n")
        f.write(" &cntrl                    \n")
        f.write("  irest=1,ntx=5,    \n")
        if implicit == "on":
            f.write(""+self.implicit+"\n")
        else:
            f.write("  cut=10.0, ntb=1, ntp=0,  \n")
        f.write("  nstlim="+sMDEquilSteps+" ,dt="+timestep+", ,iwrap=1 \n")     # Production run for 100000*0.002 ps = 2000 ps = 2 ns (repeated in submit.sh)
        f.write("  ntc="+ntc+",ntf="+ntf+",ig=-1,       \n")
        f.write("  ntpr=1000, ntwx=1000,    \n")
        f.write("  ntt=3, gamma_ln=2.0,     \n")
        f.write("  temp0=300.0,ioutfm=1, \n")
        f.write("  jar = 1,nmropt = 1, \n")
        if DISANG == "on":
            f.write("  nmropt = 1,                      \n")
        if QM == "on":
            f.write(""+self.QMMM+"")
        f.write("/ \n")
        if DISANG == "on":
            f.write("DISANG=distFile.RST                      \n")        
        f.write("&wt type=’DUMPFREQ’, istep1=1000, \n")        
        f.write("&wt type=’END’, \n")        
        f.write("DISANG=in_files/sMD_equil.RST \n")        
        f.write("DUMPAVE=data/dist.sMD.RST \n")        
        f.write("LISTIN=POUT \n")        
        f.write("LISTOUT=POUT \n")        
        f.close()
        
        f = open("in_files/sMD_equil.RST",'w')
        f.write("&rst \n" )
        f.write("   iat= "+str(self.AtomNumber1)+","+str(self.AtomNumber2)+" , \n")
        f.write("   r1 = "+r1+"  \n")
        f.write("   r2 = "+r2+"  \n")
        f.write("   r3 = "+r3+"  \n")
        f.write("   r4 = "+r4+"  \n")
        f.write("   rk2= "+rk2+" \n")
        f.write("   rk3= "+rk3+" \n")
        f.write("&end \n" )
        f.close()
    
    def DISANG(self):
        f = open("in_files/distFile.RST",'w')
        f.write("  &rst  iat= 1327,"+P_protein+", r1=1, r2=2.5, r3=15, r4=20, rk2=0, rk3=50, &end ")
        f.close()
        
        
    def FindAtomNumbers(self,protein): # Read the coordinates of the protein pdb file
        self.pdbFile = ""+absdir+"/in_files/"+protein+"_finalLEAP_nowat.pdb"
        f = open(self.pdbFile,'r')
        pdb = f.readlines()[0:]
        f.close()
    
        n = 0
        for line in pdb[0:]: # Start coordinate handling when the atoms start
            if line[0:4] == "ATOM":
                break
            n+=1
        
        k = 0
        self.AtomNumber1 = None
        self.AtomNumber2 = None
        
        for line in pdb[n:]:
            k +=1            
            coor = line.split()
            if str(coor[2]) == ""+str(AtomType1)+"":
                if coor[4] == ""+SteeredRes1+"":
                    print ""
                    print ""+str(coor[4])+" "+str(coor[2])+""
                    self.AtomNumber1 = k
                    print "This is the AtomNumber1 for sMD: " +str(self.AtomNumber1)+""
                    
            if str(coor[2]) == ""+str(AtomType2)+"":
                if coor[4] == ""+SteeredRes2+"":
                    print ""+str(coor[4])+" "+str(coor[2])+""
                    self.AtomNumber2 = k
                    print "This is the AtomNumber2 for sMD: " +str(self.AtomNumber2)+""
                    print ""
                    break
        if self.AtomNumber1 == None:
            print "AtomNumber1: Atom type or residue combination not found"            
            raise TypeError 
        if self.AtomNumber2 == None:
            print "AtomNumber2: Atom type or residue combination not found"            
            raise TypeError 
            
            
#        print "These are the updated sMD AtomNumbers"
#        print self.AtomNumber1
#        print self.AtomNumber2
        
#        f = open(""+root+"/README_sMD_"+str(self.AtomNumber1)+"_"+str(self.AtomNumber2)+".txt",'w')
#        f.write("This folder contains files for sMD simulations of the protein with prmtop "+protein+". The steered atoms are: "+str(SteeredRes1)+"."+str(AtomType1)+"="+str(self.AtomNumber1)+" and "+str(SteeredRes1)+"."+str(AtomType1)+"="+str(self.AtomNumber2)+"")
#        f.close()
               
class SetupAMD:
    
    def __init__(self):
      
        self.QMMM = """  ifqnt = 1,
/
&qmmm
  qmmask="""+qmmask+""",
  qmcharge="""+qmcharge+""",
  qm_theory="""+qm_theory+""",
  qmshake="""+qmshake+""",
  qm_ewald="""+qm_ewald+""",
  qm_pme="""+qm_pme+"""
/ 
"""     
        self.implicit = """  igb = """+igb+""", ntb = 0, cut = 16, """
    def FindParameters(self):
        linenumber = 0
        with open("logs/equil0.out",'r') as equilfile:
            for line in equilfile: 
#                print line
                if "NATOM" in line:
                    Atoms = line.split()
                    NumberOfAtoms = float(Atoms[2])
                    break
            for line in equilfile: #This loop runs until we get to the A V E R A G E S part.  The next loop finds the EPtot and DIHED and breaks out afterwards.
                linenumber += 1
                if "A V E R A G E S" in line:
                    break
                
            for line in equilfile:
                if "EPtot" in line:
                    print line
                    Energy = line.split()
                    EPTOT = float(Energy[8])
                if "DIHED" in line:
                    DihedralEnergy= line.split()
                    DIHED = float(DihedralEnergy[8])
                    break    #Break out of loop to avoid overwriting the EPTOT and DIHED parameters
   

       # Find the number of solute resiudes from pdb file
        with open("in_files/"+protein+"_finalLEAP_nowat.pdb",'r') as pdbfile:
            for line in pdbfile:
                if "TER" in line:
                    break
                l = line.split()
            
            if insertAnion == "on":
                NumberOfResidues = int(l[4])+1
            else:
                NumberOfResidues = int(l[4])
            
    
        EnergyAtom = 0.16
        EnergyResi = 4
        
        print "Number of atoms: "+str(NumberOfAtoms)+""
        print "Number of residues: "+str(NumberOfResidues)+""
        print "Potential Energy: "+str(EPTOT)+""
        print "Dihedral Energy: "+str(DIHED)+""
        
        self.alphaP = EnergyAtom*NumberOfAtoms
        self.EthreshP = EPTOT + self.alphaP
        
        self.alphaD = 0.2*EnergyResi*NumberOfResidues
        self.EthreshD = DIHED + 5*self.alphaD
        
        print "This is AlphaP: "+str(self.alphaP)+""
        print "This is EthreshP: "+str(self.EthreshP)+""
        
        print "This is AlphaD: "+str(self.alphaD)+""
        print "This is EthreshD: "+str(self.EthreshD)+""
        
        f = open("in_files/aMDBoostEnergies.txt",'w')
        f.write("The calculated aMD boost energies from the equil0.log file \n")
        f.write(" \n")
        f.write("The EPtot      = "+str(EPTOT)+" \n")
        f.write("The Edihed    = "+str(DIHED)+" \n")
        f.write(" \n")
        f.write("The found number of residues: "+str(NumberOfResidues)+" \n")
        f.write("EnergyAtom = "+str(EnergyAtom)+" \n")
        f.write("EnergyResi = "+str(EnergyResi)+" \n")
        f.write(" \n")
        f.write("alphaP    = EnergyAtom*NumberOfAtoms \n")
        f.write("alphaP    = "+str(EnergyAtom)+"*"+str(NumberOfAtoms)+" = "+str(self.alphaP)+" \n")
        f.write("EthreshP  = EPtot + alphaP  \n")
        f.write("EthreshP  = "+str(EPTOT)+" + "+str(self.alphaP)+" = "+str(self.EthreshP)+" \n")
        f.write(" \n")
        f.write("alphaD   = 0.2*EnergyResi*NumberOfResidues  \n")
        f.write("alphaD   = 0.2*"+str(EnergyResi)+"*"+str(NumberOfResidues)+" = "+str(self.alphaD)+" \n")
        f.write("EthreshD = Edihed + 5*alphaD \n")
        f.write("EthreshD = "+str(DIHED)+" + 5*"+str(self.alphaD)+" = "+str(self.EthreshD)+" \n")
        f.write(" \n")
        f.close()
        
    def aMD_in(self):
            #If aMD is specified then:
            
        f = open("in_files/aMD.in",'w')
        f.write(" 2 ns aMD simulation    \n")
        f.write(" &cntrl                    \n")
        f.write("  irest=1,ntx=5,    \n")
        if implicit == "on":
            f.write(""+self.implicit+"\n")
        else:
            f.write("  cut=10.0, ntb=1, ntp=0, iwrap=1,  \n")
        if timestep == "0.002":
            f.write("  nstlim=1000000,dt=0.002, \n") # Production for 1000000*0.002 ps = 2000 ps = 2 ns
        if timestep == "0.001":
            f.write("  nstlim=2000000,dt=0.001, \n") # Equilibrate for 2000000*0.001 ps = 2000 ps = 2 ns
        f.write("  ntc="+ntc+",ntf="+ntf+",ig=-1,       \n")
        f.write("  ntpr=1000, ntwx=1000,    \n")
        f.write("  ntt=3, gamma_ln=2.0,     \n")
        f.write("  temp0=300.0,ioutfm=1 \n")
        f.write("  iamd = "+iamd+", \n")
        f.write("  ethreshd="+str(round(self.EthreshD,2))+", alphad="+str(round(self.alphaD,2))+",   \n")
        f.write("  ethreshp="+str(round(self.EthreshP,2))+", alphap="+str(round(self.alphaP,2))+"     ,\n")
        if DISANG == "on":
            f.write("  nmropt = 1,                      \n")
        if QM == "on":        
            f.write(""+self.QMMM+"")
        f.write("&end\n")
        f.write("/ \n")
        if DISANG == "on":
            f.write("DISANG=distFile.RST                      \n")
        f.close()

    

def amd():
    os.chdir(""+root+"")
    aMD = SetupAMD()
    aMD.FindParameters()
    aMD.aMD_in()
    os.chdir(""+home+"")
            
    
def main():
    os.chdir(""+root+"")
    aMDsetup = SetupAMD()    
    setup = SetupInfiles()           
    
    if aMD == "on":       
         aMDsetup.FindParameters()
         aMDsetup.aMD_in()
         if DISANG == "on":
            setup.DISANG()
    if sMD == "on" and newSim == "off":
        setup.FindAtomNumbers(protein)
        setup.sMD()
    else:
#        setup.init()
        setup.setup_min()
        setup.setup_heat()
        setup.equil()
        if ""+method+"" == "cMD":
            setup.cMD()
        if sMD == "on" and newSim == "on":
            setup.FindAtomNumbers(protein)
            setup.sMD()
        if DISANG == "on":
            setup.DISANG()
                 
    os.chdir(""+home+"")    
    print "finished writing in files"
if __name__ == '__main__': main()
