How to Extract our Training/Testing feature set
==========================

### Step 1: Run src/cacheOverlaps.py
This generates the necessary overlap .bed files required for some of the features. IMPORTANT: You have to have overlapSelect tool installed on your computer, and set the "overlapSelectPath" in cacheOverlaps.py to point to the correct location for this file to run. If you don't have overlapSelect on your computer (like me) you have to run all these steps on corn and make sure that path is correct. 

### Step 2: See what features are available
See src/features.py for a list of features avaiable. Each function in features.py being a feature. Each has a description in it's function of what it represents.

### Step 3: Decide on what features you want
In featureExtractor.py, edit the "listOfFeatures" list to include the features that you want from features.py
You can also decide on what ratio you want the result to be split for training/testing using the PercentageOfSetForTraining at the top of this file.

### Step 4: Run FeatureExtractor.py
This extracts the features in your "listOfFeatures", saving the results to trainingSet.p and testingSet.p each of which is a list of elements, each with features and the correct result (+1 or -1) saved in pickle files.
It also generates violinTesting.bed and violinTraining.bed which is the same data in the same order in a bed file.