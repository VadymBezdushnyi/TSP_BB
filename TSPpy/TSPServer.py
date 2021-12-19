import numpy as np
import json
from flask import Flask, render_template, request, jsonify


from TSPpy.ComplexEncoder import ComplexEncoder
from TSPpy.TSPSolver import TSPSolver
from TSPpy import app

import flask_profiler

app.config["flask_profiler"] = {
    "enabled": True,
    "storage": {
        "engine": "sqlite"
    },
    "basicAuth":{
        "enabled": True,
        "username": "admin",
        "password": "admin"
    },
    "ignore": [
	    "^/static/.*"
	]
}

@app.route('/')
def index():
    print('keh')
    return render_template('index.html')

flask_profiler.init_app(app)

@app.route('/calculate')
@flask_profiler.profile()
def calculate():
    try:
        size = request.args.get('width', 1, type=int)
        matrix = np.array([request.args.getlist('matrix[{}][]'.format(i), ) for i in range(size)], dtype=np.dtype(int))
        x = TSPSolver(matrix)
        json_result = x.run()
        print(json_result)
    except:
        return jsonify(message="Something went wrong :(", ok=False)
    return json.dumps(dict(result=json_result, message="OK", ok=True), cls=ComplexEncoder)


if __name__ == '__main__':
    print('qweeh')
    app.run(port=7321)
