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
	Chromosome number feature. (indicator variable)
	Example keys:
	"chrom1" or "chrom2" or "chrom20"
	"""
	chrom = bedLine[0].lower()
	return (chrom, 1)

def absoluteStartPosition(bedLine):
	"""
	Creates a feature for the start position of the CNV in the entire genome.
	"""
	start = int(bedLine[1])
	chrom = bedLine[0].lower()
	chromSizes = {
		"chr1",  249250621
		"chr2",  243199373
		"chr3",  198022430
		"chr4",  191154276
		"chr5",  180915260
		"chr6",  171115067
		"chr7",  159138663
		"chrX",  155270560
		"chr8",  146364022
		"chr9",  141213431
		"chr10", 135534747
		"chr11", 135006516
		"chr12", 133851895
		"chr13", 115169878
		"chr14", 107349540
		"chr15", 102531392
		"chr16", 90354753
		"chr17", 81195210
		"chr18", 78077248
		"chr20", 63025520
		"chrY",  59373566
		"chr19", 59128983
		"chr22", 51304566
		"chr21", 48129895
	}
	totalStartPos = 0
	for (index, value) in enumerate(chromSizes):
		if(index == chrom): break
		else: totalStartPos += value 
	totalStartPos += start
	return ("startAbsolute", totalStartPos)

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
def overlapWithCodingExons(bedLine):
	"""
	
	"""
	info = bedLine[3].split(";")
	uniqeId = info[1]
	numOverlaps = diseasedOverlapWithExons[uniqeId]
	numOverlaps += healthyOverlapWithExons[uniqeId]
	if numOverlaps > 0:
		return ("overlapsWithCodingExons", numOverlaps)
	else:
		return False

diseasedOverlapWithRegulatoryVistaEnhancers = pickle.load(open('../overlapBEDFiles/RegulatoryVistaEnhancers/diseased.p' ,'rb'))
healthyOverlapWithRegulatoryVistaEnhancers = pickle.load(open('../overlapBEDFiles/RegulatoryVistaEnhancers/healthy.p' ,'rb'))
def overlapWithVistaEnhancer(bedLine):
	"""
	
	"""
	info = bedLine[3].split(";")
	uniqeId = info[1]
	numOverlaps = diseasedOverlapWithRegulatoryVistaEnhancers[uniqeId]
	numOverlaps += healthyOverlapWithRegulatoryVistaEnhancers[uniqeId]
	if numOverlaps > 0:
		return ("overlapWithVistaEnhancer", numOverlaps)
	else:
		return False

diseasedOverlapWithRegulatoryBroadEnhancers = pickle.load(open('../overlapBEDFiles/RegulatoryBroadEnhancers/diseased.p' ,'rb'))
healthyOverlapWithRegulatoryBroadEnhancers = pickle.load(open('../overlapBEDFiles/RegulatoryBroadEnhancers/healthy.p' ,'rb'))
def overlapWithBroadEnhancer(bedLine):
	"""
	
	"""
	info = bedLine[3].split(";")
	uniqeId = info[1]
	numOverlaps = diseasedOverlapWithRegulatoryBroadEnhancers[uniqeId]
	numOverlaps += healthyOverlapWithRegulatoryBroadEnhancers[uniqeId]
	if numOverlaps > 0:
		return ("overlapWithBroadEnhancer", numOverlaps)
	else:
		return False

diseasedOverlapWithKnownGenes = pickle.load(open('../overlapBEDFiles/KnownGenes/diseased.p' ,'rb'))
healthyOverlapWithKnownGenes = pickle.load(open('../overlapBEDFiles/KnownGenes/healthy.p' ,'rb'))
def overlapWithKnownGenes(bedLine):
	"""
	
	"""
	info = bedLine[3].split(";")
	uniqeId = info[1]
	numOverlaps = diseasedOverlapWithKnownGenes[uniqeId]
	numOverlaps += healthyOverlapWithKnownGenes[uniqeId]
	if numOverlaps > 0:
		return ("overlapWithGene", numOverlaps)
	else:
		return False

diseasedOverlapWithMicroSeq = pickle.load(open('../overlapBEDFiles/Microsatellites/diseased.p' ,'rb'))
healthyOverlapWithMicroSeq = pickle.load(open('../overlapBEDFiles/Microsatellites/healthy.p' ,'rb'))
def overlapWithMicroSats(bedLine):
	"""
	
	"""
	info = bedLine[3].split(";")
	uniqeId = info[1]
	numOverlaps = diseasedOverlapWithMicroSeq[uniqeId]
	numOverlaps += healthyOverlapWithMicroSeq[uniqeId]
	if numOverlaps > 0:
		return ("overlapWithMicroSeq", numOverlaps)
	else:
		return False

diseasedOverlapWithKnownRepeats = pickle.load(open('../overlapBEDFiles/KnownRepeats/diseased.p' ,'rb'))
healthyOverlapWithKnownRepeats = pickle.load(open('../overlapBEDFiles/KnownRepeats/healthy.p' ,'rb'))
def overlapWithKnownRepeats(bedLine):
	"""

	"""
	info = bedLine[3].split(";")
	uniqeId = info[1]
	numOverlaps = diseasedOverlapWithKnownRepeats[uniqeId]
	numOverlaps += healthyOverlapWithKnownRepeats[uniqeId]
	if numOverlaps > 0:
		return ("overlapWithKnownRepeatSeq", numOverlaps)
	else:
		return False