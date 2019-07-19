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
points = Points(preprocessor.get_points())
print("Total: {} points".format(len(points)))

# use coherence expanded algorithm to form clusters
# clusters = Cluster(points).coherence_expanding()
# print(len(clusters))
# network = TransferNetwork(points, clusters)

# generate trajectory figures
# figure = Figure()
# figure.scatter(points).show()
# Figure.transfer_network(points, network)
