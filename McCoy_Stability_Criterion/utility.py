from scipy import integrate
import numpy as np
import csv

def get_data(time, accel):
    vel = integrate.cumtrapz(accel, x=time, initial=0)
    x_pos = np.asarray(integrate.cumtrapz(vel, x=time, initial=0))

    #use pressure equations to calculate air density for each x_pos
    rho = []
    trop_x = np.argmax(x_pos > 11000)
    if trop_x == 0:
        trop_x = len(x_pos)
    rho.extend([1.225 * (288.15 / (288.15 + -0.0065 * x ** (1 + (9.8 * 0.02896) / (8.3145 * -0.0065)))) for x in x_pos[:trop_x]])

    strat_x = np.argmax(x_pos > 20000)
    if strat_x == 0:
        strat_x = len(x_pos)
    rho.extend([0.364 * np.exp(-(9.8 * 0.02896 * x / (8.3145 * 216.65))) for x in x_pos[trop_x:strat_x]])

    # assumed below the mesosphere (32km)
    rho.extend([0.088 * (216.65 / (216.65 + 0.001 * x ** (1 + (9.8 * 0.02896) / (8.3145 * 0.001)))) for x in x_pos[trop_x:strat_x]])

    return vel, x_pos, rho

def get_spin(vel, rho, path):
    rocket = {}
    with open(path, mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        # it's only iterable so we need this ugliness
        for line in reader:
            rocket = line
    rocket = dict([key, float(value)] for key, value in rocket.items())
    return [vel[i] / rocket['I_x'] * np.sqrt(2 * rho[i] * rocket['I_y'] * rocket['Surface Area'] * rocket['Calipers'] * rocket['Diameter']) for i in range(len(vel))]
