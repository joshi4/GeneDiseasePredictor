import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, datasets,cross_validation
import csv
from random import shuffle
import matplotlib.pyplot as plt
import os

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

def overlapWithEnhancers(chrom, start, end):
  ret = 0
  with open('../overlapBEDFiles/regulatory/VistaEnhancers/vistaEnhancers.bed') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
      if overlaps([chrom, start, end], [row[0], int(row[1]), int(row[2])]):
        ret += 1
  return ret

def enhancers(chrName, start, end):
  return overlapWithEnhancers(chrName, start, end)

def append_features_and_target(filename, X, y, score, skip):
  with open(filename) as f:
    reader = csv.reader(f, delimiter='\t')
    i = 1
    for row in reader:
      if i != skip:
        i += 1
        continue
      i = 1
      typeWithAnnotation = row[3]
      cnvType = row[3].split(';')[0]
      numEnhancers = enhancers(row[0], row[1], row[2])
      X.append([mkChrToFloat(row[0]), float((int(row[2]) - int(row[1])) / 10000), mkCnvTypeToFloat(cnvType), enhancers(row[0], int(row[1]), int(row[2]))])
      y.append(score)
     

def load_features_and_target(skip):
  X = []
  y = []
  append_features_and_target('../dbVarData/nstd100.diseased.vcf.bed', X, y, 1.0, skip)
  append_features_and_target('../dbVarData/nstd100.healthy.vcf.bed', X, y, -1.0, skip)
  X_shuf = []
  y_shuf = []
  index_shuf = range(len(X))
  shuffle(index_shuf)
  for i in index_shuf:
    X_shuf.append(X[i])
    y_shuf.append(y[i])
  return np.asarray(X_shuf), np.asarray(y_shuf)

def run():
  X, y = load_features_and_target(40)
  print('Loaded features; starting classification')
  print(str(len(X)))
  wclf = svm.SVC(kernel='linear', class_weight={1:10}).fit(X, y)
  print('classification completed; starting cross validation')
  scores=cross_validation.cross_val_score(wclf, X, y, cv=5)
  print('Scores/mean/sd')
  print 'Scores: ' + str(scores) + ', mean: ' + str(scores.mean()) + ', sd: ' + str(scores.std())

  return X, y, wclf

def plot(X, y, wclf, idx1, idx2):
  w = wclf.coef_[0]
  a = -w[0] / w[1]
  xx = np.linspace(0,1000)
  yy = a*xx - wclf.intercept_[0] / w[1]

  plt.plot(xx, yy, 'k-')
  plt.autoscale(enable=False)
  plt.xlim(0, max(X[:, idx1]))
  plt.ylim(0, max(X[:, idx2]))
  plt.scatter(X[:, idx1], X[:, idx2], c=y, cmap=plt.cm.Paired)
  plt.legend()

  plt.show()

# if __name__ == "__main__":
#   print('Hello')
#   run()
