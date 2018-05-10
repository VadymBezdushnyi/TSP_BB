import heapq
import math
import numpy as np
import json

from ComplexEncoder import ComplexEncoder
from TSPMatrix import TSPMatrix
from BBNode import BBNode

from copy import copy, deepcopy

INF = 10000
BOUND = 1000


class TSPSolver:
    def __init__(self, m):
        self.m = TSPMatrix(deepcopy(m))
        self.nodes_pool = None
        self.start_matrix = deepcopy(m)

    def eval_path(self, path):
        ans = 0
        for i, _ in enumerate(path):
            ans += self.start_matrix[path[i - 1]][path[i]]
        return ans

    def run(self):
        self.nodes_pool = []

        main_node = BBNode(self.m, 1)
        print(json.dumps(main_node.repr_json(), cls=ComplexEncoder))

        best_len = INF * INF
        best_path = list(range(self.m.matrix.shape[0]))

        counter = 0
        heapq.heappush(self.nodes_pool, main_node)
        while len(self.nodes_pool) > 0 and counter <= 50:

            node = heapq.heappop(self.nodes_pool)
            if node.priority > best_len:
                break

            if node.is_final():
                path = node.get_path()
                best_len = self.eval_path(best_path)
                path_len = self.eval_path(path)
                if best_len > path_len:
                    best_path = path
                    best_len = path_len
            else:

                split_edge = node.calc_split_edge()
                print(split_edge, node.tsp_matrix.matrix, node.tsp_matrix.indices,
                      node.tsp_matrix.paths_pool, node.priority, sep = '\n')
                print("#" * 40)

                InNode = deepcopy(node).include_node(split_edge)
                InNode.index = 2 * node.index

                ExNode = deepcopy(node).exclude_node(split_edge)
                ExNode.index = 2 * node.index + 1

                heapq.heappush(self.nodes_pool, InNode)
                heapq.heappush(self.nodes_pool, ExNode)

                counter += 1

        print(best_path, self.eval_path(best_path))
