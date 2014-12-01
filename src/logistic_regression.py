import collections 
import math
import util
import pickle 
from random import shuffle
"""
Given the ./testingSet.p and ./trainigSet.p binary files 
this file runs logistic regression on trainingSet and tests the performance of 
the weights learned from ./testingSet.p 

Data stored in the pickled file is [ (features, result)] where result is 1  or -1. 
1 => diseased 
-1 => healthy -1. 

for description of features see features.py and featureExtractor.py 
"""
pickled_testing_file = "./testingSet.p"
pickled_training_file = "./trainingSet.p"

class HingeLossClassifier():
    """
    This class is an abstraction that trains a SVM 
    classifier on a given training data set 
    and provides methods to evaluate the performance. 
    uses a regularization parameter lambda and hyperparameter eta.
    """
    def __init__(self):
       self.weights = collections.Counter() # feature => weight mapping. 
       self.numIters = 10 # number of iterations for Stochastic Gradient Descent. 
       self.eta = 0.9 # hyper-parameter.
       self.lambda_value = 0.8
   

    def predict(self,feature):
       """
       @param feature: feature vector for the test example
       returns +1/-1 : diseased/healthy , which is the sign of the score. 
       """

       score = util.dot_product(self.weights, feature) 
       if score > 0: 
           return 1
       return -1

    def calculate_margin(self,feature,weight,training_label):
       score = util.dot_product(weight,feature)
       return training_label* score 

    def update_weights_with_derivative(self,feature,weight,training_label):
       util.increment(weight,self.eta * training_label, feature) 
       util.increment(weight,-2*self.lambda_value,weight) # regularization factor

    def learn_boundary(self, pickled_training_file):
       """
       this is the main function of this class and is callled by the user 
       to learn the boundary.

       args: |pickled_training_file| binary file with data on all trianing examples 
       with featuers already extracted [(features, label)]. Refer to beginning of this file. 
       """

       training_examples = pickle.load(open(pickled_training_file ,'rb'))
       for i in xrange(self.numIters):
           print "iteration number = " , i 
           for feature,label in training_examples:
               margin = self.calculate_margin(feature, self.weights, label) 
               if margin < 1.0:
                   self.update_weights_with_derivative(feature,self.weights,label)

class LogisticRegression():
    """
    This class is an abstraction that trains a logistic regression classifier
    on a given training data set and provides methods to evaluate its performance 
    """
    def __init__(self):
        self.weights = collections.Counter()
        self.numIters = 10 # num of iterations for SGD
        self.eta = 1.0 #0.09 # hyper-parameter
        self.predictDiseased = 0 
        self.penalizeDiseased = 1.0# parameter to adjust the margin so that diseased is penalized more. 

    def logistic_func(self, margin):
        if margin > 500:
            return 1.0
        result = 1.0/(1 + math.exp(margin))
        return result

   # def logistic_loss_func(self, margin):
   #     if margin > 500:
   #         return 0.0
   #     
   #     return math.log(1 + math.exp(-1*margin))
         

    def predict(self,feature):
        """
        @param feature: feature vector for test example,
        returns +1/-1 based on the sign of the score 
        +1 -> diseased test case and vice versa. 
        """
        score = util.dot_product(self.weights, feature)
        if score > 0: 
            self.predictDiseased += 1
            #print "score is > 0 yay!" 
            return 1
        return -1

    def calculate_margin(self,feature,weights,training_label):
       score = util.dot_product(weights, feature)
       normal_margin = training_label*score *1.0
       #margin = normal_margin if training_label == -1 else normal_margin*1.0/self.penalizeDiseased
       return normal_margin

    def update_weights_with_derivative(self, feature,weight,training_label):
       """
       if loss function is 1/1 + e^-score then the S.G.D update courtesy of CS229 notes is 
           w_j = w_j + eta*(label - 1/1_e^-score)*feature_vector
       where z is the margin. 
       """
       margin = self.calculate_margin(feature,weight,training_label)
       update_coeff = self.logistic_func(margin)*training_label
       util.increment(weight,self.eta * update_coeff, feature)  
       if training_label == 1.0:
           update_coeff = self.predict(feature) - 1
           util.increment(weight,self.penalizeDiseased*self.eta* update_coeff, feature)



    def learn_boundary(self, pickled_training_file):
        """
        @params pickled_training_file : [ (feature,label)] format
        Goes through each training case, updating the weight params according to the model
        """
        
        training_examples = pickle.load(open(pickled_training_file ,'rb'))
        for i in xrange(self.numIters):
            print "iteration number = " , i 
            shuffle(training_examples)
            #print "loss function is now: ", self.calcLossFunction(training_examples)
            for feature,label in training_examples:
                self.update_weights_with_derivative(feature,self.weights,label)

    def calcLossFunction(self,training_examples):
        loss = 0.0 
        for  feature,label in training_examples:
            margin = self.calculate_margin(feature,self.weights,label)
            loss += self.logistic_loss_func(margin)
            if label == 1:
                loss += 0.5* ((1 - self.predict(feature))**2) 

        return loss 

def main():
    #hl = HingeLossClassifier()
    #hl.learn_boundary(pickled_training_file)
    #util.evaluate(pickled_testing_file, hl.predict)
    #print hl.weights 

    lr = LogisticRegression()
    lr.learn_boundary(pickled_training_file)
    util.evaluate(pickled_testing_file, lr.predict) 
    print lr.weights 
    print lr.predictDiseased 


if __name__ == '__main__':
    main()



