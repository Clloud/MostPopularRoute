from config import Config
from preprocessor import Preprocessor
from points import Points
from cluster import Cluster
from transfer_network import TransferNetwork
from transfer_probability import TransferProbability
from most_popular_route import MostPopularRoute
from figure import Figure

def main():
    # get points from trajectories
    preprocessor = Preprocessor(
        Config.DATASET_ROOT_DIR,
        Config.DATASET_SCALE)
    points = preprocessor.get_points()

    # use coherence expanded algorithm to form clusters
    clusters = Cluster(points).coherence_expanding()
    network = TransferNetwork(points, clusters)


    def show_transfer_edges(network):
        print(end="\t")
        for i in range(len(network.edges)):
            print(" {}\t".format(i), end="")
        print()
        for i in range(len(network.edges)):
            print(i, end="\t")
            for j in range(len(network.edges)):
                print("{}\t".format(network.edges[i][j]), end="")
            print("\n")

        for key, value in network.trajectories.items():
            print(key, value)


    show_transfer_edges(network)

    # derive transfer probability
    tp = TransferProbability(network)
    # tp.derive()
    for node in tp.nodes:
        print("\n")
        print("node", tp.nodes.index(node), ":", (node.latitude, node.longitude))
        p = tp.create_transition_matrix(node)
        print("P:\n", p)
        q, s = tp.reorganize(p, node)
        print("Q:\n", q)
        print("S:\n", s)
        print("V:\n", tp.cal_vector(node, p, q, s))

    # search the most popular route
    # mpr = MostPopularRoute(network)
    # result = mpr.search(0, 4)

    # generate trajectory figures
    # figure = Figure(theme='light')
    # cluster_points = [point for cluster in clusters for point in cluster]
    # figure.scatter_and_network(points, network, cluster_points).show()


if __name__ == '__main__':
    main()