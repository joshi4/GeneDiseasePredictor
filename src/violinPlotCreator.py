import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import seaborn as sns
import pandas as pd
import logistic_regression as logReg
import pickle

order = [ 'chr' + str(x) for x in range(1,23) ]

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
  sns.violinplot(dfX_healthy[yColumn], dfX_healthy[xColumn], inner='None', ax=ax_upper, bw=.05, order=order)
  sns.violinplot(dfX_diseased[yColumn], dfX_diseased[xColumn], inner='None', ax=ax_lower, bw=.05, order=order)
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
      X.append([chrom, start])
      y.append(score)
  plotViolin(np.array(X), np.array(y), ['chr', 'start'], 'chr', 'start')

def plotViolinFromPredictor(predictor):
  testExamples = pickle.load(open(pickledTestFile, 'rb'))
  predIter = iter(testExamples)
  with open(parallelIdFile) as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
      chrom = row[0]
      start = int(row[1])
      feature = next(predIter)
      score = predictor(feature)
      X.append([chrom, start])
      y.append(score)
  plotViolin(np.array(X), np.array(y), ['chr', 'start'], 'chr', 'start')

if __name__ == "__main__":
  # plotViolinFromReal()
  lr = logReg.LogisticRegression()
  lr.learn_boundary(pickledTrainingFile)
  plotViolinFromPredictor(lr.predict)
