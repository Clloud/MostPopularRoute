from sortedcontainers import SortedList

class MostPopularRoute:
    def __init__(self, network):
        self.nodes = network.nodes
        self.edges = network.edges
    
    def search(self, start, destination):
        """
        Find the most popular route from start node to destination node 
        through Maximum Probability Product algorithm which is similar to
        Dijkstra's shortest path algorithm.

        :param int start: the start node index
        :param int destination: the destination node index
        :return: the most popular route from the given s to d

        """
        # attribute L records the maximum ρ() value of the route from the 
        # start node s to node ni
        for node in self.nodes:
            node.L = 0
        self.nodes[start].L = 1

        # create priority queue sorted by node's attribute L
        priority_queue = SortedList(key = lambda x: x.L)
        priority_queue.add(self.nodes[start])
        # save nodes that have been processed
        scanned_nodes = set()

        while priority_queue:
            # extract node u with maximum L value
            u = priority_queue.pop()
            u_index = self.nodes.index(u) 

            # find destination node and return the most popular route
            if u_index == destination:
                return self.get_route(u_index)
            
            # check node u's adjecent node
            adjacent_node_indexes = [index for index in range(len(self.edges[u_index]))
                if self.edges[u_index][index] != -1]
            for v_index in adjacent_node_indexes:
                v = self.nodes[v_index]
                new_L = u.L * self.popularity(v_index, destination)
                if v.L < new_L:
                    # modify node v's attribute L
                    priority_queue.discard(v)
                    v.L = new_L
                    v.parent_index = u_index
                    if v not in scanned_nodes:
                        priority_queue.add(v)
            scanned_nodes.add(u)

    def popularity(self, node, destination):
        """
        Get the popularity indicator of a transfer node with respect to
        destination.

        :param int node: transfer node index
        :param int destination: destination node index
        :return: the transfer probability
        """
        if node == destination:
            return 1
        vector = self.nodes[destination].vector
        return vector[node] if node < destination else vector[node - 1]

    def get_route(self, node_index):
        """
        Get the most popular route from s to d.

        :param int node_index: the destination node index
        :return: transfer nodes' index list
        """
        route = [node_index]
        node = self.nodes[node_index]
        while hasattr(node, 'parent_index'):
            route.append(node.parent_index)
            node = self.nodes[node.parent_index]
        return route      
