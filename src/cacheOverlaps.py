import os
import collections
import pickle
import random

"""
This converts overlap results to easy to searh python objects
"""
overlapSelectPath = "../../../tools/overlapSelect"

# Two input files, diseased or healthy in .bed format
input_diseased_bed_file = "../dbVarData/nstd100.diseased.vcf.bed"
input_healthy_bed_file = "../dbVarData/nstd100.healthy.vcf.bed"
inoutFiles = [(input_diseased_bed_file,"diseased"),(input_healthy_bed_file,"healthy")]

# All the foldernames that have overlap .bed files
folders = ["knownGeneCodingExons"]
for folder in folders:
	path = "../overlapBEDFiles/%s" % folder
	fileToOverlapWith = "%s/baseToOverlapWith.bed" % path
	for (inputFile, outputFile) in inoutFiles:
		# Run the overlapSelect to get the overlap files
		output = "%s/%s.bed" % (path, outputFile)
		try:
			print "Command: %s %s %s %s" % (overlapSelectPath, fileToOverlapWith, inputFile, output)
			os.system('%s %s %s %s' % (overlapSelectPath, fileToOverlapWith, inputFile, output))
		except IOError:
			print "Error with command: %s %s %s %s" % (overlapSelectPath, fileToOverlapWith, inputFile, output)
		# Now read in the overlap files and convert them to python Counter, with uniqueID=>#Overlaps
		fin = open(output, 'r')
		data = Counter()
		for line in fin:
			metaList = line.split()[3].split(";")
			uniqueId = metaList[1]
			data[uniqueId] += 1
		# Save pickle file for later use
		outputPickleFile = "%s/%s.p" % (path, outputFile)
		pickle.dump(data, open(outputPickleFile, "wb" ))