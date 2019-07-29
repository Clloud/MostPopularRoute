import sys
import os
root_path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
src_path = root_path + '\\src'
sys.path.append(src_path)

from config import Config
from preprocessor import Preprocessor
from points import Points
from cluster import Cluster
from transfer_network import TransferNetwork
from transfer_probability import TransferProbability

# get points from trajectories
preprocessor = Preprocessor(
    Config.DATASET_ROOT_DIR,
    Config.DATASET_SCALE)
points = preprocessor.get_points()

# use coherence expanded algorithm to form clusters
clusters = Cluster(points).coherence_expanding()
network = TransferNetwork(points, clusters)

# derive transfer probability
tp = TransferProbability(network)
for node in tp.nodes:
    print("\n")
    print("node", tp.nodes.index(node), ":", (node.latitude, node.longitude))
    p = tp.create_transition_matrix(node)
    print("P:\n", p)
    q, s = tp.reorganize(p, node)
    print("Q:\n", q)
    print("S:\n", s)
    print("V:\n", tp.cal_vector(node, p, q, s))