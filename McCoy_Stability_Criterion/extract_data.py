import json
import sys

def flatten(data, prefix=""):
    flat = {}
    if isinstance(data, dict):
        if prefix:
            prefix += "."
        for k, v in data.items():
            flat.update(flatten(v, prefix + str(k)))
        return flat
    if isinstance(data, list):
        if prefix:
            prefix += "."
        i = 0
        for v in data:
            flat.update(flatten(v, prefix + str(i)))
            i += 1
        return flat
    return {prefix:data}

def get_column(lines, column):
    json_body = []
    id = []
    stack = []
    bat = {"cellA":[],"cellB":[]}

    for line in lines:
        try:
            data = json.loads(line)
            if data["id"] == "sensor":
                try:
                    flat = flatten(data)
                    flat["id"] = 0.0 #Need to handle enumerated states!
                    flt = dict()
                    for key in flat:
                        flt[key] = float(flat[key])
                    json_body += [flt]
                except KeyError:
                    print('keyError')
                    print(line)
        except ValueError:
            print('line not JSON')

    data = [[data[key] for data in json_body] for key in ["tick","adxl1.a.0","adxl1.a.1","adxl1.a.2","bmi1.a.0","bmi1.a.1","bmi1.a.2"]]
    data[0] = [(a)/1000 for a in data[0]]
    return data[0], data[column]
