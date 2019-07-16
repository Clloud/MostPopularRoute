from point import Point
import os

class Preprocessor:
    def __init__(self, root_path, scale):
        # GPS trajectory points
        self.points = []
        # dataset root path
        self.root_path = root_path
        # dataset directories
        self.directories = os.listdir(root_path)
        # dataset scale
        self.scale = scale    

    def get_points(self):
        self.__scan_directories()
        return self.points

    def __scan_directories(self):
        for directory in self.directories:
            full_path = self.root_path + '/' + directory
            if os.path.isdir(full_path) and int(directory) <= self.scale:
                data_file_dir = full_path + '/Trajectory/'
                if os.path.isdir(data_file_dir):
                    files = os.listdir(data_file_dir)
                    for file in files:
                        with open(data_file_dir + file) as data:
                            self.__get_point(data)
    
    def __get_point(self, data):
        temp = data.readlines()
        for index in range(len(temp)):
            if index < 6:
                continue
            t = temp[index].strip().split(',')
            point = Point(float(t[0]), float(t[1]))
            if self.__filter(point):
                self.points.append(point)

    def __filter(self, point):
        if (point.longitude > 116.2 and point.longitude < 116.55
            and point.latitude > 39.75 and point.latitude < 40.10):
            return True
        return False
