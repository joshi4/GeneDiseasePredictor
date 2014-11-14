import os

"""
This file has a function for each feature that we want to extract

They must follow the structure:

argument: 1 argument being the information in the bed line, split by whitespace (a list)
return: a key string that must be set to 1.
"""

overlapSelectPath = "../../tools/overlapSelect"

def chromosome(bedLine):
	"""
	Chromosome number feature.
	Example keys:
	"chrom1" or "chrom2" or "chrom20"
	"""
	chrom = bedLine[0].lower()
	return chrom


# TODO, need to calculate better thresholds for length, use histogram to equally seperate them?
def cnvLength(bedLine):
	"""
	Length of CNV, grouped into 5 equally sized groups
	"""
	start = int(bedLine[1])
	end = int(bedLine[2])
	length = end - start
	if length < 1000:
		return "lessThan1,000"
	elif length < 10000:
		return "lessThan10,000"
	elif length < 100000:
		return "lessThan100,000"
	elif length < 500000:
		return "lessThan500,000"
	elif length < 1000000:
		return "lessThan1000,000"
	else:
		return "greaterThan1000,000"


def svType(bedLine):
	"""
	The type of CNV change - insertion or duplicate or deletion
	"""
	svType = bedLine[3].lower()
	return 


def overlapWithCodingExons(bedLine):
	"""
	This checks if the CNV overlaps with any known coding exons
	"""
	fileToOverlapWith = "../overlapBEDFiles/knownGenesCodingExons.bed"
	# Run overlapSelect
	numberOverlaps = checkOverlap(bedLine, fileToOverlapWith)
	if numberOverlaps > 0:
		return "overlapsWithCodingExcons"


def checkOverlap(bedLine, fileToOverlapWith):
	"""
	General function to check the number of overlaps between two files
	"""

	# First create a temporary one line .bed file
	tempFile = "temp.bed"
	fout = open(tempFile, 'w')
	line = "\t".join(bedLine[:-1])+"\n"
	fout.write(line)
	fout.close()
	outputFile = "result.bed"
	os.system('%s %s %s %s' % (overlapSelectPath, fileToOverlapWith, tempFile, outputFile))

	try:
		numberOfOverlapLines = sum(1 for line in open(outputFile))
		os.system('rm -f %s %s' % (outputFile, tempFile))
		return numberOfOverlapLines
	except IOError:
		os.system('rm -f %s' % (tempFile))
		print "Error with command: %s %s %s %s" % (overlapSelectPath, fileToOverlapWith, tempFile, outputFile)
		return 0




