import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, datasets, cross_validation
from sklearn.metrics import accuracy_score, precision_score, recall_score
import csv
from random import shuffle
import matplotlib.pyplot as plt
import os
from random import randrange
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
import seaborn as sns
import pandas as pd

chrToFloat = {}
floatToChr = {}
cnvTypeToFloat = {}
floatToCnvType = {}

def appendDict(d, rd, key):
  if key in d:
    return d[key]
  assert len(d) == len(rd)
  val = len(d)
  d[key] = val
  rd[val] = key
  return val

def mkChrToFloat(chrName):
  return appendDict(chrToFloat, floatToChr, chrName)

def mkCnvTypeToFloat(typeName):
  return appendDict(cnvTypeToFloat, floatToCnvType, typeName)

def overlaps(a, b):
  if a[0] != b[0]:
    return False
  if a[1] < b[1] and a[2] > b[2]:
    return True
  if a[1] > b[1] and a[2] < b[2]:
    return True
  if a[1] < b[1] and a[2] > b[1]:
    return True
  if a[1] < b[2] and a[2] > b[2]:
    return True
  return False

def overlapWithVistaEnhancers():
  ret = {}
  with open('../overlapBEDFiles/regulatory/VistaEnhancers/nstd100XvistaEnhancers.bed') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
      chrom = row[0]
      start = int(row[1])
      end = int(row[2])
      score = int(row[8])
      if (chrom, start, end) in ret:
        (numEnhancers, oldScore) = ret[(chrom, start, end)]
        ret[(chrom, start, end)] = (numEnhancers + 1, oldScore + score / 100)
      else:
        ret[(chrom, start, end)] = (1, score / 100)
  return ret

vistaEnhancersDict = overlapWithVistaEnhancers()

def vistaEnhancers(chrName, start, end):
  if (chrName, start, end) in vistaEnhancersDict:
    (numEnhancers, score) = vistaEnhancersDict[(chrName, start, end)]
    return numEnhancers, score
  return 0, 0

enhancerTypesToFloat = {}
floatToEnhancerTypes = {}

minChrom = {}
maxChrom = {}

def addMinChrom(chrom, pos):
  if chrom in minChrom:
    if pos < minChrom[chrom]:
      minChrom[chrom] = pos
  else:
    minChrom[chrom] = pos

def addMaxChrom(chrom, pos):
  if chrom in maxChrom:
    if pos > maxChrom[chrom]:
      maxChrom[chrom] = pos
  else:
    maxChrom[chrom] = pos

def append_features_and_target_baseline(filename, X, y, score, skip):
  with open(filename) as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
      if (randrange(skip) != 0):
        continue
      typeWithAnnotation = row[3]
      cnvType = row[3].split(';')[0]
      start = int(row[1])
      end = int(row[2])
      addMinChrom(row[0], start)
      addMaxChrom(row[0], end)
      X.append([mkChrToFloat(row[0]), float(row[1]) / 100000.0, float(row[2]) / 100000.0, mkCnvTypeToFloat(cnvType)])
      # X.append([mkChrToFloat(row[0]), randrange(2000), randrange(2000), mkCnvTypeToFloat(cnvType)])
      y.append(score)

def append_features_and_target_vista(filename, X, y, score, skip):
  with open(filename) as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
      if (randrange(skip) != 0):
        continue
      typeWithAnnotation = row[3]
      cnvType = row[3].split(';')[0]
      start = int(row[1])
      end = int(row[2])
      addMinChrom(row[0], start)
      addMaxChrom(row[0], end)
      numEnhancers, enhancerScore = vistaEnhancers(row[0], int(row[1]), int(row[2]))
      X.append([mkChrToFloat(row[0]), float(row[1]) / 100000.0, float(row[2]) / 100000.0, np.log10(float((int(row[2]) - int(row[1])))), mkCnvTypeToFloat(cnvType), numEnhancers, enhancerScore])
      y.append(score)

def load_features_and_target(baseline, skipDiseased, skipHealthy):
  X = []
  y = []
  if baseline:
    append_features_and_target_baseline('../dbVarData/nstd100.diseased.vcf.bed', X, y, 1.0, skipDiseased)
  else:
    append_features_and_target_vista('../dbVarData/nstd100.diseased.vcf.bed', X, y, 1.0, skipDiseased)
  numDiseased = len(X)
  if baseline:
    append_features_and_target_baseline('../dbVarData/nstd100.healthy.vcf.bed', X, y, -1.0, skipHealthy)
  else:
    append_features_and_target_vista('../dbVarData/nstd100.healthy.vcf.bed', X, y, -1.0, skipHealthy)
  numHealthy = len(X) - numDiseased
  X_shuf = []
  y_shuf = []
  index_shuf = range(len(X))
  shuffle(index_shuf)
  for i in index_shuf:
    X_shuf.append(X[i])
    y_shuf.append(y[i])
  return np.asarray(X_shuf), np.asarray(y_shuf), numDiseased, numHealthy

# kernels: e.g. linear, rbf, poly
# classifiers: svc, knn (k nearest neighbors), rf (random forest), lr (logistic regression)
def runBase(classifier='svc', kernel='linear', skip=1, diseaseFactor=1.0):
  print '======= BASE LINE ======='
  X, y, numDiseased, numHealthy = load_features_and_target(True, max(int(skip / diseaseFactor), 1), skip)
  X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=.25)
  return X, y, run(X_train, X_test, y_train, y_test, numDiseased, numHealthy, kernel, classifier)

