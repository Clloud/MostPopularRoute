from point import Point


class TransferNetwork():
    def __init__(self, points, clusters):
        self.nodes = []
        self.create_transfer_node(clusters)

    def create_transfer_node(self, clusters):
        for cluster in clusters:
            sum1, sum2 = 0, 0
            for point in cluster:
                sum1 += point.latitude
                sum2 += point.longitude
            node = Point(sum1 / len(cluster), sum2 / len(cluster))
            self.nodes.append(node)
