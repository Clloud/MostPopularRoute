import math

        
class Config_1:
    DATASET_ROOT_DIR = 'E:\\Files\\Project\\2019暑期科研\\test1\\Data'
    DATASET_SCALE = 0
    TRAJACTORY_SCALE = 20
    RANGE = {
        'status': False
    }

    GROUP_SIZE_THRESHOLD = 2
    COHERENCE_THRESHOLD = 0.3
    SCALING_FACTOR = 1.2
    TURNING_ALPHA = 5
    TURNING_BETA = 2

    RADIUS = SCALING_FACTOR * \
        ((-math.log(COHERENCE_THRESHOLD)) ** -TURNING_ALPHA)


class Config_2:
    # 数据集根目录
    DATASET_ROOT_DIR = 'E:\\Files\\Project\\2019暑期科研\\test2\\Data'
    # 选取前几个用户的轨迹数据
    DATASET_SCALE = 3
    # 选取前几条轨迹
    TRAJACTORY_SCALE = 4
    # 有效坐标点的范围(False表示范围无限制)
    RANGE = {
        'status': True,
        'longitude_upper_bound': 116.32,
        'longitude_lower_bound': 116.304,
        'latitude_upper_bound': 40.018,
        'latitude_lower_bound': 40.004,
    }

    # 组尺寸φ
    GROUP_SIZE_THRESHOLD = 3
    # 连贯性阈值τ
    COHERENCE_THRESHOLD = 0.99
    # 比例参数δ
    SCALING_FACTOR = 100
    # 转向参数α
    TURNING_ALPHA = 5
    # 转向参数β
    TURNING_BETA = 2

    RADIUS = SCALING_FACTOR * \
        ((-math.log(COHERENCE_THRESHOLD)) ** -TURNING_ALPHA)


class Config(Config_1):
    pass
