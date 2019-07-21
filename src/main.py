from config import Config
from preprocessor import Preprocessor
from points import Points
from cluster import Cluster
from transfer_network import TransferNetwork
from figure import Figure

# get points from trajectories
preprocessor = Preprocessor(
    Config.DATASET_ROOT_DIR,
    Config.DATASET_SCALE)
points = preprocessor.get_points()

# use coherence expanded algorithm to form clusters
clusters = Cluster(points).coherence_expanding()
network = TransferNetwork(points, clusters)

# generate trajectory figures
figure = Figure(theme='light')
figure.scatter_and_network(points, clusters, network).show()
