from config import Config
from preprocessor import Preprocessor
from points import Points
from cluster import Cluster
from transfer_network import TransferNetwork
from figure import Figure
import time
import sys
import os


def process():
    # get points from trajectories
    preprocessor = Preprocessor(
        Config.DATASET_ROOT_DIR,
        Config.DATASET_SCALE)
    points = preprocessor.get_points()

    # use coherence expanded algorithm to form clusters
    cluster = Cluster(points)
    clusters = cluster.coherence_expanding()
    network = TransferNetwork(points, clusters)
    coherences = cluster.coherences
    coherences.sort()
    cluster_points = [point for cluster in clusters for point in cluster]

    return points, clusters, network, coherences, cluster_points


def report(points, clusters, network, coherences, cluster_points, execute_time):
    """
    generate configuration text and result analysis
    """
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
    info += "Points: {}\n".format(len(points))
    info += "Clusters: {}\n".format(len(clusters))
    info += "Points in clusters: {:.1f}%\n".format(len(cluster_points) / len(points) * 100)
    info += "Running time: {:.3f} s\n\n".format(execute_time)
    info += "Coherence data distribution:\n"

    # get coherence data distribution
    for i in range(1, 11):
        info += "{}% coherence < {:.3f}\n".format(i * 10,
            coherences[int(i / 10 * len(coherences)) - 1])
    info += "\nFor more information, please refer to coherence.txt"

    print(config_text + info)
    return config_text + info


def graph(points, network, cluster_points, save_path):
    """
    generate analysis graph
    """
    figure = Figure(theme='light')
    figure.scatter_and_network(points, network, cluster_points).save(save_path).show()


def save_to_file(analysis, coherences, save_path):
    """
    save analysis to file
    """
    with open("{}\\analysis.txt".format(save_path), "w") as file:
        file.write(analysis)

    # save coherence data to file
    with open("{}\\coherence.txt".format(save_path), "w") as file:
        file.write("Coherence data:\n")
        for coherence in coherences:
            file.write("{}\n".format(coherence))


def __generate_output_path():
    root_path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
    output_path = "{}\\out\\{}".format(
        root_path,
        time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())))
    os.makedirs(output_path)
    return output_path


start_time = time.time()
points, clusters, network, coherences, cluster_points = process()
end_time = time.time()

analysis = report(points, clusters, network, coherences, cluster_points, end_time - start_time)
save_path = __generate_output_path()
save_to_file(analysis, coherences, save_path)
graph(points, network, cluster_points, save_path)
