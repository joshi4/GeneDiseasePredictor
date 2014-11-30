import pickle
import collections
import math
import util
import random
import sys
from utils import *


##################################
'''
K-means implementation for CNV classfication. More detailed comments in the kmeans
and helper functions below. 

Summary: 12 clusters and 10 iterations. Have adjusted for data set proportions
(10% diseased and 90% healthy). Training and testing data is using Justin's first
feature vector extractor, which contains a mix of indicator variables and large integers. 

Preliminary error rate is 32% and total cost averages to around 800.
I think our new feature vector will lower this error rate, however.
The indicator variables are effectively being ignored, because of the huge numbers in columns 
such as 'start' or 'end', which give the offset in number of nucleotides
from the beginning of the chromosome. The distance metric used to calculate nearest cluster
and total cost is meant to only work with indicator variables, so let's hope that cleans up
the results a little!
'''
#################################


pickledTrainingFile = "./trainingSet.p"
pickledTestingFile = "./testingSet.p"
K_CONST = 12
MAX_ITERS = 10

#calculates magnitude of a feature vector
def magnitude(dic):
	totalSum = 0
	for key, value in dic.iteritems():
		totalSum += value * value
	return math.sqrt(totalSum)

#helper function for findLoss. Uses cosine similarity algorithm
def scoreVectors(example, center, centerMag):
	# Error checking hack... Obviously if the example and cluster are the same,
	# we want to return a distance of 0. If we omit this check, we will end up
	# with a cosineSimilarity of 1. The arcosine is undifined, so an exception is
	# thrown. I found this to be an effective workaround.
	if example == center:
		return 0
	#####################################################

	dtpdt = dotProduct(example, center) #from utils.py (copied from 221 assinment folder)
	magA = magnitude(example)
	if magA == 0 or centerMag == 0:
		return float('Inf')
	cosineSimilarity = (dtpdt)/(magA * centerMag)	#from Wikipedia
	try:
		result = 2*(math.acos(cosineSimilarity)/math.pi) # Not sure if we should have the *2 out front or not
	except Exception as e:
		print cosineSimilarity
		print e
		return 0 # --> if cosineSimilarity = 1, math.acos is undefined, but the curve approaches 0
	return result

#helper fu nction for kmeans. Selects a random entry from the list of feature
#vectors passed in to the kmeans function.
def selectRandomCenters(examples, K):
    centers = []
    for x in range(K):
      randEx = examples[random.randint(0, len(examples)-1)][0] #len(examples) - 1
      centers.append(randEx)
    return centers

#helper funciton for kmeans. Returns the "average" of the given cluster. 
# Taken from the CS221 assignment starter code
def findMiddle(cluster):
	exAvg = {}
	count = len(cluster)
	for example in cluster:
		increment(exAvg, 1, example[0])
	for k, v in exAvg.items():
		exAvg[k] = v/float(count)
	return exAvg

#Returns the total cost of the current assignment
def findLoss(assignments, examples, centers):
	loss = 0
	for i, example in enumerate(examples):
		center = centers[assignments[i]]
		centerMag = magnitude(center)
		loss += math.pow(scoreVectors(example[0], center, centerMag), 2)
	return loss

#Finds the closest center to the given example
def findGroup(example, centers):
	minimum = -1
	index = 0
	for x in range(len(centers)):
		center = centers[x]
		centerMag = magnitude(center)
		score = scoreVectors(example, center, centerMag)
		if score < minimum or minimum == -1:
			minimum = score
			index = x
	return index


