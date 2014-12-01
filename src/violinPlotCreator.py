import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import seaborn as sns
import pandas as pd
import logistic_regression as logReg
import pickle

pickledTestFile = './testingSet.p'
pickledTrainingFile = './trainingSet.p'
parallelIdFile = './violinTesting.bed'

def plotViolin(X, y, columnNames, xColumn, yColumn):
  X_healthy = X[y == -1]
  X_diseased = X[y == 1]
  dfX_healthy = pd.DataFrame(X_healthy)
  dfX_healthy.columns = columnNames
  dfX_diseased = pd.DataFrame(X_diseased)
  dfX_diseased.columns = columnNames
  f, (ax_upper, ax_lower) = plt.subplots(2, 1)
  sns.violinplot(dfX_healthy[yColumn], dfX_healthy[xColumn], inner='None', ax=ax_upper, bw=.05, color=['red', 'blue'])
  sns.violinplot(dfX_diseased[yColumn], dfX_diseased[xColumn], inner='None', ax=ax_lower, bw=.05, color=['red', 'blue'])
  plt.show()

def plotViolinFromReal():
  X = []
  y = []
  with open(parallelIdFile) as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
      chrom = row[0]
      start = int(row[1])
      score = float(row[2])
      num = chrom[3:]
      if (len(num) == 1):
        num = '0' + num
      X.append([num + 'r', start])
      y.append(score)
      X.append([num + 'p', start])
      y.append(score)
  plotViolin(np.array(X), np.array(y), ['chr', 'start'], 'chr', 'start')

def plotViolinFromPredictor(predictor):
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
      predicted = predictor(feature)
      num = chrom[3:]
      if (len(num) == 1):
        num = '0' + num
      X.append([num + 'r', start])
      y.append(actual)
      X.append([num + 'p', start])
      y.append(predicted)
  plotViolin(np.array(X), np.array(y), ['chr', 'start'], 'chr', 'start')

if __name__ == "__main__":
  # plotViolinFromReal()
  classifier = logReg.HingeLossClassifier()
  classifier.learn_boundary(pickledTrainingFile)
  plotViolinFromPredictor(classifier.predict)
