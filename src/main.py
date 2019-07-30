from config import Config
from preprocessor import Preprocessor
from points import Points
from cluster import Cluster
from transfer_network import TransferNetwork
from transfer_probability import TransferProbability
from most_popular_route import MostPopularRoute
from figure import Figure
from cache import Cache


def main():
    key = Cache.generate_key(str(Config()))
    if Cache.check(key):
        data = Cache.get(key)
        points = data['points']
        network = data['network']
    else:
        pass
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

        # save points and network to cache
        Cache.save(key, {
            "points": points,
            "network": network
        })

    # show the distribution of transfer probability
    figure = Figure(width=8)
    figure.transfer_probability(network, 8).show()

    # search the most popular route
    mpr = MostPopularRoute(network)
    route = mpr.search(0, 4)
    print(route)
    figure = Figure()
    figure.most_popular_route(points, network, route).show()


if __name__ == '__main__':
    main()