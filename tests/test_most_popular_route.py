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
from most_popular_route import MostPopularRoute
from figure import Figure

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
tp.derive()

# search the most popular route
mpr = MostPopularRoute(network)
route = mpr.search(0, 6)
print(route)
figure = Figure()
figure.most_popular_route(points, network, route).show()