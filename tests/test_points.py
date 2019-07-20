import sys
import os
root_path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
src_path = root_path + '\\src'
sys.path.append(src_path)

from point import Point
from points import Points
from preprocessor import Preprocessor
from config import Config
import time


preprocessor = Preprocessor(
    Config.DATASET_ROOT_DIR,
    scale=2)
points = preprocessor.get_points()
print("Total: {} points".format(len(points)))
time_start = time.time()
print("Range query ...")
result = points.range_query(points[0], 10)
print("Result: {} points".format(len(result)))
time_end = time.time()
print("Time cost {} s".format(time_end - time_start))