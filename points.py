class Points:
    def __init__(self, data):
        self.data = data
        self.index = 0
    
    def __iter__(self):
        return iter(self.data)
    
    def next(self):
        self.index += 1
        return self.data[self.index]

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        return self.data[index]
    
    def range_query(self, point, radius):
        # implement this
        return []
