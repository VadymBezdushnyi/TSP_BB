import heapq
import math
import numpy as np
import json
import TSPMatrix

from copy import copy, deepcopy

INF = 1000000
BOUND = 1000



class BBNode:

    def __init__(self, tsp_matrix, index):
        self.tsp_matrix = tsp_matrix
        self.index = index
        self.priority = 0

    def __lt__(self, other):
        return (self.priority / self.tsp_matrix.matrix.shape[0], self.index) <\
        (other.priority / self.tsp_matrix.matrix.shape[0], other.index)

    def repr_json(self):
        return dict(tsp_matrix = self.tsp_matrix,
                    index = self.index,
                    priority = self.priority)

    def is_final(self):
        return len(self.tsp_matrix.paths_pool) == 1 and \
               len(self.tsp_matrix.paths_pool[0]) == self.tsp_matrix.init_size

    def calc_split_edge(self):
        # TODO: remove to TSPMatrix
        self.tsp_matrix.reduce_matrix()
        self.tsp_matrix.calc_zero_score()

        indcs = self.tsp_matrix.indices
        res = max([(self.tsp_matrix.zero_score[i][j], indcs[0][i], indcs[1][j])
                   for i, j in np.ndindex(self.tsp_matrix.matrix.shape)
                   if indcs[0][i] != indcs[1][j] and self.tsp_matrix.matrix[i][j] <= BOUND])
        return res[1:]

    def get_path(self):
        if self.is_final():
            return self.tsp_matrix.paths_pool[0]

    def include_node(self, split_edge):
        self.tsp_matrix.include_edge(*split_edge)
        self.tsp_matrix.reduce_matrix()
        self.priority = self.tsp_matrix.lower_bound
        if self.priority == math.nan:
            self.priority = INF  # TODO
        return self

    def exclude_node(self, split_edge):
        self.tsp_matrix.exclude_edge(*split_edge)
        self.tsp_matrix.reduce_matrix()
        self.priority = self.tsp_matrix.lower_bound
        return self
