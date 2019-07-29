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

    # derive transfer probability
    tp = TransferProbability(network)
    tp.derive()

    # search the most popular route
    mpr = MostPopularRoute(network)
    route = mpr.search(0, 15)
    print(route)
    figure = Figure()
    figure.most_popular_route(points, network, route).show()


if __name__ == '__main__':
    main()