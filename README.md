CNV Classifier
====================

Combined project for CS273A and CS221. 

For more info about features and feature extraction read the GeneratingFeaturesREADME in `src/`

## Models: 

* Baseline: Hinge Loss 
* Logistic Regression 
* K nearest neighbours ( with Ball trees )
* K means 

## API 

--------------------------------
HingeLoss and Logistic Regression both found in logistic\_regression.py and share the same API: 

* instantiate the class
* call the learn\_boundary method 
* pass the predict method to the common evaluation function in utils. 

API for K\_nn is the same with the exception of the learn boundary method. 

There are separate modules for Ball Trees, maxHeap and distance metric used in K\_nn 

The code in violinPlots should be a good illustration on using the API. 

--------------------------------
