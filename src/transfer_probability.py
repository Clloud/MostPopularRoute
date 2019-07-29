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
        """
        Derive matrix P ,matrix Q ,matrix S and column vector V of each node.

        """
        for node in self.nodes:
            p = self.create_transition_matrix(node)
            q, s = self.reorganize(p, node)
            node.vector = self.cal_vector(node, p, q)

    def create_transition_matrix(self, d):
        """
        Construct the transition matrix P by function transition_probability.

        :param Point d: the destination node
        :return: matrix P

        """
        nodes_len = len(self.nodes)
        p = np.zeros((nodes_len, nodes_len), dtype=float)
        p_row, p_col = p.shape[0], p.shape[1]
        for row in range(p_row):
            for col in range(p_col):
                p[row][col] = self.transition_probability(d, self.nodes[row],
                                                          self.nodes[col])

        return p

    def transition_probability(self, d, nodei, nodej):
        """
        Get the transition probability of moving from nodei to nodej
        through the state of nodei and the subscripts of both nodes.

        :param Point d: the destination node
        :param Point nodei: the starting node of transition
        :param Point nodej: the ending node of transition
        :return: the transition probability

        """
        absorbing_state = [-1 for j in range(len(self.edges))]
        nodei_index = self.nodes.index(nodei)
        nodej_index = self.nodes.index(nodej)

        if (nodei == d or self.edges[nodei_index] == absorbing_state) \
                and nodei_index == nodej_index:
            return 1
        elif (not (nodei == d or self.edges[nodei_index] == absorbing_state)) \
                and nodei_index != nodej_index:
            return self.prd(d, nodei, nodej)
        else:
            return 0

    def prd(self, d, nodei, nodej):
        """
        Get the turning probability of moving from nodei to nodej
        through the ratio of adding func values of all the trajectories
        on (nodei,nodej) and all the trajectories starting from nodei.

        :param Point d: the destination node
        :param Point nodei: the starting node of transition
        :param Point nodej: the ending node of transition
        :return: the turning probability

        """
        sum_ij, sum_i = 0, 0
        nodei_index = self.nodes.index(nodei)
        nodej_index = self.nodes.index(nodej)

        # add func values of all the trajectories on (nodei,nodej)
        if self.edges[nodei_index][nodej_index] != -1:
            for t in self.edges[nodei_index][nodej_index]:
                sum_ij += self.func(t, d, nodei)

        # add func values of all the trajectories starting from nodei
        for col in range(len(self.edges)):
            if self.edges[nodei_index][col] != -1:
                for t in self.edges[nodei_index][col]:
                    sum_i += self.func(t, d, nodei)

        if sum_i == 0:
            return 0
        return sum_ij / sum_i

    def func(self, traj, d, nodei):
        """
        Estimate the likelihood that a trajectory traj might
        suggest a correct route to d.

        :param Point.trajectory_id traj: the trajectory
        :param Point d: the destination node
        :param Point nodei: the starting node
        :return: the likelihood

        """
        dists = sys.maxsize
        flag = 0
        traj_value = self.trajectories[traj]
        nodei_index_in_traj = \
            self.trajectories[traj].index(self.nodes.index(nodei))

        # trajectory traj passes node d ,dists = 0
        if self.nodes.index(d) in traj_value[nodei_index_in_traj::]:
            dists = 0
            flag = 1
        # trajectory traj only has one node rather than edge
        elif len(traj_value[nodei_index_in_traj::]) == 1:
            dists = math.pow(
                ((d.latitude - self.nodes[traj_value[0]].latitude) ** 2
                 + (d.longitude - self.nodes[traj_value[0]].longitude) ** 2),
                0.5)
            flag = 1
        # trajectory traj has one edge at least
        elif len(traj_value[nodei_index_in_traj::]) >= 2:
            for index in range(nodei_index_in_traj, len(traj_value) - 1):
                new_dist = self.get_dist(d, self.nodes[traj_value[index]],
                                         self.nodes[traj_value[index + 1]])
                if new_dist < dists:
                    dists = new_dist
                    flag = 1

        if flag == 0:
            return 0
        return math.exp(-dists)

    def get_dist(self, d, point1, point2):
        """
        Get the shortest Euclidean/network distance between d and
        the segment from point1 to point2.

        :param Point d: the point outside the segment
        :param Point point1: the endpoint of the segment
        :param Point point2: another endpoint of the segment
        :return: the distance

        """
        d_x = d.latitude
        d_y = d.longitude
        point1_x = point1.latitude
        point1_y = point1.longitude
        point2_x = point2.latitude
        point2_y = point2.longitude
        cross = (point2_x - point1_x) * (d_x - point1_x) \
                + (point2_y - point1_y) * (d_y - point1_y)
        dist2 = (point2_x - point1_x) ** 2 + (point2_y - point1_y) ** 2

        if cross <= 0:
            return math.sqrt((d_x - point1_x) ** 2 + (d_y - point1_y) ** 2)
        if cross >= dist2:
            return math.sqrt((d_x - point2_x) ** 2 + (d_y - point2_y) ** 2)
        r = cross / dist2
        p_x = point1_x + (point2_x - point1_x) * r
        p_y = point1_y + (point2_y - point1_y) * r
        return math.sqrt((d_x - p_x) ** 2 + (d_y - p_y) ** 2)

    def reorganize(self, p, d):
        """
        Reorganize matrix P to canonical form by grouping
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

    def matrix_multiply(self, a, n):
        """
        Calculate n power of matrix A.

        :param np.array a: matrix A
        :param int n: n power
        :return: matrix result

        """
        result = np.identity(a.shape[0])
        for i in range(n):
            result = np.dot(result, a)
        return result

    def step_t(self):
        """
        Set step t as the diameter of the transfer network by Floyd.

        :return: the diameter

        """
        edge_matrix_len = len(self.edges)
        weight = [[sys.maxsize for j in range(edge_matrix_len)]
                  for i in range(edge_matrix_len)]
        for i in range(edge_matrix_len):
            weight[i][i] = 0
            for j in range(edge_matrix_len):
                if self.edges[i][j] != -1 and i != j:
                    weight[i][j] = 1

        for k in range(edge_matrix_len):
            for i in range(edge_matrix_len):
                for j in range(edge_matrix_len):
                    if weight[i][j] > weight[i][k] + weight[k][j]:
                        weight[i][j] = weight[i][k] + weight[k][j]
        return max(max(weight))

    def cal_vector(self, d, p, q):
        """
        Get the column vector V of each node through matrix P and matrix Q.

        :param Point d: the node d
        :param np.array p: matrix P
        :param np.array q: matrix Q
        :return: column vector V

        """
        TR = []
        absorbing_state = [-1 for j in range(len(self.edges))]

        # D=S[*,d]
        for index, node in enumerate(self.nodes):
            if not (node == d or self.edges[index] == absorbing_state):
                TR.append(index)
        D = p[np.ix_(TR, [self.nodes.index(d)])]

        # V=D+Q·D+Q^2·D+...+Q^(t-1)·D
        v = np.zeros(D.shape)
        for j in range(0, self.step_t()):
            v = v + np.dot(self.matrix_multiply(q, j), D)
        return v
