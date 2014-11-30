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

# The dataset is split into training and testing sets
PercentageOfSetForTraining = 80 # A percentage

# Two input files, diseased or healthy in .bed format
input_diseased_bed_file = "../dbVarData/nstd100.diseased.vcf.bed"
input_healthy_bed_file = "../dbVarData/nstd100.healthy.vcf.bed"

# To loop through the two files
files = [(input_diseased_bed_file, 1.0), (input_healthy_bed_file, -1.0)]

# A list of feature extracting functions (one for each feature). 
# Each must take the .bed line as argument, and return the key that is to be set to 1
# These functions are defined in features.py and must have the same argument and return type structure
listOfFeatures = [features.absoluteStartPosition, features.overlapWithKnownRepeats, features.overlapWithMicroSats, features.overlapWithKnownGenes, features.overlapWithVistaEnhancer, features.overlapWithCodingExons, features.chromosome, features.cnvLength, features.svType]

# To save the results (sparse representation of features)
dataTesting = []
dataTraining = []

# Loop through each file (healthy & diseased)
for (file, result) in files:
	# Each line is a tuple of (features, result) where:
	#	features is a collection of features (sparse representation)
	# 	value is '1.0' or '-1.0' (diseased or healthy)
	# The entire feature set is a list of these tuples

	counter = 0
	fin = open(file, 'r')
	for line in fin:

		sparseFeatures = collections.Counter()
		lineList = line.split()
		
		# For each feature extraction function, run it on this input line
		for featureFunc in listOfFeatures:
			feature = featureFunc(lineList)
			if feature:
				(key, value) = feature
				if key: sparseFeatures[key] = value

		# Add this entry into the training or testing set
		if(random.randint(1,100) <= PercentageOfSetForTraining):
			dataTraining.append((sparseFeatures, result))
		else:
			dataTesting.append((sparseFeatures, result))

# Save the results to pickle files for later use
pickle.dump(dataTraining, open("trainingSet.p", "wb"))	
pickle.dump(dataTesting, open("testingSet.p", "wb"))