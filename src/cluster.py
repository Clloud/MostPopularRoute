from collections import deque
from config import Config
import math
import time

class Cluster:
    """
    Find road intersections(clusters) from trajectory points through 
    coherence expanded algorithm.
    """
    def __init__(self, points):
        self.points = points
        self.coherences = []

    def coherence_expanding(self):
        clusters = []
        for point in self.points:
            if not point.classified:
                point.classified = True
                cluster = self.expand(point)
                if len(cluster) >= Config.GROUP_SIZE_THRESHOLD:
                    for point in cluster:
                        point.classified = True
                    clusters.append(cluster)
        return clusters

    def expand(self, point):
        result = set()
        # save points that has been checked
        searched = set()
        # save point.id
        seeds = deque()
        # save point obejects to be checked
        seeds_dict = dict()

        searched.add(point.id)
        seeds.append(point.id)
        seeds_dict[point.id] = point
        result.add(point)

        while (len(seeds)):
            seed = seeds_dict[seeds.popleft()]
            seeds_dict.pop(seed.id)
            
            # find points nearby
            points = self.points.range_query(seed, Config.RADIUS)
            for pt in points:
                if self.__calculate_coherence(seed, pt) >= Config.COHERENCE_THRESHOLD \
                    and (not pt.classified) \
                    and pt.id not in seeds \
                    and pt.id not in searched:
                    seeds.append(pt.id)
                    seeds_dict[pt.id] = pt
                    result.add(pt)
                searched.add(pt.id)                
        return list(result)

    def __calculate_coherence(self, p, q):
        coherence = math.exp(- (self.__distance(p, q) / Config.SCALING_FACTOR) ** Config.TURNING_ALPHA) \
            * (self.__angle_sin_value(p, q) ** Config.TURNING_BETA)
        self.coherences.append(coherence)
        return coherence

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
        try:
            angle_cos_value = (x1 * x2 + y1 * y2) / (module_x * module_y)
        except ZeroDivisionError:
            return 0

        return math.sqrt(abs(1 - angle_cos_value ** 2))
