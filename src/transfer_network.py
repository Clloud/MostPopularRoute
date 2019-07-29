from point import Point


class TransferNetwork():
    """
    Build transfer network from trajectory points and clusters.

    :Attributes
        nodes: A list of transfer node obejects.

        edges: Adjecent matrix. If there are no edges between node i 
            and node j, then edges[i][j] = -1. Otherwise, a list of 
            trajectory which has passed through node i and node j will 
            be recorded in edges[i][j].
            e.g. `edges[0][1] = [1, 2]` means trajectory 1 and trajectory 2
            pass through adjecent node 0 and node 1

        trajectories: A list of trajectories consists of transfer nodes.
            e.g. `trajectories[0] = [1, 3, 6]` means trajectory 0 pass through 
            transfer node 1, 3, 6. 
    """
    def __init__(self, points, clusters):
        self.nodes = []
        self.edges = []
        self.trajectories = dict()

        self.create_transfer_node(clusters)
        self.create_transfer_edge(points, clusters)

    def create_transfer_node(self, clusters):
        """
        Dervie transfer node from clusters.

        Each cluster is represented by a transfer node, whose coordinate
        is approximately the average coordinate of the cluster points.
        """
        for cluster in clusters:
            sum1, sum2 = 0, 0
            for point in cluster:
                sum1 += point.latitude
                sum2 += point.longitude
            node = Point(sum1 / len(cluster), sum2 / len(cluster))
            self.nodes.append(node)

    def create_transfer_edge(self, points, clusters):
        """
        Construct transfer edge by checking trajectories between 
        transfer nodes.
        """
        clusters_size = len(clusters)
        self.edges = [[-1 for col in range(clusters_size)] for row in range(clusters_size)]

        cluster_points = dict()
        cluster_point_ids = set()
        for index in range(len(clusters)):
            for point in clusters[index]:
                point.cluster_id = index
                cluster_points[point.id] = point
                cluster_point_ids.add(point.id)
        
        index = self.find_first_point_in_cluster(0, points, cluster_point_ids)
        previous_point = points[index]
        while index < len(points) - 1:
            index += 1
            point = points[index]

            # current point is not in the clusters, skip
            if point.id not in cluster_point_ids:
                continue
            
            # Current point and its previous point are in the same trajectory, 
            # but they are not in the same cluster
            if point.trajectory_id == previous_point.trajectory_id \
                and point.cluster_id != previous_point.cluster_id:
                t_id = point.trajectory_id
                i = previous_point.cluster_id
                j = point.cluster_id
                # save the new found edge
                self.save_edge(i, j, t_id)
                self.save_edge(j, i, t_id)
                self.save_trajectory(i, j, t_id)
                previous_point = point
            else:
                previous_point = points[index]

    def find_first_point_in_cluster(self, index, points, cluster_point_ids):
        """
        Find the first point in the clusters after the indexed point.
        """
        for i in range(index, len(points)):
            # find the desired point
            if points[i].id in cluster_point_ids:
                return i
        return len(points) - 1
                
    def save_edge(self, i, j, t_id):
        if self.edges[i][j] == -1:
            self.edges[i][j] = []
        self.edges[i][j].append(t_id)

    def save_trajectory(self, i, j, t_id):
        if t_id not in self.trajectories.keys():
            self.trajectories[t_id] = []
        else:
            self.trajectories[t_id].pop()
        self.trajectories[t_id].append(i)
        self.trajectories[t_id].append(j)
