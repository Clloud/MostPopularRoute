from config import Config
from preprocessor import Preprocessor
from points import Points
from cluster import Cluster
from transfer_network import TransferNetwork
from figure import Figure
import time


# get points from trajectories
preprocessor = Preprocessor(
    Config.DATASET_ROOT_DIR,
    Config.DATASET_SCALE)
points = preprocessor.get_points()

# use coherence expanded algorithm to form clusters
start_time = time.time()
cluster = Cluster(points)
clusters = cluster.coherence_expanding()
network = TransferNetwork(points, clusters)
coherences = cluster.coherences
coherences.sort()
cluster_points = [point for cluster in clusters for point in cluster]
end_time = time.time()

# generate configuration text and result analysis
config_text = ">> CONFIGURATIONS\n"
config_text += "DATASET_ROOT_DIR: '{}'\n".format(Config.DATASET_ROOT_DIR)
config_text += "DATASET_SCALE = {}\n".format(Config.DATASET_SCALE)
config_text += "TRAJACTORY_SCALE = {}\n\n".format(Config.TRAJACTORY_SCALE)
config_text += "GROUP_SIZE_THRESHOLD φ = {}\n".format(Config.GROUP_SIZE_THRESHOLD)
config_text += "COHERENCE_THRESHOLD τ = {}\n".format(Config.COHERENCE_THRESHOLD)
config_text += "SCALING_FACTOR δ = {}\n".format(Config.SCALING_FACTOR)
config_text += "TURNING_ALPHA α = {}\n".format(Config.TURNING_ALPHA)
config_text += "TURNING_BETA β = {}\n".format(Config.TURNING_BETA)
config_text += "RADIUS r = {:.3f}\n".format(Config.RADIUS)
config_text += "\n----------------------------------------------------------------\n\n"

info = ">> RESULT\n"
info += "Points: {}".format(len(points))
info += "Clusters: {}\n".format(len(clusters))
info += "Points in clusters: {:.1f}%\n".format(len(cluster_points) / len(points) * 100)
info += "Running time: {:.3f} s\n\n".format(end_time - start_time)
for i in range(1, 11):
    info += "{}% coherence < {:.3f}\n".format(i * 10,
        coherences[int(i / 10 * len(coherences)) - 1])

print(config_text + info)
with open("../out/result.txt", "w") as file:
    file.write(config_text + info)

# generate analysis graph
figure = Figure(theme='light')
figure.scatter_and_network(points, network, cluster_points).save().show()