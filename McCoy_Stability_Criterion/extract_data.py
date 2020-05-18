import json
import sys
import csv

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

def get_thrust(lines, mass):
    time = []
    accel = []
    for i, line in enumerate(lines):
         if i > 1:
             time.append(float(line.split()[0]))
             accel.append(float(line.split()[1]) / mass[i - 2])
    small_timesteps = np.linspace(time[i], time[len(time)-1], 9525)
    accel = np.interp(small_timesteps, time, accel)
    return time, accel
    # time = [float(line.split()[0]) for i, line in enumerate(lines) if i > 1]
    # accel = [float(line.split()[1]) / mass for i, line in enumerate(lines) if i > 1]
    return time, accel

def get_rocket(path):
    rocket = {}
    with open(path, mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        # it's only iterable so we need this ugliness
        for line in reader:
            rocket = line
    return dict([key, float(value)] for key, value in rocket.items())

def get_motor_mass(time):
   #from data sheet of H550
    burn_time = 0.55
    motor_mass = 0.316
    prop_mass = 0.176
    dry_mass = motor_mass - prop_mass
   #linear interpolation of mass
   #TODO approximate using N5800 fit
    if time - time[0] < burn_time:
        loss_rate = prop_mass / burn_time
        motor_mass = motor_mass - loss_rate * time
    else:
        motor_mass = dry_mass
        
    return motor_mass
