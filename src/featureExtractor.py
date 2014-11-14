import os
import collections
import pickle
import features

"""
This file takes in .bed files and extracts features from it using features.py
It saves the result to pickle files for later use
"""

# Two input files, diseased or healthy in .bed format
input_diseased_bed_file = "../dbVarData/nstd100.diseased.vcf.bed"
input_healthy_bed_file = "../dbVarData/nstd100.healthy.vcf.bed"

# To loop through the files
files = [(input_diseased_bed_file, 'd'), (input_healthy_bed_file, 'h')]

# A list of feature functions. Each must take the .bed line as arguent, and return the string key that is to be set to 1
# These functions are defined in features.py and must have the same argument, return type structure
listOfFeatures = [features.chromosome, features.cnvLength, features.svType, features.overlapWithCodingExons]

# Loop through each file
for (file, result) in files:
	# Each line is a tuple of (features, result) where:
	#	features is a collection of indicator features
	# 	value is 'd' or 'h' (diseased or healthy)
	# The entire feature set is a list of these tuples
	
	data = []

	fin = open(file, 'r')
	for line in fin:
		sparseFeatures = collections.Counter()
		lineList = line.split()
		
		for featureFunc in listOfFeatures:
			key = featureFunc(lineList)
			if key: sparseFeatures[key] += 1

		# Add this entry into the set
		data.append((sparseFeatures, result))
		break

	print data
	# Save the results to pickle file
	#pickle.dump( data, open( file+"orfs.p", "wb" ) )
