import os
import collections
import pickle
import features
import random

"""
This file takes in .bed files and extracts features from it using features.py
It also splits the results into a testing set and a training set, based on |PercentageOfSetForTraining|
It saves the result to pickle files:
trainingSet.p
testingSet.p
"""

PercentageOfSetForTraining = 80 # A percentage

# Two input files, diseased or healthy in .bed format
input_diseased_bed_file = "../dbVarData/nstd100.diseased.vcf.bed"
input_healthy_bed_file = "../dbVarData/nstd100.healthy.vcf.bed"

# To loop through the files
files = [(input_diseased_bed_file, 1.0), (input_healthy_bed_file, -1.0)]

# A list of feature extracting functions (one for each feature). 
# Each must take the .bed line as argument, and return the key that is to be set to 1
# These functions are defined in features.py and must have the same argument and return type structure
listOfFeatures = [features.chromosome, features.cnvLength, features.svType, features.startPosition, features.endPosition]
BaseLineFeatures = [features.overlapWithBroadEnhancer, features.overlapWithVistaEnhancer, features.overlapWithCodingExons, features.chromosome, features.cnvLength, features.svType]

dataTesting = []
dataTraining = []

# Loop through each file
for (file, result) in files:
	# Each line is a tuple of (features, result) where:
	#	features is a collection of features (sparse representation)
	# 	value is 'd' or 'h' (diseased or healthy)
	# The entire feature set is a list of these tuples

	counter = 0
	fin = open(file, 'r')
	for line in fin:

		# Temp, TODO, remove this
		#counter += 1
		#if counter >=20: break

		sparseFeatures = collections.Counter()
		lineList = line.split()
		
		for featureFunc in BaseLineFeatures: #BaselineFeatures
			feature = featureFunc(lineList)
			if feature:
				(key, value) = feature
				if key: sparseFeatures[key] = value

		# Add this entry into the training/testing set
		if(random.randint(1,100) <= PercentageOfSetForTraining):
			dataTraining.append((sparseFeatures, result))
		else:
			dataTesting.append((sparseFeatures, result))
		# print (sparseFeatures, result)

#print "Training data: %s " % dataTraining
#print "Testing data: %s " % dataTesting
# Save the results to pickle files
pickle.dump(dataTraining, open("trainingSet.p", "wb" ))	
pickle.dump(dataTesting, open("testingSet.p", "wb" ))
