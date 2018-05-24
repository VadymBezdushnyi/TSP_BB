import heapq
import math
import numpy as np
import json

from ComplexEncoder import ComplexEncoder
from TSPMatrix import TSPMatrix, INF
from BBNode import BBNode

from copy import copy, deepcopy


MAXBB_ITERATIONS = 1500000


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

        best_len = INF * INF  # TODO
        best_path = list(range(self.m.matrix.shape[0]))

        iteration = 0
        json_objects = {}

        heapq.heappush(self.nodes_pool, main_node)
        json_objects[1] = main_node
        time_entries = [dict(created=[1], final=[], deleted=[])]
        order = []
        while len(self.nodes_pool) > 0 and iteration < MAXBB_ITERATIONS:

            node = heapq.heappop(self.nodes_pool)
            order.append(node.index)
            if node.priority >= best_len:
                break

            if node.is_final():
                time_entries.append(dict(created=[],
                                         final=[node.index],
                                         deleted=[]))
                path = node.get_path()
                best_len = self.eval_path(best_path)
                path_len = self.eval_path(path)
                node.tsp_matrix.paths_pool[0].append(node.tsp_matrix.paths_pool[0][0])  # TODO
                if best_len > path_len:
                    best_path = path
                    best_len = path_len
            else:

                split_edge = node.tsp_matrix.calc_split_edge(node.tsp_matrix)

                # print(split_edge)
                # print(node.tsp_matrix.matrix)
                # print(node.tsp_matrix.indices)
                # print(node.tsp_matrix.paths_pool)
                # print(node.priority)
                # # print("#" * 40)

                InNode = deepcopy(node).include_node(split_edge)
                InNode.index = 2 * node.index + 1
                json_objects[InNode.index] = InNode

                ExNode = deepcopy(node).exclude_node(split_edge)
                ExNode.index = 2 * node.index
                json_objects[ExNode.index] = ExNode

                heapq.heappush(self.nodes_pool, InNode)
                heapq.heappush(self.nodes_pool, ExNode)

                time_entries.append(dict(created=[InNode.index, ExNode.index],
                                         final=[],
                                         deleted=[node.index]))

                iteration += 1
        # print(json_objects)
        # print(iteration)
        # print(best_path, self.eval_path(best_path))
        return dict(nodes=json_objects,
                    time_entries=time_entries,
                    order=order,
                    best_path=best_path)
