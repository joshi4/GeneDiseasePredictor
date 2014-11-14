import os
import collections
import pickle
import features
import random

"""
This file takes in .bed files and extracts features from it using features.py
It saves the result to pickle files for later use
"""

FractionOfSetForTraining = 80 # A percentage

# Two input files, diseased or healthy in .bed format
input_diseased_bed_file = "../dbVarData/nstd100.diseased.vcf.bed"
input_healthy_bed_file = "../dbVarData/nstd100.healthy.vcf.bed"

# To loop through the files
files = [(input_diseased_bed_file, 'd'), (input_healthy_bed_file, 'h')]

# A list of feature extracting functions (one for each feature). 
# Each must take the .bed line as argument, and return the string key that is to be set to 1
# These functions are defined in features.py and must have the same argument and return type structure
listOfFeatures = [features.chromosome, features.cnvLength, features.svType, features.overlapWithCodingExons]

dataTesting = []
dataTraining = []

# Loop through each file
counter = 0
for (file, result) in files:
	# Each line is a tuple of (features, result) where:
	#	features is a collection of features (sparse representation)
	# 	value is 'd' or 'h' (diseased or healthy)
	# The entire feature set is a list of these tuples
	
	# Temp, TODO, remove this
	counter += 1
	if counter >=5: break

	fin = open(file, 'r')
	for line in fin:
		sparseFeatures = collections.Counter()
		lineList = line.split()
		
		for featureFunc in listOfFeatures:
			key = featureFunc(lineList)
			if key: sparseFeatures[key] += 1

		# Add this entry into the set
		if(random.randint(1,100) <= FractionOfSetForTraining):
			dataTraining.append((sparseFeatures, result))
		else:
			dataTesting.append((sparseFeatures, result))
		print (sparseFeatures, result)


print dataTraining
print dataTesting
# Save the results to pickle files
pickle.dump(dataTraining, open("trainingSet.p", "wb" ))
pickle.dump(dataTesting, open("testingSet.p", "wb" ))