import math


class Config_1:
    DATASET_ROOT_DIR = '../data/test1/Data'  # The data set root directory
    DATASET_SCALE    = 0                # How many users' trajectory data are choosed
    TRAJACTORY_SCALE = 20               # How many trajectories are choosed per user
    RANGE = {                           # To pick trajectory points within the range
        'status': False
    }

    GROUP_SIZE_THRESHOLD     = 3        # group size threshold φ
    COHERENCE_THRESHOLD      = 0.4      # coherence threshold τ
    SCALING_FACTOR           = 1.5      # scaling factor δ
    TURNING_ALPHA            = 5        # tuning parameter α
    TURNING_BETA             = 2        # tuning parameter β

    RADIUS = SCALING_FACTOR * \
        ((-math.log(COHERENCE_THRESHOLD)) ** (1 / TURNING_ALPHA))


class Config_2:
    DATASET_ROOT_DIR = '../data/test2/Data'  # The data set root directory
    DATASET_SCALE    = 3                # How many users' trajectory data are choosed
    TRAJACTORY_SCALE = 4                # How many trajectories are choosed per user
    RANGE = {                           # To pick trajectory points within the range
        'status': True,
        'longitude_upper_bound': 116.32,
        'longitude_lower_bound': 116.304,
        'latitude_upper_bound': 40.018,
        'latitude_lower_bound': 40.004,
    }

    GROUP_SIZE_THRESHOLD    = 3         # group size threshold φ
    COHERENCE_THRESHOLD     = 0.99      # coherence threshold τ
    SCALING_FACTOR          = 15e-4     # scaling factor δ
    TURNING_ALPHA           = 5         # tuning parameter α
    TURNING_BETA            = 2         # tuning parameter β

    RADIUS = SCALING_FACTOR * \
        ((-math.log(COHERENCE_THRESHOLD)) ** (1 / TURNING_ALPHA))

class Config_3:
    DATASET_ROOT_DIR = '../data/test3/Data'  # The data set root directory
    DATASET_SCALE    = 0                # How many users' trajectory data are choosed
    TRAJACTORY_SCALE = 20               # How many trajectories are choosed per user
    RANGE = {                           # To pick trajectory points within the range
        'status': False
    }

    GROUP_SIZE_THRESHOLD    = 3         # group size threshold φ
    COHERENCE_THRESHOLD     = 0.49      # coherence threshold τ
    SCALING_FACTOR          = 1.1       # scaling factor δ
    TURNING_ALPHA           = 5         # tuning parameter α
    TURNING_BETA            = 2         # tuning parameter β

    RADIUS = SCALING_FACTOR * \
        ((-math.log(COHERENCE_THRESHOLD)) ** (1 / TURNING_ALPHA))


class Config(Config_3):
    __attr__ = ['DATASET_ROOT_DIR', 'DATASET_SCALE', 'TRAJACTORY_SCALE', 'RANGE',
        'GROUP_SIZE_THRESHOLD', 'COHERENCE_THRESHOLD', 'SCALING_FACTOR', 
        'TURNING_ALPHA', 'TURNING_BETA', 'RADIUS']

    def __str__(self):
        s = ""
        for attr in self.__attr__:
            s += attr + ' ' + str(getattr(self, attr)) + '\n'
        return s

    def __repr__(self):
        return self.__str__()