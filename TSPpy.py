from flask import Flask, render_template, request, jsonify
import numpy as np
from core import TSPSolver

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate_jordan')
def calculate_jordan():

    print('lol')
    size = request.args.get('width', 1, type=int)
    matrix = np.array([request.args.getlist('matrix[{}][]'.format(i), ) for i in range(size)], dtype = np.dtype(int))
    x = TSPSolver(matrix)
    print('wtf')
    x.run()

    return jsonify(matrix=[[0] * size] * size, message="OK", ok=True)
    return jsonify(matrix=[[0] * size] * size, message="Something went wrong :(", ok=False)
    # return jsonify(matrix=[[(x) for x in v] for v in j], message="Successfully calculated!", ok=True)


if __name__ == '__main__':
    app.run()
