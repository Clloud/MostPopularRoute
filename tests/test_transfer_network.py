import sys
import os
root_path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
src_path = root_path + '\\src'
sys.path.append(src_path)

from transfer_network import TransferNetwork
from point import Point

a = TransferNetwork([],[
        [Point(1, 3, 1), Point(3, 1, 1), Point(1, 1, 2), Point(2, 2, 2)],
        [Point(5, 4, 2), Point(6, 3, 2), Point(6, 5, 3), Point(5, 4, 3)],
        [Point(3, 0, 1), Point(4, -1, 1), Point(4, 0, 3), Point(2, -2, 3)]
    ])

for node in a.nodes:
    print(node)

for i in range(len(a.edges)):
    for j in range(len(a.edges)):
        if a.edges[i][j] != -1:
            print("edge: ({}, {}) trajectory_id: {}".format(i, j, a.edges[i][j]))