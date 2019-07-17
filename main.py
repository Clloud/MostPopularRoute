from config import Config
from preprocessor import Preprocessor
from points import Points
from cluster import Cluster
from figure import Figure

# get points from trajectories
preprocessor = Preprocessor(
    Config.DATASET_ROOT_DIR,
    Config.DATASET_SCALE)
points = Points(preprocessor.get_points())

# use coherence expanded algorithm to form clusters
clusters = Cluster(points).coherence_expanding()

# generate trajectory figures
print("Total: {} points".format(len(points)))
Figure.scatter(points)
