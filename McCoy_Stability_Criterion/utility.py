import scipy
import numpy as np

def get_data(time, accel):
    vel = scipy.integrate.cumtrapz(accel, x=time)
    x_pos = scipy.integrate.cumtrapz(vel, x=time)

    #use pressure equations to calculate air density for each x_pos
    trop_x = np.argmax(x_pos < 11000)
    rho_trop = 1.225 * (288.15 / (288.15 + -0.0065 * x_pos[:trop_x]) ^ (1 + (9.8 * 0.02896) / (8.3145 * -0.0065))
    strat_x = np.argmax(x_pos < 20000)
    rho_strat = 0.364 * np.exp(-(9.8 * 0.02896 * x_pos[trop_x:strat_x]) / (8.3145 * 216.65))
    # assumed below the mesosphere (32km)
    rho_mes = 0.088 * (216.65 / (216.65 + 0.001 * x_pos[trop_x:strat_x]) ^ (1 + (9.8 * 0.02896) / (8.3145 * 0.001))

    return vel, x_pos, np.append(rho_trop, rho_mes, rho_strat)

def get_spin(vel, rho):
    return vel / 0.004 * np.sqrt(2 * rho * -.2352 * 0.0607 * 7 * 0.00607)
