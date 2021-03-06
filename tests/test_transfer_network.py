import sys
import os
root_path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
src_path = root_path + '\\src'
sys.path.append(src_path)

from config import Config
from preprocessor import Preprocessor
from point import Point
from points import Points
from cluster import Cluster
from transfer_network import TransferNetwork


# get points from trajectories
points = Preprocessor(
    Config.DATASET_ROOT_DIR, 
    Config.DATASET_SCALE).get_points()

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