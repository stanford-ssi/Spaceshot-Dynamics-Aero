import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize


# Primary author is Umar Patel, with contributions from John Bailey
'''m is mass of propellant, must add mass of total rocket including airframe and engine'''
'''The following numbers are from the N5800 burn data'''

time = [0, 0.019, 0.049, 0.103, 0.384, 1.109, 1.569, 1.991, 2.622, 3.011, 3.192, 3.334, 3.423, 3.513, 3.581, 3.594]
thrust = [0, 6694.9, 6720.29, 6593.33, 6677.97, 6957.28, 6940.35, 6720.29, 6009.33, 3275.51, 2606.86, 1599.67, 1041.05, 389.337, 220.06, 0]
propellant_mass = [9.425, 9.39557, 9.30245, 9.13611, 8.27327, 5.98604, 4.5069, 3.17309, 1.31463, 0.478961, 0.232618, 0.0944131, 0.0400353, 0.0102497, 0.000661903, 0]
'''propellant type is C-Star'''

'''All inputs will be in SI-units. In the code we will convert to Stupid American units bc NASA equations are in those'''
'''m would be mass of airframe plus mass of engine'''
'''total mass would be mass of airframe and mass of engine plus mass of propellant'''
'''mass is in kg'''
m = 17.401
'''coefficient of drag below, will need to calculate when we receive specifics on '''
Cd = 0.75
'''Actual reference area TBD, below is just approximate cross-sectional area of rockets in meters squared'''
ref_area = 0.008107319269
'''velocity in meters/second'''
starting_velocity = 0
'''altitude in meters'''
starting_altitude = 26000


'''You can change num_of_intervals to however many intervals you want'''
num_of_intervals = 300
time_approx_curve = np.linspace(0, 3.594, num=num_of_intervals)
time_interval = time_approx_curve[1] - time_approx_curve[0]

'''creates thrust array'''
thrust_approx_curve = np.zeros(num_of_intervals)
for i in range(num_of_intervals):
    thrust_approx_curve[i] = np.interp(time_approx_curve[i], time, thrust)


'''creates total mass array'''
airframe_and_engine_mass = m * np.ones(16)
mass = np.zeros(16)
for i in range(16):
    mass[i] = airframe_and_engine_mass[i] + propellant_mass[i]

mass_approx_curve = np.zeros(num_of_intervals)
for i in range(num_of_intervals):
    mass_approx_curve[i] = np.interp(time_approx_curve[i], time, mass)

def air_density(altitude_in_feet):
    air_density_in_slugs_per_cubic_feet = (51.97 * (((254.65 + (0.00164 * altitude_in_feet)) / 389.98)**(-11.388))) / (1718.0 * (254.65 + (0.00164 * altitude_in_feet)))
    conversion_to_kg_per_cubic_meter = air_density_in_slugs_per_cubic_feet * 515.379
    return conversion_to_kg_per_cubic_meter

def conversion_from_meters_to_feet(meters):
    return meters * 3.28084

velocity_curve = np.zeros(num_of_intervals)
air_density_curve = np.zeros(num_of_intervals)
altitude_curve = np.zeros(num_of_intervals)
altitude = starting_altitude
instantaneous_velocity = starting_velocity
for i in range(num_of_intervals):
    velocity_curve[i] = instantaneous_velocity
    air_density_curve[i] = air_density(conversion_from_meters_to_feet(altitude))
    altitude_curve[i] = altitude

    instantaneous_thrust = thrust_approx_curve[i]
    instantaneous_drag = 0.5 * air_density_curve[i] * (instantaneous_velocity ** 2.0) * Cd * ref_area
    instantaneous_net_force = instantaneous_thrust - instantaneous_drag
    instantaneous_acceleration = instantaneous_net_force / mass_approx_curve[i]
    altitude = altitude + (instantaneous_velocity * time_interval) + (0.5 * instantaneous_acceleration * (time_interval ** 2.0))
    instantaneous_velocity = instantaneous_velocity + instantaneous_acceleration * time_interval



fig, axs= plt.subplots(4)
fig.suptitle('Altitude, Velocity, Air Density, and Dynamic Pressure after ignition')
plt.xlabel("Time after motor ignition (seconds)")
axs[0].plot(time_approx_curve, altitude_curve,'tab:orange')
axs[0].set(ylabel='Altitude (m)')
axs[1].plot(time_approx_curve, velocity_curve)
axs[1].set(ylabel='Velocity (m/s)')
axs[2].plot(time_approx_curve, air_density_curve, 'tab:green')
axs[2].set(ylabel='Air density (kg/m^3)')
axs[3].plot(time_approx_curve, .5*air_density_curve*velocity_curve**2, 'tab:red')
axs[3].set(ylabel= 'Q (N/M^2)')
for ax in axs.flat:
    ax.label_outer()

plt.show()


