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

# A list of feature extracting functions (one for each feature). 
# Each must take the .bed line as argument, and return a list of (key, value) tuples
# These functions are defined in features.py and must have the same argument and return type structure
#listOfFeatures = [features.overlapWithMicroSats, features.overlapWithKnownGenes, features.overlapWithVistaEnhancer, features.overlapWithCodingExons, features.chromosome, features.cnvLength, features.logOfLength, features.svType, features.overlapWithKnownGenesIndicatorPerGene]

listOfFeatures = [features.overlapWithCodingExons, features.chromosome, features.cnvLength, features.svType]

# Two input files, diseased or healthy in .bed format
input_diseased_bed_file = "../dbVarData/nstd100.diseased.vcf.bed"
input_healthy_bed_file = "../dbVarData/nstd100.healthy.vcf.bed"
# To loop through the two files
files = [(input_diseased_bed_file, 1.0), (input_healthy_bed_file, -1.0)]

# To save the results (sparse representation of features)
dataTesting = []
dataTraining = []

violinTraining = open('violinTraining.bed', 'w')
violinTesting = open('violinTesting.bed', 'w')

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

		startPos = int(lineList[1])
		chrom = lineList[0]
		violinLine = "%s\t%s\t%s\n" % (chrom, startPos, result)
		
		# For each feature extraction function, run it on this input line
		for featureFunc in listOfFeatures:
			features = featureFunc(lineList)
			if features:
				for feature in features:
					(key, value) = feature
					if key: sparseFeatures[key] = value

		# Add this entry into the training or testing set
		if(random.randint(1,100) <= PercentageOfSetForTraining):
			dataTraining.append((sparseFeatures, result))
			violinTraining.write(violinLine)
		else:
			dataTesting.append((sparseFeatures, result))
			violinTesting.write(violinLine)

violinTesting.close()
violinTraining.close()

# Save the results to pickle files for later use
pickle.dump(dataTraining, open("trainingSet.p", "wb"))	
pickle.dump(dataTesting, open("testingSet.p", "wb"))
