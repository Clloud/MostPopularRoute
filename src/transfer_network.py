from point import Point


class TransferNetwork():
    def __init__(self, points, clusters):
        self.nodes = []
        self.edges = []
        self.trajectories = dict()
        self.create_transfer_node(clusters)
        self.create_transfer_edge(points, clusters)

    def create_transfer_node(self, clusters):
        for cluster in clusters:
            sum1, sum2 = 0, 0
            for point in cluster:
                sum1 += point.latitude
                sum2 += point.longitude
            node = Point(sum1 / len(cluster), sum2 / len(cluster))
            self.nodes.append(node)

    def create_transfer_edge(self, points, clusters):
        # 初始化，-1 表示两个cluster之间没有边相连, >=0 的数值表示相连边属于哪一条路径
        clusters_size = len(clusters)
        self.edges = [[-1 for col in range(clusters_size)] for row in range(clusters_size)]

        cluster_points = dict()
        cluster_point_ids = set()
        for index in range(len(clusters)):
            for point in clusters[index]:
                point.cluster_id = index
                cluster_points[point.id] = point
                cluster_point_ids.add(point.id)
        
        index = self.find_first_point_in_cluster(0, points, cluster_point_ids)
        previous_point = points[index]
        while index < len(points) - 1:
            index += 1
            point = points[index]
            # 当前点不在cluster中
            if point.id not in cluster_point_ids:
                continue
            # 当前点和前一个点在同一条轨迹上 且 当前点和前一个点不在同一个cluster中
            if point.trajectory_id == previous_point.trajectory_id \
                and point.cluster_id != previous_point.cluster_id:
                t_id = point.trajectory_id
                i = previous_point.cluster_id
                j = point.cluster_id
                # 保存路径
                self.save_edge(i, j, t_id)
                self.save_edge(j, i, t_id)
                self.save_trajectory(i, j, t_id)
                previous_point = point
            else:
                previous_point = points[index]

    def find_first_point_in_cluster(self, index, points, cluster_point_ids):
        # 找从index开始第一个位于cluster中的点
        for i in range(index, len(points)):
            # 找到
            if points[i].id in cluster_point_ids:
                return i
        return len(points) - 1
                
    def save_edge(self, i, j, t_id):
        if self.edges[i][j] == -1:
            self.edges[i][j] = []
        self.edges[i][j].append(t_id)

    def save_trajectory(self, i, j, t_id):
        if t_id not in self.trajectories.keys():
            self.trajectories[t_id] = []
        else:
            self.trajectories[t_id].pop()
        self.trajectories[t_id].append(i)
        self.trajectories[t_id].append(j)

    # # 二维矩阵保存 transfer edge ，矩阵的行和列均为 cluster的序号（无向图则该矩阵为对称的）
    # # -1 表示两个cluster之间没有边相连, >=0 的数值表示相连边属于哪一条路径（即trajectory_id）
    # def create_transfer_edge(self, points, clusters):
    #     clusters_size = len(clusters)
    #     # 初始化transfer edge矩阵
    #     self.edges = [[-1 for col in range(clusters_size)] for row in range(clusters_size)]

    #     for i in range(clusters_size):
    #         for j in range(i + 1, clusters_size):
    #             p_tid = -1
    #             for point in clusters[i]:
    #                 # 一条路径只使用一个点，因此cluster中有几条不同的路径则循环几次
    #                 if point.trajectory_id == p_tid:
    #                     continue
    #                 p_tid = point.trajectory_id

    #                 # 判断cluster[i]和cluster[j]是否有边相连
    #                 # point是以时间序存储在cluster中的，因此可保证第一个检查到的边即为有效的transfer edge
    #                 if self.trajectory_only_edge(p_tid, i, j) and \
    #                     self.trajectory_pass_cluster(p_tid, clusters[j]):
    #                     self.edges[i][j] = p_tid
    #                     self.edges[j][i] = p_tid

    # # 检查这条路径在cluster上是否有point（考虑point.id？）
    # def trajectory_pass_cluster(self, tid, cluster):
    #     for point in cluster:
    #         if point.trajectory_id == tid:
    #             return True
    #     return False

    # # 保证一条路径在一个cluster上只有一条transfer edge（按时间序）
    # def trajectory_only_edge(self, tid, i, j):
    #     for k in range(i + 1, j):
    #         if self.edges[i][k] == tid:
    #             return False
    #     return True