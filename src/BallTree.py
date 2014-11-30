import collections
import MaxHeap
import pickle 
import Kdistance
class BallTreeNode():
    def __init__(self,data):
        self.data = data # list of tuple of the form [( feature, label)]
        self.right = None
        self.left = None

class BallTree(Kdistance):
    def construct_balltree(self,data,used_keys):
        """
        @params: [(feature,label)] where feature is some k dimensional vector
        @params: |used_keys| set of keys that have already been used to split the tree, don't use them again. 
        @modification to algo is: instead of choosing dimension with greatest spread, we choose 
        the most frequent occuring dimension. 
        returns reference to root of the ball tree 
        """
        if len(data) == 0: 
            return None
        if len(data) == 1: # base case 
            return BallTreeNode(data)
        #find dimension c which is occurs most frequently in the dataset. 
        most_frequent_key = collections.Counter()
        for feature,_ in data:
            most_frequent_key += feature
        most_common_key_list = most_frequent_key.most_common(1 if len(used_keys)== 0 else len(used_keys)+1)
        most_common_key = None
        for k,_ in most_common_key_list:
            if k not in used_keys:
                most_common_key = k 
                break 
        if most_common_key == None: #next base case.
            #print "most_common_key is none, creating large leaf node with %d data points" %(len(data))
            return BallTreeNode(data)
        #print "going a level deeper: most_common_key is %s" %(most_common_key)
        #print "the set of used keys is ", used_keys 

        right = [] #right is all those data points where most_common_key = 1
        left = [] #left is all those data points where most_common_key = 0 
        pivot = None
        for feature,label in data:
            if most_common_key in feature:
                if pivot == None:
                    pivot = (feature,label)
                else:
                    right.append((feature,label))
            else:
                left.append((feature,label))
        node = BallTreeNode(pivot)
        updated_used_keys = set(used_keys)
        updated_used_keys.add(most_common_key)
        node.left = self.construct_balltree(left,updated_used_keys)
        node.right = self.construct_balltree(right,updated_used_keys)
        return node 
    
    def test_tree_creation(self):
        test_data = pickle.load(open("testingSet.p", "rb"))
        mixed_data = [test_data[1000] , test_data[7000] , test_data[2000] , test_data[3000] , test_data[4000] , test_data[5000] , test_data[6000]]
        root_node = self.construct_balltree(mixed_data, set())


    def nearest_neighbors(self,k,target_vector,root):
        """
        @param: |k| is the number of nearest neighbours
        @param: |target_vector| number of 
        @param: |root| is the starting point of our search in the ball tree 
        @return: |Q| a priority queue of size |k| which has the k nearest neighbours 
                of |target_vector|
        """
        neighbours = MaxHeap(k)
        def recurse(k, target_vector, root, neighbours):
            if root != None:
                root_feature_vector = root.data[0][0]
                max_feature_vector = neighbours.peek_max_ele()[1][0]
                if self.computeDistance(root_feature_vector,target_vector) >= 
                    self.computeDistance( root_feature_vector, max_feature_vector):
                            return 
            elif root.left == None and root.right == None: #if its a leaf node then ... 
                for point in root.data:
                    point_v = point[0]
                    q_first = neighbours.peek_max_ele()[1][0]
                    candidate_distance = self.computeDistance(target_vector,point_v) 
                    heap_distance = self.computeDistance( target_vector,q_first)
                    if  candidate_distance  < heap_distance:
                        neighbours.insert_ele((candidate_distance, point))
            else:
                #figure out the closest child node, explore that first. 
                left_child = root.left 
                right_child = root.right 
                left_feature_vector = left_child[0][0]
                right_feature_vector = right_child[0][0]
                right_distance = self.computeDistance(target_vector, right_feature_vector)
                left_distance = self.computeDistance(target_vector, left_feature_vector)
                if right_distance < left_feature_vector:
                    recurse(k,target_vector,right_child,neighbours)
                    recurse(k,target_vector,left_child,neighbours)
                else:
                    recurse(k,target_vector,left_child,neighbours)
                    recurse(k,target_vector,right_child,neighbours)
        recurse(k,target_vector,root_feature_vector, neighbours)
        return neighbours.heap



btree = BallTree()
btree.test_tree_creation()
