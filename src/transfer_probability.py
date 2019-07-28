import math
import sys
import numpy as np


class TransferProbability:
    def __init__(self, network):
        self.nodes = network.nodes
        self.edges = network.edges
        self.trajectories = network.trajectories
        self.derive()

    def derive(self):
        for node in self.nodes:
            p = self.create_transition_matrix(node)
            self.reorganize(p, node)
            q, s = self.reorganize(p, node)
            node.vector = self.cal_vector(node, p, q, s)
    
    # 创建P矩阵
    def create_transition_matrix(self, d):
        p = np.zeros((len(self.nodes), len(self.nodes)), dtype=float)
        p_row, p_col = p.shape[0], p.shape[1]
        for row in range(p_row):
            for col in range(p_col):
                p[row][col] = self.transition_probability(d, self.nodes[row], self.nodes[col])
        return p

    def transition_probability(self, d, nodei, nodej):
        # nodei is an absorbing state and i=j
        if (nodei == d or self.edges[self.nodes.index(nodei)] == [-1 for j in range(len(self.edges))]) \
                and self.nodes.index(nodei) == self.nodes.index(nodej):
            return 1

        # nodei is a transient state and i!=j
        elif (not (nodei == d or self.edges[self.nodes.index(nodei)] == [-1 for j in range(len(self.edges))])) \
                and self.nodes.index(nodei) != self.nodes.index(nodej):
            return self.prd(d, nodei, nodej)

        # otherwise
        else:
            return 0

    def prd(self, d, nodei, nodej):
        sum_ij, sum_i = 0, 0

        # self.edges中所有轨迹中通过ni到nj的边
        if self.edges[self.nodes.index(nodei)][self.nodes.index(nodej)] != -1:
            for t in self.edges[self.nodes.index(nodei)][self.nodes.index(nodej)]:
                sum_ij += self.func(t, d, nodei)

        # self.edges中所有轨迹中通过ni出去的边
        for col in range(len(self.edges)):
            if self.edges[self.nodes.index(nodei)][col] != -1:
                for t in self.edges[self.nodes.index(nodei)][col]:
                    sum_i += self.func(t, d, nodei)

        # sum_i=0表示从nodei无法转移到后续的任意其他node
        if sum_i == 0:
            return 0

        return sum_ij / sum_i

    def func(self, traj, d, nodei):
        # 初始值为无穷大
        dists = sys.maxsize
        flag = 0

        # 若路径traj从nodei之后的部分经过点d，则dists=0
        if self.nodes.index(d) in self.trajectories[traj][self.trajectories[traj].index(self.nodes.index(nodei))::]:
            dists = 0
            flag = 1

        # 若路径traj从nodei之后的部分只有一个点而没有边，则dists为点d与该点间的距离
        elif len(self.trajectories[traj][self.trajectories[traj].index(self.nodes.index(nodei))::]) == 1:
            dists = math.pow(((d.latitude - self.nodes[self.trajectories[traj][0]].latitude) ** 2 +
                              (d.longitude - self.nodes[self.trajectories[traj][0]].longitude) ** 2), 0.5)
            flag = 1

        # 若路径traj从nodei之后的部分有至少两个点，则dists为点d到边的最短距离
        elif len(self.trajectories[traj][self.trajectories[traj].index(self.nodes.index(nodei))::]) >= 2:
            for index in range(self.trajectories[traj].index(self.nodes.index(nodei)),
                               len(self.trajectories[traj]) - 1):
                new_dist = self.get_dist(d, self.nodes[self.trajectories[traj][index]],
                                         self.nodes[self.trajectories[traj][index + 1]])
                if new_dist < dists:
                    dists = new_dist
                    flag = 1

        # flag=0，即dists仍为无穷大，则表明func=0
        if flag == 0:
            return 0

        return math.exp(-dists)

    # 点d与由point1和point2确定的线段之间的欧式距离
    def get_dist(self, d, point1, point2):
        cross = (point2.latitude - point1.latitude) * (d.latitude - point1.latitude) + \
                (point2.longitude - point1.longitude) * (d.longitude - point1.longitude)
        if cross <= 0:
            return math.sqrt((d.latitude - point1.latitude) ** 2 + (d.longitude - point1.longitude) ** 2)
        dist2 = (point2.latitude - point1.latitude) ** 2 + (point2.longitude - point1.longitude) ** 2
        if cross >= dist2:
            return math.sqrt((d.latitude - point2.latitude) ** 2 + (d.longitude - point2.longitude) ** 2)
        r = cross / dist2
        p_x = point1.latitude + (point2.latitude - point1.latitude) * r
        p_y = point1.longitude + (point2.longitude - point1.longitude) * r
        return math.sqrt((d.latitude - p_x) ** 2 + (d.longitude - p_y) ** 2)

    def reorganize(self, p, d):
        """
        Reorgnize matrix P to canoical form by grouping 
        absorbing states into ABS and transient states into TR.

        :param np.array p: matrix P
        :param Point d: the destination node
        :return: matrix Q(TR * TR), matrix S(TR * ABS)

        """
        ABS = []
        TR = []
        absorbing_state = [-1 for j in range(len(self.edges))]
        for index, node in enumerate(self.nodes):
            if node == d or self.edges[index] == absorbing_state:
                ABS.append(index)
            else:
                TR.append(index)
        
        p_left_top = p[np.ix_(TR, TR)]
        p_left_bottom = p[np.ix_(ABS, TR)]
        p_right_top = p[np.ix_(TR, ABS)]
        p_right_bottom = p[np.ix_(ABS, ABS)]

        return p_left_top, p_right_top

    # 矩阵乘方
    def matrix_multiply(self, a, n):
        # 初始化为单位矩阵
        matrix_result = np.identity(a.shape[0])
        for i in range(n):
            new_a = np.dot(matrix_result, a)
            matrix_result = new_a
        return matrix_result

    # 计算t步之内的概率，这里设置t为transfer network的直径（利用Floyd算法）
    def step_t(self):
        edge_matrix_len = len(self.edges)
        edge_weight = [[sys.maxsize for j in range(edge_matrix_len)] for i in range(edge_matrix_len)]
        for i in range(edge_matrix_len):
            edge_weight[i][i] = 0
            for j in range(edge_matrix_len):
                if self.edges[i][j] != -1 and i != j:
                    edge_weight[i][j] = 1
        for k in range(edge_matrix_len):
            for i in range(edge_matrix_len):
                for j in range(edge_matrix_len):
                    if edge_weight[i][j] > edge_weight[i][k] + edge_weight[k][j]:
                        edge_weight[i][j] = edge_weight[i][k] + edge_weight[k][j]
        return max(max(edge_weight))

    # 列向量V
    def cal_vector(self, d, p, q, s):
        # D=S[*,d]
        TR = [node for node in self.nodes if
              not (node == d or self.edges[self.nodes.index(node)] == [-1 for j in range(len(self.edges))])]
        D = p[np.ix_([self.nodes.index(tr) for tr in TR], [self.nodes.index(d)])]
        # V=D+Q·D+Q^2·D+...+Q^(t-1)·D
        v = np.zeros(D.shape)
        for j in range(0, self.step_t()):
            v = v + np.dot(self.matrix_multiply(q, j), D)
        return v
