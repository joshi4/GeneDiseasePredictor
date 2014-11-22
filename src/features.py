import os

"""
This file has a function for each feature that we want to extract

They must follow the structure:

argument: 1 argument being the information in the bed line, split by whitespace (a list)
return: a (key, value) tuple where key is the key and value is the features value (this is 1 for indicator variables)
"""

overlapSelectPath = "../../../tools/overlapSelect"

def startPosition(bedLine):
	"""
	"""
	start = int(bedLine[1])
	return ("start", start)

def endPosition(bedLine):
	"""
	"""
	end = int(bedLine[2])
	return ("end", end)

def chromosome(bedLine):
	"""
	Chromosome number feature.
	Example keys:
	"chrom1" or "chrom2" or "chrom20"
	"""
	chrom = bedLine[0].lower()
	return (chrom, 1)

def length(bedLine):
	"""
	"""
	start = int(bedLine[1])
	end = int(bedLine[2])
	length = end - start
	return ("length", length)

# TODO, need to calculate better thresholds for length, use histogram to equally seperate them?
def cnvLength(bedLine):
	"""
	Length of CNV, grouped into 5 equally sized groups* Still need to work out group thresholds
	"""
	start = int(bedLine[1])
	end = int(bedLine[2])
	length = end - start
	if length < 1000:
		return ("lessThan1,000", 1)
	elif length < 10000:
		return ("lessThan10,000", 1)
	elif length < 100000:
		return ("lessThan100,000", 1)
	elif length < 500000:
		return ("lessThan500,000", 1)
	elif length < 1000000:
		return ("lessThan1000,000", 1)
	else:
		return ("greaterThan1,000,000", 1)


def svType(bedLine):
	"""
	The type of CNV change - insertion or duplicate or deletion
	"""
	info = bedLine[3].split(";")
	svType = info[0].lower()
	return (svType, 1)

def overlapWithCodingExonsFast(bedLine):
	"""
	This checks if the CNV overlaps with any known coding exons
	"""

	fileWithOverlaps = "../overlapBEDFiles/knownGenesCodingExons/knownGenesCodingExons-healthy.bed"
	numberOverlaps = checkOverlapUsingFile(bedLine, fileWithOverlaps)
	fileWithOverlaps = "../overlapBEDFiles/knownGenesCodingExons/knownGenesCodingExons-disease.bed"
	numberOverlaps += checkOverlapUsingFile(bedLine, fileWithOverlaps)
	if numberOverlaps > 0:
		return ("overlapsWithCodingExcons", 1)
	else:
		return False

def overlapWithCodingExons(bedLine):
	"""
	This checks if the CNV overlaps with any known coding exons
	"""
	fileToOverlapWith = "../overlapBEDFiles/knownGenesCodingExons/knownGenesCodingExons.bed"
	# Run overlapSelect
	numberOverlaps = checkOverlap(bedLine, fileToOverlapWith)
	if numberOverlaps > 0:
		return ("overlapsWithCodingExcons", numberOverlaps)
	else:
		return False


def checkOverlapUsingFile(bedLine, fileWithOverlaps):
	"""
	General function that searches a |fileWithOverlaps| for the ID in |bedLine|
	|fileWithOverlaps| is a precomputed overlap file
	"""
	info = bedLine[3].split(";")
	ID = info[1]
	resultsFile = "tempResults.bed"
	try:
		os.system("grep '%s' %s > %s" % (ID, fileWithOverlaps, resultsFile))
		numberOfOverlapLines = sum(1 for line in open(resultsFile))
		return numberOfOverlapLines
	except IOError:
		return 0;

def checkOverlap(bedLine, fileToOverlapWith):
	"""
	General function to check the number of overlaps between our bed enrty |bedLine| and another .bed file |fileToOverlapWith|
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




