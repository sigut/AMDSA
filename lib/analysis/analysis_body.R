
# Create empty lists
rdList = c()
rfList = c()
pcList = c()
hcList  = c()
cijList = c()
gsList = c()

for (i in 1:length(folderNames) ) {

    # Information for user
    print("Doing analysis on: ")
    print(folderNames[i])
    trajectoryFilepath <- paste(folderNames[i],id_dcd[i], sep="", collapse='', big=TRUE)

	print("======================================================================")
	print("======================================================================")
	print("======================================================================")

    # Read the files
    print("Reading DCD and PDB files")
    dcd <- read.dcd( trajectoryFilepath )
    pdb <- read.pdb( id_pdb[i] )

    # Get the ca of the pdb
    print("Creating list of CA atoms")
    ca.inds <- atom.select(pdb, elety="CA")

    # Fit trajectory to the pdb coords
    print("Fitting trajectory to pdb file")
    xyz <- fit.xyz(fixed=pdb$xyz, mobile=dcd,
               fixed.inds=ca.inds$xyz,
               mobile.inds=ca.inds$xyz)

    print("======================================================================")
    print("======================================================================")
    print("======================================================================")

    # Principal Component Analysis
    print("Plotting PCA analysis")
    plotFilepath <- paste(folderNames[i],"PCA.pdf", sep="", collapse='')
    pc <- pca.xyz(xyz[,ca.inds$xyz],rm.gaps=TRUE)
    pdf( plotFilepath, width=10, height=5 )
    plot(pc, col=bwr.colors(nrow(xyz)) )
    dev.off()

    #print("Plotting PCA V.2.00 analysis")
    #plotFilepath <- paste(folderNames[i],"PCA_2.pdf", sep="", collapse='')
    #hc <- hclust(dist(pc$z[,1:2]))
    #grps <- cutree(hc, k=2)
    #pdf( plotFilepath, width=10, height=5 )
    #	plot(pc, col=grps)
    #	dev.off()

    print("Plotting the 3 first principal components")
    plotFilepath <- paste(folderNames[i],"First3PC.pdf", sep="", collapse='')
    pdf( plotFilepath, width=10, height=5 )	
	plot.bio3d(pc$au[,1], ylab="PC1 (A)", xlab="Residue Position", typ="l")
	points(pc$au[,2], typ="l", col="blue")
	points(pc$au[,3], typ="l", col="green")
	dev.off()

    # Save trajectory of PC1 and PC2
    pc1Path <- paste(folderNames[i],"pc1_movement.pdb", sep="", collapse='')
    pc2Path <- paste(folderNames[i],"pc2_movement.pdb", sep="", collapse='')
    pc3Path <- paste(folderNames[i],"pc3_movement.pdb", sep="", collapse='')
    p1 <- mktrj.pca(pc, pc=1, file=pc1Path)
    p2 <- mktrj.pca(pc, pc=2, file=pc2Path)
    p3 <- mktrj.pca(pc, pc=3, file=pc3Path)

    # Run RMSD analysis
    print("Plotting RMSD analysis")
    plotFilepath <- paste(folderNames[i],"rmsd.pdf", sep="", collapse='')
    rd <- rmsd(xyz[1,ca.inds$xyz], xyz[,ca.inds$xyz]) 
    pdf( plotFilepath, width=10, height=5 )
    plot(rd, typ="l", ylab="RMSD", xlab="Frame No.")
    points(lowess(rd), typ="l", col="red", lty=2, lwd=2)
    dev.off()

    # Plot RMSD histograms
    print("Plotting RMSD Histograms")
    plotFilepath <- paste(folderNames[i],"rmsd_Histogram.pdf", sep="", collapse='')
    pdf( plotFilepath, width=10, height=5 )
    hist(rd, breaks=40, freq=FALSE, main="RMSD Histogram", xlab="RMSD")
    lines(density(rd), col="gray", lwd=3)
    dev.off()

	# Plot RMSF
    print("Plotting RMSF analysis")
    plotFilepath <- paste(folderNames[i],"rmsf.pdf", sep="", collapse='')
	rf <- rmsf(xyz[,ca.inds$xyz])
    pdf( plotFilepath, width=10, height=5 )
	plot(rf, ylab="RMSF", xlab="Residue Position", typ="l")
    dev.off()

	#Atomic Displacements:
    write.ncdf(p1,  paste(folderNames[i],"trj_pc1.nc", sep="", collapse=''))
    write.ncdf(p2,  paste(folderNames[i],"trj_pc2.nc", sep="", collapse=''))
    write.ncdf(p3,  paste(folderNames[i],"trj_pc3.nc", sep="", collapse=''))



	# Cross-Correlation Analysis
    print("Plotting Cross-Correlation Analysis")
    plotFilepath <- paste(folderNames[i],"Cross-Correlation.pdf", sep="", collapse='')
    pdf( plotFilepath, width=10, height=5 )	
	cij<-dccm(xyz[,ca.inds$xyz])
	plot(cij)
	dev.off()

	# View the cross-correlations in pymol
    savePrefix <- paste(folderNames[i],"correlation", sep="", collapse='')
    view.dccm( cij, pdb, launch=FALSE, radius=0.1, step=0.2, omit=0.4 )

	

    # Move the pymol files to the resultsDir of the case. Run by opening pymol in resultsDir and typing "run corr.py"
    file.rename("corr.py", paste(folderNames[i],"corr.py", sep="", collapse=''))
    file.rename("corr.inpcrd.pdb", paste(folderNames[i],"corr.inpcrd.pdb", sep="", collapse=''))
	

    # Save data for multi plotting
	#print("Save iteration data")
	#rdList <- list( rdList, list(rd) )
	#rfList <- list( rfList, list(rf) )
	#pcList <- list( pcList, list(pc) )
	#hcList  <- list( hcList, list(hc) )
	#cijList <- list( cijList, list(cij) )
	#gsList <- list( gsList, list(gs) )

}




