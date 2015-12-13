import os

# INFO
# This script cleans up the .pdb files, removing certain residues and linking cysteines to each other
# It also saves given "gaff" residues in separate pdb files.

# Easy variables

import argparse

#Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--protein',
                    help = 'Specify the Protein by typing in the file name, for instance: ClosedProtein.pdb',
                    default = "OpenProtein.pdb")
args = parser.parse_args()
protein = args.protein

dontinclude = ["EDO", "SO4"," PI"]
cyxresidues = ["1114","1159","1300","1363"]
gaffResidues = [" PI"]

# Setup to run
cases = {
	""+protein+"": {
		"dontinclude": dontinclude,
		"cyxresidues": cyxresidues,
		"gaff": gaffResidues	
	},
#	"4F1U": {
#		"dontinclude": dontinclude,
#		"cyxresidues": cyxresidues,
#		"gaff": gaffResidues	
#	}
}

# Go through the cases
for pdbfile,dictionary in cases.items():

	# Open files for gaff residues
	gaffFiles = {}
	for gaffResidue in dictionary['gaff']:
		gaffFiles[ gaffResidue ] = open( pdbfile + "_" + gaffResidue.replace(" ","") + ".pdb" , "w")
	
	# Open the pdb file
	with open(pdbfile +".pdb","r") as fi:

		# The readout file
		with open(pdbfile + "_cleaned.pdb","w") as fo:

			# Go through the lines
			for line in fi.readlines():

				# Check if we want to include this line in cleaned output
				if "ANISOU" not in line and \
					line[16] != "B" and \
					line[16] != "C" and \
					"MASTER" not in line and \
					"REMARK" not in line and \
					"CONECT" not in line:

					# Check if we're including this residue
					if line[17:20] not in dictionary['dontinclude'] and line[77] != "H":

						# Remove the A from the residue name
						if line[16] == "A":
							temp = list(line)
							temp[16] = " "
							line = "".join(temp)

						# Change CYS residues to CYX
						if line[17:20] == "CYS":
							line = line.replace("CYS","CYX")

						# Write cleaned file
						fo.write( line )

					# Check if residue should be treated with gaff
					if line[17:20] in dictionary['gaff']:
						
						# Write to the correct file
						gaffFiles[ line[17:20] ].write( line )

						
