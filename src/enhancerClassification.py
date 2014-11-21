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

def overlapWithVistaEnhancers(chrom, start, end):
  numEnhancers = 0
  enhancerTypes = []
  with open('../overlapBEDFiles/regulatory/VistaEnhancers/vistaEnhancers.bed') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
      if overlaps([chrom, start, end], [row[0], int(row[1]), int(row[2])]):
        numEnhancers += 1
        enhancerTypes.append(row[3])
  return numEnhancers, enhancerScore

def overlapWithBroadEnhancers(chrom, start, end):
  numEnhancers = 0
  enhancerScore = 0
  with open('../overlapBEDFiles/regulatory/BroadEnhancers/gm12878ChromHmm.bed') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
      if overlaps([chrom, start, end], [row[0], int(row[1]), int(row[2])]):
        numEnhancers += 1
        enhancerScore += float(row[4]) / 100.0
  return numEnhancers, enhancerScore

def enhancers(chrName, start, end):
  return overlapWithEnhancers(chrName, start, end)

def append_features_and_target_baseline(filename, X, y, score, skip):
  with open(filename) as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
      if (randrange(skip) != 0):
        continue
      typeWithAnnotation = row[3]
      cnvType = row[3].split(';')[0]
      X.append([mkChrToFloat(row[0]), np.log10(float(row[1])), np.log10(float(row[2])), mkCnvTypeToFloat(cnvType)])
      y.append(score)

def append_features_and_target(filename, X, y, score, skip):
  with open(filename) as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
      if (randrange(skip) != 0):
        continue
      typeWithAnnotation = row[3]
      cnvType = row[3].split(';')[0]
      numEnhancers, enhancerScore = enhancers(row[0], int(row[1]), int(row[2]))
      X.append([mkChrToFloat(row[0]), np.log(float((int(row[2]) - int(row[1])))), mkCnvTypeToFloat(cnvType), numEnhancers, enhancerScore])
      y.append(score)
     
def load_features_and_target(baseline, skipDiseased, skipHealthy):
  X = []
  y = []
  if baseline:
    append_features_and_target_baseline('../dbVarData/nstd100.diseased.vcf.bed', X, y, 1.0, skipDiseased)
  else:
    append_features_and_target('../dbVarData/nstd100.diseased.vcf.bed', X, y, 1.0, skipDiseased)
  numDiseased = len(X)
  if baseline:
    append_features_and_target_baseline('../dbVarData/nstd100.healthy.vcf.bed', X, y, -1.0, skipHealthy)
  else:
    append_features_and_target('../dbVarData/nstd100.healthy.vcf.bed', X, y, -1.0, skipHealthy)
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
def runBase(classifier='svc', kernel='linear', skip=25, diseaseFactor=1.0):
  print '======= BASE LINE ======='
  X, y, numDiseased, numHealthy = load_features_and_target(True, max(int(skip / diseaseFactor), 1), skip)
  return run(X, y, numDiseased, numHealthy, kernel, classifier)

def runClass(classifier='svc', kernel='linear', skip=25, diseaseFactor=1.0):
  print '===== SOPHISTICATED ====='
  X, y, numDiseased, numHealthy = load_features_and_target(False, max(int(skip / diseaseFactor), 1), skip)
  return run(X, y, numDiseased, numHealthy, kernel, classifier)

def run(X, y, numDiseased, numHealthy, kernel, classifier):
  X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=.25)
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
    method = KNeighborsClassifier()
  elif classifier == 'rf':
    method = RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=1)
  elif classifier == 'lr':
    method = LogisticRegression(class_weight={-1:1, 1:diseasedWeight})
  wclf = method.fit(X_train, y_train)
  y_score_bin = wclf.predict(X_test)
  print('classification completed; starting cross validation')
  accuracy = accuracy_score(y_score_bin, y_test)
  print 'Accuracy: ' + str(accuracy * 100) + '%'
  precision = precision_score(y_score_bin, y_test)
  print 'Precision (prob. of diagnosis being true): ' + str(precision * 100) + '%'
  recall = recall_score(y_score_bin, y_test)
  print 'Recall (percentage of correctly diagnosed out of all cases): ' + str(recall * 100) + '%'
  return X, y, wclf

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

# if __name__ == "__main__":
#   print('Hello')
#   run()
