import os
import collections
import pickle
import random
from sets import Set

overlapSelectPath = "../../../tools/overlapSelect"

# Two input files, diseased or healthy in .bed format
input_diseased_bed_file = "../dbVarData/nstd100.diseased.vcf.bed"
input_healthy_bed_file = "../dbVarData/nstd100.healthy.vcf.bed"
inoutFiles = [(input_diseased_bed_file, "diseased"),(input_healthy_bed_file, "healthy")]

def cacheGeneralIndicatorOverlaps():
	"""
	This converts overlap results to easy to searh python objects before running the feature extraction step (featureExtractor.py)


	"""
	# All the foldernames that have overlap .bed files
	folders = ["knownGenesCodingExons", "RegulatoryBroadEnhancers", "RegulatoryVistaEnhancers", "KnownGenes", "Microsatellites"]
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
			data = collections.Counter()
			for line in fin:
				metaList = line.split()[3].split(";")
				uniqueId = metaList[1]
				data[uniqueId] += 1
			# Save pickle file for later use
			outputPickleFile = "%s/%s.p" % (path, outputFile)
			pickle.dump(data, open(outputPickleFile, "wb" ))
			# Remove temp .bed file
			os.system('rm %s' % (output))


def cacheKnownGeneIndicatorsPerGene():
	"""
	Now do overlaps for 1 feature PER Gene

	This Uses overlapSelect with -mergeOutput option
	"""

	path = "../overlapBEDFiles/KnownGenes"
	fileToOverlapWith = "%s/baseToOverlapWith.bed" % (path)
	newTempFile = "%s/temp.bed" % (path)
	# First cut the KnownGenes.bed file to remove uneccessary columns
	os.system('cut -f 1-4 %s > %s' % (fileToOverlapWith, newTempFile))
	for (inputFile, outputFile) in inoutFiles:
		output = "%s/%sMerged.bed" % (path, outputFile)
		try:
			os.system('%s %s %s %s -mergeOutput' % (overlapSelectPath, newTempFile, inputFile, output))
		except IOError:
			print "Error with command: %s %s %s %s -mergeOutput" % (overlapSelectPath, newTempFile, inputFile, output)
		# Now read in the merged overlap files and convert them to python Counter
		fin = open(output, 'r')
		data = {}
		for line in fin:
			# Get the entry unique ID
			metaList = line.split()[3].split(";")
			uniqueId = metaList[1]
			# Get the genes names it overlaps with
			lineList = line.split()
			colIndex = 3
			while( (len(lineList)-1) > colIndex ):
				colIndex += 4
				overlappedGeneName = lineList[colIndex]
				if uniqueId in data:
					data[uniqueId].add(overlappedGeneName)
				else:
					data[uniqueId] = Set([overlappedGeneName])

		# Save pickle file for later use
		outputPickleFile = "%s/%sMerged.p" % (path, outputFile)
		pickle.dump(data, open(outputPickleFile, "wb" ))
		# Remove temp .bed file
		os.system('rm %s' % (output))
	os.system('rm %s' % (newTempFile))

if __name__ == "__main__":
	cacheGeneralIndicatorOverlaps()
	cacheKnownGeneIndicatorsPerGene()
