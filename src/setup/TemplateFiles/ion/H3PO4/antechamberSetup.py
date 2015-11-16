import os

# Define files to treat
filesToTreat = { 
#	"HPO4": {
#		"name": "HPO4",
#		"charge": -2
#	},
#	"H2PO4": {
#		"name": "H2PO4",
#		"charge": -1
#	}
	
	"H3PO4d": {
		"name": "H3PO4d",
		"charge": 0
	},
	"H3PO4s": {
		"name": "H3PO4s",
		"charge": 0
	}
}

# Go through files to treat
for pdbfile,dictionary in filesToTreat.items():

	###########################
	# Go through http://ambermd.org/tutorials/basic/tutorial4b/
	###########################

	# Reduce command
	query = "reduce "+dictionary['name']+".pdb > "+dictionary['name']+"_h.pdb"
	print "Now running: "+query
	os.system(query)

	# Line separation
	print "\n\n\n\n"

	# Create mol2 files
	query = "antechamber -i "+dictionary['name']+"_h.pdb -fi pdb -o "+dictionary['name']+".mol2 -fo mol2 -c mul -s 2 -nc "+str(dictionary['charge'])
	print "Now running: " + query
	os.system( query )

	# Line separation
	print "====================== \n\n\n\n"

# Clean up temp files
#os.system("rm -rf ANTECHAMBER_*")
#os.system("rm *~ sqm.* ATOMTYPE.INF")

