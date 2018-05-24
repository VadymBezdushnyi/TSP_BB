class BBNode:

    def __init__(self, tsp_matrix, index):
        self.tsp_matrix = tsp_matrix
        self.index = index
        self.priority = 0

    def __lt__(self, other):
        return (self.priority / self.tsp_matrix.matrix.shape[0], -self.index) < \
               (other.priority / self.tsp_matrix.matrix.shape[0], -other.index)

    def repr_json(self):
        return dict(tsp_matrix=self.tsp_matrix,
                    index=self.index,
                    priority=self.priority)

    def is_final(self):
        return len(self.tsp_matrix.paths_pool) == 1 and \
               len(self.tsp_matrix.paths_pool[0]) == self.tsp_matrix.init_size

    def get_path(self):
        if self.is_final():
            return self.tsp_matrix.paths_pool[0]

    def include_node(self, split_edge):
        self.tsp_matrix.include_edge(*split_edge)
        self.tsp_matrix.reduce_matrix()
        self.priority = self.tsp_matrix.lower_bound
        return self

    def exclude_node(self, split_edge):
        self.tsp_matrix.exclude_edge(*split_edge)
        self.tsp_matrix.reduce_matrix()
        self.priority = self.tsp_matrix.lower_bound
        return self
