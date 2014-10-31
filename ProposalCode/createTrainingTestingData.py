import random

# Read from files
adverseBED = "../dbVarData/diseased.bed"
benignBED = "../BenignData/benignSimple.bed"
trainingBED = "../training.bed"
testingAdverseBED = "../testingAdverse.bed"
testingBenignBED = "../testingBenign.bed"


trainingFileHandler = open(trainingBED, 'w')
testingAdverseFileHandler = open(testingAdverseBED, 'w')
testingBenignFileHandler = open(testingBenignBED, 'w')

with open(adverseBED) as f:
	for line in f:
		if(random.randint(1,10) == 10):
			# Print to training file
			testingAdverseFileHandler.write(line)
		else:
			# Print to testing file
			trainingFileHandler.write(line)
with open(benignBED) as f:
	for line in f:
		if(random.randint(1,10) == 10):
			# Print to training file
			testingBenignFileHandler.write(line)

testingAdverseFileHandler.close()
testingBenignFileHandler.close()
trainingFileHandler.close()