def kmeans(featureVectors, K, maxIters):
	'''K-means clustering algorithm adapted from CS221 sentiment classification

	featureVectors: list of string-to-double sparse vectors, stored as a counter/dict
	K: number of centroids. TODO: adjust
	maxIters: if the algorithm doesnt converge, terminate after this many iterations'''
	#################

	#################
	z = {} #A dict mapping from a cluster index to a list of groupings
	for i in range(K):
		z[i] = list() #initialize to empty list
	centers = selectRandomCenters(featureVectors, K) #selects randomly from our feature vectors 
	for i in range(maxIters):
		assignments = []	#Assignments array contains group/centroid index of the feature
											# Array is in same order as the featureVectors

		#Iterate through each training example. Finds the closest center and assigns it to that
		#group. z[i] contains all (features, label) examples assigned the ith center.
		for j in range(0, len(featureVectors)):
			features, label = featureVectors[j]
			groupIndex = findGroup(features, centers) 
			z[groupIndex].append((features, label))	# each feature vector is a data point, which is assigned to a cluster
			# keeps track of the group index of each entry in examples, in the order in which they are read from the file
			assignments.append(groupIndex)

		#update centers
		for x in range(K):
			centers[x] = findMiddle(z[x])
		cost = findLoss(assignments, featureVectors, centers) 

		# ---> This cost should decrease with iterations... Currently does not.
		# Possible reason: cosine similarity distance metric intended for [0, 1] values,
		# and the current test feature vector contains start/end position
		print 'Running cost iteration ' + str(i) + ': ' + str(cost)

	return centers, assignments, cost, z

# Each cluster is either diseased or healthy, depending on the majority of training data
# points assigned there. Since 10% of the training data is known to be diseased, we
# classify a cluster as diseased if more than 10% of it is dieased.
def classifyCenters(z, K):
	result = dict()
	for i in range(0, K):
		healthy = 0
		diseased = 0

		#check if there are any assignments to the ith cluster
		if len(z[i]) == 0:
			result[i] = 0

		else:
			for example, label in z[i]:
				if label == 1:
					diseased += 1
				else:
					healthy += 1
			#For some reason, only getting around 1 "diseased" cluster. I would expect more
			if float(diseased)/float(diseased+healthy) >= 0.1: 
				print 'DISEASED cluster'
				result[i] = 1
			else:
				print 'HEALTHY cluster'
				result[i] = -1
	return result




# Examples: List of tuples containing a feature vector (string to int dict) and a classfication
# label, used for calculating error rate. 
# Centers: List of feature vecrtors representing the 'coordinates' of each center
# z: dict mapping center index to list of feature vectors assigned to that centroid
def test(examples, centers, z, K):
	total = len(examples)
	numDiseased = 0
	numHealthy = 0
	incorrect = 0
	#first, map each center to either diseased (1) or healthy (-1), depending on the majority of
	# data points clustered there
	classifiedCenters = classifyCenters(z, K)
	for example, label in examples:
		groupIndex = findGroup(example, centers)
		if classifiedCenters[groupIndex] == -1:
			numHealthy += 1
		elif classifiedCenters[groupIndex] == 1:
			numDiseased += 1

		if classifiedCenters[groupIndex] != label:
			incorrect += 1

	return float(incorrect)/float(total), \
		float(numHealthy)/float(total), \
		float(numDiseased)/float(total)



def main():
	#training examples contains (features, label), where features is our extracted
	#feature vector, and label is the true classification where 1 = diseased and
	#-1 = healthy.
	print 'Begin Training...'
	trainingExamples = pickle.load(open(pickledTrainingFile, 'rb'))
	centers, assignments, cost, z = kmeans(trainingExamples, K_CONST, MAX_ITERS)

	print 'Finished Training'
	print 'Final Cost: ' + str(cost)
	print 'Begin classification... '

	testingExamples = pickle.load(open(pickledTrainingFile, 'rb'))
	errorRate, healthy, diseased = test(testingExamples, centers, z, K_CONST)

	print 'Finished testing...'
	print 'Error rate: ' + str(errorRate)
	print 'Percentage healthy in testing set: ' + str(healthy)
	print 'Percentage diseased in testing set: ' + str(diseased)
	#print centers

if __name__ == '__main__':
  main()

