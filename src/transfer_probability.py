from transfer_network import TransferNetwork
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
            # q, s = self.acquire(p)
            node.vector = self.cal_vector(q, s)

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

    # 点d与由point1和point2确定的直线之间的欧式距离
    def get_dist(self, d, point1, point2):
        a = point2.longitude - point1.longitude
        b = point1.latitude - point2.latitude
        c = point2.latitude * point1.longitude - point1.latitude * point2.longitude
        return (math.fabs(a * d.latitude + b * d.longitude + c)) / (math.pow(a * a + b * b, 0.5))

    # 创建P矩阵
    def create_transition_matrix(self, d):
        p = np.zeros((len(self.nodes), len(self.nodes)), dtype=float)
        p_row, p_col = p.shape[0], p.shape[1]
        for row in range(p_row):
            for col in range(p_col):
                p[row][col] = self.transition_probability(d, self.nodes[row], self.nodes[col])
        return p

    # 重构P矩阵，获得Q矩阵和S矩阵
    def reorganize(self, p, d):
        ABS = [node for node in self.nodes if
               (node == d or self.edges[self.nodes.index(node)] == [-1 for j in range(len(self.edges))])]
        TR = [node for node in self.nodes if
              not (node == d or self.edges[self.nodes.index(node)] == [-1 for j in range(len(self.edges))])]
        p_lefttop = p[np.ix_([self.nodes.index(tr) for tr in TR], [self.nodes.index(tr) for tr in TR])]
        p_leftbottom = p[np.ix_([self.nodes.index(ab) for ab in ABS], [self.nodes.index(tr) for tr in TR])]
        p_righttop = p[np.ix_([self.nodes.index(tr) for tr in TR], [self.nodes.index(ab) for ab in ABS])]
        p_rightbottom = p[np.ix_([self.nodes.index(ab) for ab in ABS], [self.nodes.index(ab) for ab in ABS])]
        return p_lefttop, p_righttop

    def acquire(self, p):
        pass

    def cal_vector(self, q, s):
        pass
