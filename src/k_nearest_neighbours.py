from Kdistance import Kdistance 
import util
import pickle
class NearestNeighbors(Kdistance):
    """
    This class models the K-NN algorithm. 
    Will be using the distance metric to be the angle between 
    two vectors. 
    """
    def __init__(self,n,training_file):
        self.N = n 
        self.training_data = pickle.load(open(training_file, "rb"))

    def nearest_neighbor(self,v):
        """
        @param: test vector |v|
        returns list of the n nearest neighbours based 
        on the distance metric inherited from Kdistance 
        """
        k_nn = []
        for feature,label in self.training_data:
            curr_distance = self.computeDistance(feature,v)
            if len(k_nn) < self.N:
                k_nn.append((curr_distance,label))
            else:
                element_to_remove = min(k_nn)
                k_nn.remove(element_to_remove)
                k_nn.append((curr_distance,label))
        return k_nn

    def predictor(self,v):
        """
        @params: test vector |v|
        returns prediction based on k- nearest neighbours
        """
        k_nn = self.nearest_neighbor(v)
        diseased_counter = 0 
        for _,label in k_nn:
            if label == 1:
                diseased_counter += 1
            else:
                diseased_counter -= 1
        if diseased_counter > 0:
            return 1
        return -1 


# digest the whole training dataset. 
# we want to weight the distances appropriately
# See time to predict for 1 element in the testing set. 
# Then, take a call on speeding it up
#options include:
#1. k-d tree's (but its difficult cause of the high possible dimensionality, but low real dimensionality) 
#2.cache the test set and if new test ele within some small distance of it then use the previous prediction
#3. Run the test queries in parallel. 

def evaluate(pickled_test_file,predictor):
    test_examples = pickle.load(open(pickled_test_file, 'rb'))
    errors = 0 
    false_positive = 0 
    false_negative = 0 
    N = len(test_examples) 
    for feature,label in test_examples:
        print "about to begin running the predictor"
        result = predictor(feature)
        print "finished"
        if result != label:
            errors += 1
        if result == 1 and label == -1 :
            false_positive += 1 
        if result == -1  and label == 1:
            false_negative += 1
        print "label = %d and result = %d" %(label,result)
        break 

nn = NearestNeighbors(3,"trainingSet.p")
util.evaluate("testingSet.p", nn.predictor)