def runClass(classifier='svc', kernel='linear', skip=1, diseaseFactor=1.0):
  print '===== ALL  FEATURES ====='
  X, y, numDiseased, numHealthy = load_features_and_target(False, max(int(skip / diseaseFactor), 1), skip)
  X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=.25)
  return X, y, run(X_train, X_test, y_train, y_test, numDiseased, numHealthy, kernel, classifier)

def run(X_train, X_test, y_train, y_test, numDiseased, numHealthy, kernel, classifier):
  assert (len([i for i in y_test if i > 0]) > 0)
  print('Loaded features; starting classification')
  print('Number of diseased samples: ' + str(numDiseased))
  print('Number of healthy samples: ' + str(numHealthy))
  diseasedWeight = float(numHealthy) / float(numDiseased)
  # diseasedWeight = 1
  print('Diseased weight: ' + str(diseasedWeight))
  if classifier == 'svc':
    method = svm.SVC(kernel=kernel, degree=2, class_weight={-1:1, 1:diseasedWeight})
  elif classifier == 'knn':
    method = KNeighborsClassifier(n_neighbors=3)
  elif classifier == 'rf':
    method = RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=1)
  elif classifier == 'lr':
    method = LogisticRegression(class_weight={-1:1, 1:diseasedWeight})
  wclf = method.fit(X_train, y_train)
  y_pred = wclf.predict(X_test)
  print('classification completed; starting validation')
  precision = precision_score(y_test, y_pred)
  print 'Precision (prob. of diagnosis being true): ' + str(precision * 100) + '%'
  recall = recall_score(y_test, y_pred)
  print 'Recall (percentage of correctly diagnosed out of all cases): ' + str(recall * 100) + '%'
  return wclf

def plot(X, idx1, idx2):
  xLim1 = min(X[:, idx1])
  yLim1 = min(X[:, idx2])
  xLim2 = max(X[:, idx1])
  yLim2 = max(X[:, idx2])

  plt.autoscale(enable=True)
  plt.xlim(xLim1, xLim2)
  plt.ylim(yLim1, yLim2)
  plt.scatter(X[:, idx1], X[:, idx2], c=y, cmap=plt.cm.Paired)
  plt.legend()

  plt.show()

def myPlotViolin(X, y):
  plotViolin(X, y, ['chr', 'start', 'end', 'cnvType'], 'chr', 'start')

def plotViolin(X, y, columnNames, xColumn, yColumn):
  X_healthy = X[y == -1]
  X_diseased = X[y == 1]
  dfX_healthy = pd.DataFrame(X_healthy)
  dfX_healthy.columns = columnNames
  dfX_diseased = pd.DataFrame(X_diseased)
  dfX_diseased.columns = columnNames
  f, (ax_upper, ax_lower) = plt.subplots(2, 1)
  sns.violinplot(dfX_healthy[yColumn], dfX_healthy[xColumn], inner='None', ax=ax_upper, bw=.001)
  sns.violinplot(dfX_diseased[yColumn], dfX_diseased[xColumn], inner='None', ax=ax_lower, bw=.001)
  plt.show()

def plotLSVC(X, y, wclf, idx1, idx2):
  w = wclf.coef_[0]
  a = -w[idx1] / w[idx2]
  print 'Slope: ' + str(a)
  print 'Intercept: ' + str(wclf.intercept_[0] / w[idx2])
  xLim1 = min(X[:, idx1])
  yLim1 = min(X[:, idx2])
  xLim2 = max(X[:, idx1])
  yLim2 = max(X[:, idx2])
  xx = np.linspace(xLim1, xLim2)
  yy = a*xx - wclf.intercept_[0] / w[idx2]

  plt.plot(xx, yy)
  plt.autoscale(enable=False)
  plt.xlim(xLim1, xLim2)
  plt.ylim(yLim1, yLim2)
  plt.scatter(X[:, idx1], X[:, idx2], c=y, cmap=plt.cm.Paired)
  plt.legend()

  plt.show()

def findKnnRegions():
  X, y, wclf = runBase('knn')
  step = 5000 
  last = False
  regionStart = 0
  regionEnd = 0
  regions = []
  for chrom in minChrom:
    for i in xrange(minChrom[chrom], maxChrom[chrom], step):
      if wclf.predict([chrToFloat[chrom], i / 100000.0, (i + step) / 100000.0, 1.0])[0] == 1:
        if last:
          regionEnd = i + step
        else:
          last = True
          regionStart = i
          regionEnd = i + step
      else:
        if last:
          regions.append([chrom, regionStart, regionEnd])
          last = False
  return regions

def printRegions(regions):
  for t in regions:
    print t[0] + ':' + str(t[1]) + '-' + str(t[2])

def printRegionsBED(regions, filename):
  f = open(filename, 'w')
  for t in regions:
    f.write(t[0] + '\t' + str(t[1]) + '\t' + str(t[2]) + '\n')
  f.close()

# if __name__ == "__main__":
#   printRegionsBED(findKnnRegions(), 'knnRegions.bed')
