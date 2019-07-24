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
        if (nodei == d or self.edges[self.nodes.index(nodei)] == [-1 for j in range(len(self.edges))]) \
                and nodei == nodej:
            return 1
        elif (not (nodei == d or self.edges[self.nodes.index(nodei)] == [-1 for j in range(len(self.edges))])) \
                and nodei != nodej:
            return self.prd(d, nodei, nodej)
        else:
            return 0

    def prd(self, d, nodei, nodej):
        sum_ij, sum_i = 0, 0
        # self.edges中所有轨迹中通过ni到nj的边
        for t in self.edges[self.nodes.index(nodei)][self.nodes.index(nodej)]:
            sum_ij += self.func(t, d)
        # self.edges中所有轨迹中通过ni出去的边
        for col in range(len(self.edges)):
            for t in self.edges[self.nodes.index(nodei)][col]:
                sum_i += self.func(t, d)
        # if sum_i == 0:
        #    return 0
        return sum_ij / sum_i

    def func(self, traj, d):
        dists = sys.maxsize
        if len(self.trajectories[traj]) == 1:
            dists = math.pow(((d.latitude - self.trajectories[traj][0].latitude) ** 2 +
                              (d.longitude - self.trajectories[traj][0].longitude) ** 2), 0.5)
        elif len(self.trajectories[traj]) >= 2:
            for index in range(len(self.trajectories[traj]) - 1):
                new_dist = self.get_dist(d, self.trajectories[traj][index], self.trajectories[traj][index + 1])
                if new_dist < dists:
                    dists = new_dist
        return math.exp(-dists)

    def get_dist(self, d, point1, point2):
        a = point2.longitude - point1.longitude
        b = point1.latitude - point2.latitude
        c = point2.latitude * point1.longitude - point1.latitude * point2.longitude
        return (math.fabs(a * d.latitude + b * d.longitude + c)) / (math.pow(a * a + b * b, 0.5))

    def create_transition_matrix(self, d):
        p = np.zeros((len(self.nodes), len(self.nodes)), dtype=float)
        p_row, p_col = p.shape[0], p.shape[1]
        for row in range(p_row):
            for col in range(p_col):
                p[row][col] = self.transition_probability(d, self.nodes[row], self.nodes[col])
        return p

    def reorganize(self, p, d):
        ABS = [node for node in self.nodes if
               (node == d or self.edges[self.nodes.index(node)] == [-1 for j in range(len(self.edges))])]
        TR = [node for node in self.nodes if
              not (node == d or self.edges[self.nodes.index(node)] == [-1 for j in range(len(self.edges))])]
        p_lefttop = p[np.ix_([self.nodes.index(tr) for tr in TR], [self.nodes.index(tr) for tr in TR])]
        p_leftbottom = p[np.ix_([self.nodes.index(abs) for abs in ABS], [self.nodes.index(tr) for tr in TR])]
        p_righttop = p[np.ix_([self.nodes.index(tr) for tr in TR], [self.nodes.index(abs) for abs in ABS])]
        p_rightbottom = p[np.ix_([self.nodes.index(abs) for abs in ABS], [self.nodes.index(abs) for abs in ABS])]
        return p_lefttop, p_righttop

    def acquire(self, p):
        pass

    def cal_vector(self, q, s):
        pass
