trainingBED = "../training.bed"
testingAdverseBED = "../testingAdverse.bed"
testingBenignBED = "../testingBenign.bed"


def checkBenign():
	numIncorrectBenign = 0
	totalCount = 0
	maxIterations = 100
	with open(testingBenignBED) as f:
		for line in f:
			lineList = line.split()
			if(len(lineList)):
				try:
					chromosome = int(lineList[0])
					startPos = int(lineList[1])
					endPos = int(lineList[2])
					
					if totalCount < maxIterations:
						totalCount += 1
						# Now check for a match in training file using awk
						with open(trainingBED) as trainLines:
							for trainLine in trainLines:
								trainList = trainLine.split()
								if len(trainList) > 0 and isinstance( int(trainList[0]), int ):
									if trainList[0] == chromosome:
										if (startPos < int(trainList[2]) and startPos > int(trainList[1])) or (endPos < int(trainList[2]) and endPos > int(trainList[1])):
											numIncorrectBenign += 1
											print "Found an overlap of %s with %s " % (line, trainLine)
											break
				except ValueError:
					print "error"			

	print "Benign incorrect: %f " % ((float(numIncorrectBenign)/totalCount)*100)

def checkAdverse():
	numIncorrectAdverse = 0
	totalCount = 0
	maxIterations = 1000
	with open(testingAdverseBED) as f:
		for line in f:
			lineList = line.split()
			if(len(lineList)):
				try:
					chromosome = int(lineList[0])
					startPos = int(lineList[1])
					endPos = int(lineList[2])
					
					if totalCount < maxIterations:
						totalCount += 1
						# Now check for a match in training file using awk
						isCorrect = False
						with open(trainingBED) as trainLines:
							for trainLine in trainLines:
								trainList = trainLine.split()
								if len(trainList) > 0 and isinstance( int(trainList[0]), int ):
									if int(trainList[0]) == chromosome:
										if (startPos < int(trainList[2]) and startPos > int(trainList[1])) or (endPos < int(trainList[2]) and endPos > int(trainList[1])):
											isCorrect = True
											print "Found an overlap of %s with %s " % (line, trainLine)
											break
						if not isCorrect:
							numIncorrectAdverse += 1
				except ValueError:
					print "error"	

	if totalCount > 0:
		print "Adverse incorrect: %.2f " % ((float(numIncorrectAdverse)/float(totalCount))*100)

checkBenign()
checkAdverse()