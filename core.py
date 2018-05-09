import heapq
import math
import numpy as np
from copy import copy, deepcopy

INF = 10000
BOUND = 1000

class Matrix:
    def __init__(self, a):
        self.init_size = a.shape[0]
        self.m = a.copy()
        self.paths_pool = []
        self.lower_bound = 0
        self.indices = [list(range(0, a.shape[0])), list(range(0, a.shape[0]))]
        self.min_cols = []
        self.min_rows = []

    def __enter__(self):
        return self

    def reduce_matrix(self):
        min_rows = self.m.min(axis=1)

        for i, j in np.ndindex(self.m.shape):
            self.m[i][j] -= min_rows[i]

        min_cols = self.m.min(axis=0)
        for i, j in np.ndindex(self.m.shape):
            self.m[i][j] -= min_cols[j]

        self.lower_bound += np.sum(min_rows) + np.sum(min_cols)
        self.min_rows = min_rows
        self.min_cols = min_cols

    def score_for_zeros(self):
        zero_score = np.zeros(self.m.shape)
        for i, j in np.ndindex(self.m.shape):
            if self.m[i][j] == 0:
                min_in_row = np.min(np.delete(self.m[i], j))
                min_in_col = np.min(np.delete(self.m[:, j], i))
                zero_score[i][j] = min_in_row + min_in_col

        return zero_score

    def include_edge(self, ind, jnd):

        self.m = np.delete(self.m, self.indices[0].index(ind), 0)
        self.m = np.delete(self.m, self.indices[1].index(jnd), 1)

        self.indices[0].remove(ind)
        self.indices[1].remove(jnd)

        start_of_new_path, end_of_new_path = [ind], [jnd]
        # print(self.paths_pool)
        for path in self.paths_pool:
            if path[-1] == ind:
                start_of_new_path = path[:]

            if path[0] == jnd:
                end_of_new_path = path[:]

        if start_of_new_path in self.paths_pool:
            self.paths_pool.remove(start_of_new_path)

        if end_of_new_path in self.paths_pool:
            self.paths_pool.remove(end_of_new_path)

        start_of_new_path.extend(end_of_new_path)
        self.paths_pool.append(start_of_new_path[:])
        if self.m.shape[0] > 2:
            self.m[self.indices[0].index(start_of_new_path[-1])][self.indices[1].index(start_of_new_path[0])] = INF

    def exlcude_edge(self, ind, jnd):
        self.m[self.indices[0].index(ind)][self.indices[1].index(jnd)] = INF


class TSPNode:

    def __init__(self, a):
        self.matrix = a
        self.priority = 0

    def is_final(self):
        return len(self.matrix.paths_pool) == 1 and \
               len(self.matrix.paths_pool[0]) == self.matrix.init_size

    def calc_split_edge(self):
        # TODO: REFACTOR
        self.matrix.reduce_matrix()
        zero_matrix = self.matrix.score_for_zeros()

        indcs = self.matrix.indices
        res = max([(zero_matrix[i][j], indcs[0][i], indcs[1][j])
                   for i, j in np.ndindex(self.matrix.m.shape)
                        if indcs[0][i] != indcs[1][j] and self.matrix.m[i][j] <= BOUND])
        print("lasdasdasd", res, res[1:])
        return res[1:]

    def get_path(self):
        if self.is_final():
            return self.matrix.paths_pool[0]

    def include_node(self, split_edge):
        self.matrix.include_edge(*split_edge)
        self.matrix.reduce_matrix()
        self.priority = self.matrix.lower_bound
        if self.priority == math.nan:
            self.priority = INF  # TODO
        return self

    def exclude_node(self, split_edge):
        self.matrix.exlcude_edge(*split_edge)
        self.matrix.reduce_matrix()
        self.priority = self.matrix.lower_bound
        return self


class TSPSolver:
    def __init__(self, m):
        self.m = Matrix(deepcopy(m))
        self.nodes_pool = None
        self.start_matrix = deepcopy(m)

    def eval_path(self, path):
        ans = 0
        # print(path)
        for i, _ in enumerate(path):
            # print(self.start_matrix[path[i - 1]][path[i]])
            ans += self.start_matrix[path[i - 1]][path[i]]
        return ans

    def run(self):
        print("miss you")
        self.nodes_pool = []

        main_node = TSPNode(self.m)

        best_len = INF * INF
        best_path = list(range(self.m.m.shape[0]))

        counter = 0
        heapq.heappush(self.nodes_pool, [1, counter, main_node])
        while len(self.nodes_pool) > 0 and counter <= 50:

            priority, _, node = heapq.heappop(self.nodes_pool)
            if priority > best_len:
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
                print(split_edge, node.matrix.m, node.matrix.indices, node.matrix.paths_pool, priority, sep="\n")
                print("#" * 40)

                InNode = deepcopy(node).include_node(split_edge)
                ExNode = deepcopy(node).exclude_node(split_edge)

                heapq.heappush(self.nodes_pool, [InNode.priority, 2 * counter, InNode])
                heapq.heappush(self.nodes_pool, [ExNode.priority, 2 * counter + 1, ExNode])

                counter += 1

        print(best_path, self.eval_path(best_path))


def run():
    a = np.array([[INF, 90, 80, 40, 100],
                  [60, INF, 40, 50, 70],
                  [50, 30, INF, 60, 20],
                  [10, 70, 20, INF, 50],
                  [20, 40, 50, 20, INF]])

    b = np.array([[INF, 1, 1, 1],
                  [1, INF, 1, 1],
                  [1, 1, INF, 1],
                  [1, 1, 1, INF]])

    c = np.array([[10000, 0, 0, 0, 1, 0],
                  [0, 10000, 1, 0, 0, 2],
                  [0, 0, 10000, 1, 0, 0],
                  [1, 0, 0, 10000, 2, 0],
                  [0, 0, 0, 0, 10000, 1],
                  [0, 0, 0, 0, 0, 10000], ])
    TSPSolver(c).run()
