class MaxHeap():
    """
    this class implements a max heap tailored to work with the |BallTree| class. 
    """
    def __init__(self,k):
        self.heap = [(float('Inf'), (None,None))]*k
        self.size = k 

    def peek_max_distance(self):
        return self.heap[0][0]

    def peek_max_ele(self):
        return self.heap[0]

    def insert_ele(self,ele):
        """
        @param: ele is a tuple ( distance, (feature,label))
        add ele to the top of the heap and execute |downward_heapify| to 
        maintain heap property
        """
        self.heap[0] = ele
        self.downward_heapify(0)

    def downward_heapify(self,index):
        left_child = 2*index + 1 
        right_child = 2*index + 2
        ele = self.heap[index][0]
        max_ele = ele 
        max_index = index 
        
        if left_child < self.size and ele < self.heap[left_child][0]:
            max_ele = self.heap[left_child][0]
            max_index = left_child
            
        if right_child < self.size and max_ele < self.heap[right_child][0]:
            max_ele = self.heap[right_child][0] 
            max_index = right_child

        if max_index != index:
            temp = self.heap[max_index]
            self.heap[max_index] = self.heap[index] 
            self.heap[index] = temp
            self.downward_heapify(max_index)
            
            
### testing the max heap implementation           
#elements_to_add = [(9,None), (34,None), (45,None), (8, None), (-1, None), (42,None)]
#max_heap = MaxHeap(4)
#for ele in elements_to_add:
#    max_heap.insert_ele(ele)
#print max_heap.peek_max_ele()
            
            
            
            
            
            
            

