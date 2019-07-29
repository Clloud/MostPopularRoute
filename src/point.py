import math


class Point:
    count = 0

    def __init__(self, latitude, longitude, trajectory_id=-1):
        self.latitude = latitude
        self.longitude = longitude
        self.trajectory_id = trajectory_id

        self.id = Point.count
        Point.count += 1
        self.moving_direction = (0, 0)
        self.classified = False

    def __str__(self):
        return "Trajectory {} Point {} (longitude,latitude): ({}, {}), \
            moving_direction: {}".format(
            self.trajectory_id,
            self.id,
            self.longitude,
            self.latitude, 
            self.moving_direction)

    def calculate_moving_direction(self, latitude, longitude):
        """
        Calculate current point's moving direction. 
        e.g. Pi and Pi+1 are adejcent points from the same trajectory,
        we denote Pi's moving direction as vector<PiPi+1>.
        
        :param float latitude: next point's latitude
        :param float longitude: next point's longitude
        """
        x = latitude - self.latitude
        y = longitude - self.longitude
        if x == 0 and y == 0:
            return
        self.moving_direction = (
            x / math.sqrt(x ** 2 + y ** 2),
            y / math.sqrt(x ** 2 + y ** 2))
