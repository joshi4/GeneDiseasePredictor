import collections
import pickle 


# taken dot_product and increment from the sentiment assignment 
def dot_product(d1,d2):
    if len(d1) < len(d2):
        return dot_product(d2,d1)
    return sum(d1.get(f, 0) * v for f, v in d2.items())

def increment(d1,scale,d2):
    """
    Implements d1 += scale * d2 for sparse vectors.
    @param dict d1: the feature vector which is mutated.
    @param float scale
    @param dict d2: a feature vector.
    """
    for f, v in d2.items():
        d1[f] = d1.get(f, 0) + v * scale

def evaluate(pickled_test_file,predictor):
    test_examples = pickle.load(open(pickled_test_file, 'rb'))
    test_data = test_examples[20000:31001]  + test_examples[1000:3500]
    errors = 0 
    false_positive = 0 
    false_negative = 0 
    true_positive = 0 
    true_negative = 0 
    #N = len(test_examples) 
    N = len(test_data) 
    for feature,label in test_data:
        #print "test feature vector is ", feature
        result = predictor(feature)
        if result != label:
            errors += 1
        if result == 1 and label == -1 :
            false_positive += 1 
        if result == -1  and label == 1:
            false_negative += 1
        if result == 1 and label == 1:
            true_positive += 1
        if result == -1 and label == -1:
            true_negative += 1

    error_percent = errors*100.0/N 
    false_negative_percent = false_negative *100.0/N
    false_positive_percent = false_positive *100.0/N
    print "You misclassified %d out of %d for an error percent of %f" %(errors, N, error_percent) 
    print "false positves = %d or in percent: %f"%(false_positive, false_positive_percent) 
    print "false negatves = %d or in percent: %f"%(false_negative, false_negative_percent) 
    print "true positives are: %d" %(true_positive)
    print "true negatives are: %d" %(true_negative)

