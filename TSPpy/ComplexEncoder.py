import json
import numpy

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        elif isinstance(obj, numpy.int64):
            return int(obj)
        elif hasattr(obj,'repr_json'):
            return obj.repr_json()
        else:
            return json.JSONEncoder.default(self, obj)