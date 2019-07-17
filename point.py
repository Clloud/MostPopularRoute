import math


class Point:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.moving_direction = (0, 0)
        self.classified = False

    def __str__(self):
        return "latitude: {}, longtitude: {}, moving_direction: {}".format(
            self.latitude, self.longitude, self.moving_direction)

    def calculate_moving_direction(self, latitude, longitude):
        x = latitude - self.latitude
        y = longitude - self.longitude
        if x == 0 and y == 0:
            return
        self.moving_direction = (
            x / math.sqrt(x ** 2 + y ** 2),
            y / math.sqrt(x ** 2 + y ** 2))
