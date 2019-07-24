from config import Config
from preprocessor import Preprocessor
from points import Points
from cluster import Cluster
from transfer_network import TransferNetwork
from transfer_probability import TransferProbability
from figure import Figure

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
test_tp = TransferProbability(network)
for node in test_tp.nodes:
    print("\n")
    print((node.latitude, node.longitude))
    p = test_tp.create_transition_matrix(node)
    print(p)
    q = test_tp.reorganize(p, node)[0]
    print(q)
    s = test_tp.reorganize(p, node)[1]
    print(s)

# generate trajectory figures
figure = Figure(theme='light')
cluster_points = [point for cluster in clusters for point in cluster]
figure.scatter_and_network(points, network, cluster_points).show()
