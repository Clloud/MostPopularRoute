import math


class Config:
    DATASET_ROOT_DIR = '../test/Data'
    DATASET_SCALE = 0

    GROUP_SIZE_THRESHOLD = 3
    COHERENCE_THRESHOLD = 0.5

    SCALING_FACTOR = 200
    TURNING_ALPHA = 5
    TURNING_BETA = 2

    # reference: Paper PART III, PAGE 904
    RADIUS = SCALING_FACTOR * \
        ((-math.log(COHERENCE_THRESHOLD)) ** -TURNING_ALPHA)
