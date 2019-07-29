import math
from rtree import index

class Points:
    def __init__(self):
        self.data = []
        self.index = 0
        self.rtree_index = index.Index()
    
    def __iter__(self):
        return iter(self.data)
    
    def next(self):
        self.index += 1
        return self.data[self.index]

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        return self.data[index]

    def append(self, p):
        self.data.append(p)
        self.rtree_index.insert(self.index, 
            (p.latitude, p.longitude, p.latitude, p.longitude))
        self.index += 1

    def range_query(self, point, radius):
        """
        Query all points within radius through r-tree index.

        :param Point point: the center point
        :param float radius
        :return: a list of points
        
        """
        index_list = list(self.rtree_index.intersection(
            (point.latitude - radius, point.longitude - radius,
            point.latitude + radius, point.longitude + radius)))
        result = [self.data[i] for i in index_list]
        return result
