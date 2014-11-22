import os
import pickle

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
		return ("greaterThan1000,000", 1)


def svType(bedLine):
	"""
	The type of CNV change - insertion or duplicate or deletion
	"""
	info = bedLine[3].split(";")
	svType = info[0].lower()
	return (svType, 1)


diseasedOverlapWithExons = pickle.load(open('../overlapBEDFiles/knownGenesCodingExons/diseased.p' ,'rb'))
healthyOverlapWithExons = pickle.load(open('../overlapBEDFiles/knownGenesCodingExons/healthy.p' ,'rb'))
def overlapWithCodingExonsFastest(bedLine):
	info = bedLine[3].split(";")
	uniqeId = info[1]
	numOverlaps = diseasedOverlapWithExons[uniqeId]
	numOverlaps += healthyOverlapWithExons[uniqeId]
	if numOverlaps > 0:
		return ("overlapsWithCodingExons", numOverlaps)
	else:
		return False