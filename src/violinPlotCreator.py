import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import seaborn as sns
import pandas as pd
import logistic_regression
import pickle
import kmeans
import k_nearest_neighbours

pickledTestFile = './testingSet.p'
pickledTrainingFile = './trainingSet.p'
parallelIdFile = './violinTesting.bed'

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 50}

sns.set_context("notebook", font_scale=1.5)

def plotViolin(X, y, columnNames, xColumn, yColumn, filename):
  plt.rc('font', **font)
  X_healthy = X[y == -1]
  X_diseased = X[y == 1]
  dfX_healthy = pd.DataFrame(X_healthy)
  dfX_healthy.columns = columnNames
  dfX_diseased = pd.DataFrame(X_diseased)
  dfX_diseased.columns = columnNames
  f, (ax_upper, ax_lower) = plt.subplots(2, 1, figsize=(16,12), dpi=80, facecolor='w', edgecolor='k')
  sns.violinplot(dfX_healthy[yColumn], dfX_healthy[xColumn], inner='None', ax=ax_upper, bw=.05, color=['red', 'blue'])
  # sns.violinplot(dfX_healthy[yColumn], dfX_healthy[xColumn], inner='None', ax=ax_upper, bw=.05)
  ax_upper.set(xlabel='Healthy/Chromosomes', ylabel='')
  sns.violinplot(dfX_diseased[yColumn], dfX_diseased[xColumn], inner='None', ax=ax_lower, bw=.05, color=['red', 'blue'])
  # sns.violinplot(dfX_diseased[yColumn], dfX_diseased[xColumn], inner='None', ax=ax_lower, bw=.05)
  ax_lower.set(xlabel='Diseased/Chromosomes', ylabel='')
  if (filename != None):
    plt.savefig(filename)
  else:
    plt.show()

def padNum1(num):
  if (len(num) == 1):
    return '0' + num
  return num

def plotViolinChrSplit(X, y, columnNames, xColumn, yColumn, filename):
  l = [ [ num + 'a', num + 'p' ] for num in [ padNum1(str(num)) for num in range(1,12) ] ]
  set1 = [ item for sublist in l for item in sublist ]
  yIter = iter(y)
  X1 = []
  X2 = []
  y1 = []
  y2 = []
  for x in X:
    yData = next(yIter)
    if (x[0] in set1):
      X1.append(x)
      y1.append(yData)
    else:
      X2.append(x)
      y2.append(yData)
  filename1 = None
  filename2 = None
  if (filename != None):
    filename1 = filename + '1.png'
    filename2 = filename + '2.png'
  plotViolin(np.array(X1), np.array(y1), columnNames, xColumn, yColumn, filename1)
  plotViolin(np.array(X2), np.array(y2), columnNames, xColumn, yColumn, filename2)

def plotViolinFromReal(filename=None):
  X = []
  y = []
  with open(parallelIdFile) as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
      chrom = row[0]
      start = int(row[1])
      score = float(row[2])
      num = chrom[3:]
      num = padNum1(num)
      X.append([num, start])
      y.append(score)
  plotViolin(np.array(X), np.array(y), ['chr', 'start'], 'chr', 'start', filename)

def plotViolinFromPredictor(predictor, filename=None):
  X = []
  y = []
  testExamples = pickle.load(open(pickledTestFile, 'rb'))
  predIter = iter(testExamples)
  with open(parallelIdFile) as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
      chrom = row[0]
      start = int(row[1])
      actual = float(row[2])
      feature,_ = next(predIter)
      predicted = float(predictor(feature))
      num = chrom[3:]
      num = padNum1(num)
      X.append([num + 'a', start])
      y.append(actual)
      X.append([num + 'p', start])
      y.append(predicted)
  for i in range(1,23):
    num = str(i)
    if (len(num) == 1):
      num = '0' + num
    X.append([num + 'a', 10])
    y.append(1)
    X.append([num + 'a', 10])
    y.append(-1)
    X.append([num + 'p', 10])
    y.append(1)
    X.append([num + 'p', 10])
    y.append(-1)
  plotViolinChrSplit(np.array(X), np.array(y), ['chr', 'start'], 'chr', 'start', filename)

if __name__ == "__main__":
  # plotViolinFromReal('realData.png')

  # Hinge Loss:
  # print 'Hinge Loss:'
  # classifier = logistic_regression.HingeLossClassifier()
  # classifier.learn_boundary(pickledTrainingFile)
  # plotViolinFromPredictor(classifier.predict, 'hingeLoss')

  # Logistic Regression:
  # print 'Logistic Regression:'
  # classifier = logistic_regression.LogisticRegression()
  # classifier.learn_boundary(pickledTrainingFile)
  # plotViolinFromPredictor(classifier.predict, 'logisticRegression')

  # print 'New features:'
  # execfile('featureExtractor.py')

  # KMeans:
  # print 'KMeans'
  # classifier = kmeans.KMeans()
  # trainingExamples = pickle.load(open(pickledTrainingFile, 'rb'))
  # centers, assignments, cost, z = classifier.learn(trainingExamples)
  # classifier.classifyCenters(z)
  # plotViolinFromPredictor(classifier.test, 'kmeans')

  # K Nearest Neighbors:
  print 'K Nearest Neighbors'
  nn = k_nearest_neighbours.NearestNeighbors(5, pickledTrainingFile)
  plotViolinFromPredictor(nn.predict, 'knn')

