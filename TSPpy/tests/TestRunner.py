import numpy as np
from TSPpy.TSPSolver import TSPSolver

INF = 10000000
BOUND = 10000000
def readTest(input_file):
    a = []
    for line in input_file:
        s = line.split()
        a.append(s)
    a = np.array(a, dtype=int)
    np.fill_diagonal(a, INF)
    return a

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

    with open('42.txt') as f:
        d = readTest(f)
        print(d)

    TSPSolver(d).run()
