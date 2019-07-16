from config import Config
from preprocessor import Preprocessor
from figure import Figure

# get points from trajectories
preprocessor = Preprocessor(
    Config.DATASET_ROOT_DIR,
    Config.DATASET_SCALE)
points = preprocessor.get_points()

# generate trajectory figures
print("Total: {} points".format(len(points)))
Figure.scatter(points)