from collections import deque
from config import Config
import math


class Cluster:
    def __init__(self, points):
        self.points = points

    def coherence_expanding(self):
        clusters = []
        for point in self.points:
            if not point.classified:
                point.classified = True
                cluster = self.expand(point)
                if len(cluster) > Config.GROUP_SIZE_THRESHOLD:
                    clusters.append(cluster)
        return clusters

    def expand(self, point):
        result = []
        seeds = deque()
        seeds.append(point)
        result.append(point)
        # reference: Paper PART III, PAGE 904
        radius = Config.SCALING_FACTOR * \
            ((-math.log(Config.COHERENCE_THRESHOLD)) ** -Config.TURNING_ALPHA)

        while (len(seeds)):
            seed = seeds.popleft()
            points = self.points.range_query(seed, radius)
            for pt in points:
                if (not pt.classified) and self.__calculate_coherence(seed, pt) >= Config.COHERENCE_THRESHOLD:
                    seeds.append(pt)
                    result.append(pt)
        return result

    def __calculate_coherence(self, p, q):
        return math.exp(- (__distance(p, q) / Config.SCALING_FACTOR) ** Config.TURNING_ALPHA) \
            * (self.__angle_sin_value(p, q) ** Config.TURNING_BETA)

    def __distance(self, p, q):
        delta_x = p.latitude - q.latitude
        delta_y = p.longitude - q.longitude
        return math.sqrt(delta_x ** 2 + delta_y ** 2)

    def __angle_sin_value(self, p, q):
        x1 = p.moving_direction[0]
        y1 = p.moving_direction[1]
        x2 = q.moving_direction[0]
        y2 = q.moving_direction[1]

        module_x = math.sqrt(x1 ** 2 + y1 ** 2)
        module_y = math.sqrt(x2 ** 2 + y2 ** 2)
        angle_cos_value = (x1 * x2 + y1 * y2) / (module_x * module_y)
        return math.sqrt(1 - angle_cos_value ** 2)
