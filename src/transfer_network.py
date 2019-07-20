from point import Point


class TransferNetwork():
    def __init__(self, points, clusters):
        self.nodes = []
        self.edges = []
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

    # 二维矩阵保存 transfer edge ，矩阵的行和列均为 cluster的序号（无向图则该矩阵为对称的）
    # -1 表示两个cluster之间没有边相连, >=0 的数值表示相连边属于哪一条路径（即trajectory_id）
    def create_transfer_edge(self, points, clusters):
        clusters_size = len(clusters)
        # 初始化transfer edge矩阵
        self.edges = [[-1 for col in range(clusters_size)] for row in range(clusters_size)]

        for i in range(clusters_size):
            for j in range(i + 1, clusters_size):
                p_tid = -1
                for point in clusters[i]:
                    # 一条路径只使用一个点，因此cluster中有几条不同的路径则循环几次
                    if point.trajectory_id == p_tid:
                        continue
                    p_tid = point.trajectory_id

                    # 判断cluster[i]和cluster[j]是否有边相连
                    # point是以时间序存储在cluster中的，因此可保证第一个检查到的边即为有效的transfer edge
                    if self.trajectory_only_edge(p_tid, i, j) and \
                        self.trajectory_pass_cluster(p_tid, clusters[j]):
                        self.edges[i][j] = p_tid
                        self.edges[j][i] = p_tid

    # 检查这条路径在cluster上是否有point（考虑point.id？）
    def trajectory_pass_cluster(self, tid, cluster):
        for point in cluster:
            if point.trajectory_id == tid:
                return True
        return False

    # 保证一条路径在一个cluster上只有一条transfer edge（按时间序）
    def trajectory_only_edge(self, tid, i, j):
        for k in range(i + 1, j):
            if self.edges[i][k] == tid:
                return False
        return True