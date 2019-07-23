class TransferProbability:
    def __init__(self, network):
        self.nodes = network.nodes
        self.edges = network.edges
        self.derive()

    def derive(self):
        for node in self.nodes:
            p = self.create_transition_matrix()
            self.reorganize(p)
            q, s = self.acquire(p)
            node.vector = self.cal_vector(q, s)

    def create_transition_matrix(self):
        pass

    def reorganize(self):
        pass

    def acquire(self):
        pass

    def cal_vector(self):
        pass
