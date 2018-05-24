import numpy as np

INF = 1000000
MAX_VALUE = 1000

class TSPMatrix:
    def __init__(self, input_matrix):
        self.init_size = input_matrix.shape[0]
        self.init_matrix = input_matrix.copy()
        self.matrix = input_matrix.copy()
        self.zero_score = np.zeros(input_matrix.shape)
        self.paths_pool = []
        self.lower_bound = 0
        self.indices = [list(range(0, input_matrix.shape[0])),
                        list(range(0, input_matrix.shape[0]))]
        self.min_cols = []
        self.min_rows = []

    def __enter__(self):
        return self

    def repr_json(self):
        return dict(init_matrix=self.init_matrix,
                    matrix=self.matrix,
                    zero_score=self.zero_score,
                    paths_pool=self.paths_pool,
                    lower_bound=self.lower_bound,
                    indices=self.indices,
                    min_cols=self.min_cols,
                    min_rows=self.min_rows
                    )

    def reduce_matrix(self):
        min_rows = self.matrix.min(axis=1)
        for i, j in np.ndindex(self.matrix.shape):
            self.matrix[i][j] -= min_rows[i]

        min_cols = self.matrix.min(axis=0)
        for i, j in np.ndindex(self.matrix.shape):
            self.matrix[i][j] -= min_cols[j]

        self.lower_bound += np.sum(min_rows) + np.sum(min_cols)
        self.min_rows = min_rows
        self.min_cols = min_cols

    def calc_zero_score(self):
        self.zero_score = np.zeros(self.matrix.shape)
        for i, j in np.ndindex(self.matrix.shape):
            if self.matrix[i][j] == 0:
                min_in_row = np.min(np.delete(self.matrix[i], j))
                min_in_col = np.min(np.delete(self.matrix[:, j], i))
                self.zero_score[i][j] = min_in_row + min_in_col

    def include_edge(self, ind, jnd):

        self.matrix = np.delete(self.matrix, self.indices[0].index(ind), 0)
        self.matrix = np.delete(self.matrix, self.indices[1].index(jnd), 1)

        self.indices[0].remove(ind)
        self.indices[1].remove(jnd)

        start_of_new_path, end_of_new_path = [ind], [jnd]

        # set back edge to infinity
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

        if self.matrix.shape[0] > 1:
            self.matrix[self.indices[0].index(start_of_new_path[-1])][self.indices[1].index(start_of_new_path[0])] = INF

    def exclude_edge(self, ind, jnd):
        self.matrix[self.indices[0].index(ind)][self.indices[1].index(jnd)] = INF


    def calc_split_edge(self, tsp_matrix):
        self.reduce_matrix()
        self.calc_zero_score()

        indcs = self.indices
        # find best edge with zero score
        res = max([(tsp_matrix.zero_score[i][j], indcs[0][i], indcs[1][j])
                   for i, j in np.ndindex(tsp_matrix.matrix.shape)
                   if indcs[0][i] != indcs[1][j] and tsp_matrix.matrix[i][j] <= MAX_VALUE])
        return res[1:]