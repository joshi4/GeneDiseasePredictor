import util
import math
class Kdistance():
    """
    This class is an Abstract class with common methods for
    computing the distance between two given vectors. 
    We will be using the distance metric as the angle between 
    the two vectors. This can be reused in K-NN and K-means. 
    """
    def dotProduct(self, a, b):
        return util.dot_product(a,b)
    
    def magnitude(self,v):
        """
        @param vector/collection dict |v|
        returns L2 norm of the vector 
        """
        curr_sum = 0.0 
        for value,_ in enumerate(v):
            curr_sum += (value * value )
        return math.sqrt(curr_sum)

    def computeDistance(self,a,b):
        """
        @params two vectors |a| and |b| 
        returns the angle between the two. 
        special case: returns +Inf if one of the vectors is None
        """
        if a == None or b == None:
            return float('Inf')
        dot_product = self.dotProduct(a,b)
        magnitude_a = self.magnitude(a)
        magnitude_b = self.magnitude(b)
        return math.acos(dot_product/(magnitude_a*magnitude_b))*180/math.pi


