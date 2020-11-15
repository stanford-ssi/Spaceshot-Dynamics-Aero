import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

# All in SI units
# m is mass of propellant, must add mass of total rocket including airframe and engine
#The following numbers are from the N5800 burn data

time = [0, 0.019, 0.049, 0.103, 0.384, 1.109, 1.569, 1.991, 2.622, 3.011, 3.192, 3.334, 3.423, 3.513, 3.581, 3.594]
thrust = [0, 6694.9, 6720.29, 6593.33, 6677.97, 6957.28, 6940.35, 6720.29, 6009.33, 3275.51, 2606.86, 1599.67, 1041.05, 389.337, 220.06, 0]
propellant_mass = [9.425, 9.39557, 9.30245, 9.13611, 8.27327, 5.98604, 4.5069, 3.17309, 1.31463, 0.478961, 0.232618, 0.0944131, 0.0400353, 0.0102497, 0.000661903, 0]


g = 9.8


#TODO hangle
# Dry mass "m"
m = 11
# TODO: calculate
Cd = 0.75

# Spin damping moment coefficient TODO: calculate

Clp = 0.03

# Actual reference area TBD, below is just approximate cross-sectional area of rockets in meters squared
ref_area = 0.008107319269
diameter = 0.5

# Moment of inertia about axis of symmetry (kg m^2)
#TODO: Moment of Inertia FunctionS
momentOfInertiaX = .004

# Initial velocity (m/s) (Must initialize with nonzero value, or division by zero with omega update)
starting_velocity = 1

# Angular velocity in rad/second about axis of rocket symmetry
omega_0 = 315
starting_altitude = 26000

# Can adjust interval number
num_of_intervals = 3000
time_approx_curve = np.linspace(0, 240, num=num_of_intervals)
time_interval = time_approx_curve[1] - time_approx_curve[0]

# Creates thrust array
thrust_approx_curve = np.zeros(num_of_intervals)
for i in range(num_of_intervals):
    thrust_approx_curve[i] = np.interp(time_approx_curve[i], time, thrust)

# Creates total mass array
airframe_and_engine_mass = m * np.ones(16)
mass = np.zeros(16)
for i in range(16):
    mass[i] = airframe_and_engine_mass[i] + propellant_mass[i]

mass_approx_curve = np.zeros(num_of_intervals)
for i in range(num_of_intervals):
    mass_approx_curve[i] = np.interp(time_approx_curve[i], time, mass)


def air_density(altitude):
    air_density_in_kg_cubic_meters = (2.488*(((.00299*altitude-131.21)+273.1)/216.6)**(-11.388))/(.2869*((.00299*altitude-131.21)+273.1))
    return air_density_in_kg_cubic_meters

velocity_curve = np.zeros(num_of_intervals)
omega_curve = np.zeros(num_of_intervals)
air_density_curve = np.zeros(num_of_intervals)
altitude_curve = np.zeros(num_of_intervals)
altitude = starting_altitude

V = starting_velocity
omega = omega_0
for i in range(num_of_intervals):
    velocity_curve[i] = V
    omega_curve[i] = omega
    air_density_curve[i] = air_density(altitude)
    altitude_curve[i] = altitude
    thrust = thrust_approx_curve[i]

    # Update drag force
    drag = 0.5 * air_density_curve[i] * (V ** 2.0) * Cd * ref_area

    # Update gravitational force
    Fg = mass_approx_curve[i]*g

    # Net force is thrust minus drag minus gravitational force
    F = thrust - drag - Fg

    # Acceleration is net force over mass
    A = F / mass_approx_curve[i]

    altitude = altitude + (V * time_interval) + (0.5 * A * (time_interval ** 2.0))

    # Update velocity
    # velocity = v0 + A * delta t
    V = V + A * time_interval

    # Update spin rate omega based on spin damping moment
    # omega = omega - torque / moment of inertia * delta t
    omega = omega-0.5*(air_density_curve[i]*abs(V)**2*ref_area * diameter * (omega * diameter/ abs(V)) * Clp / momentOfInertiaX) * time_interval

# Set up Pyplot figure with subplots for altitude, velocity, air density, dynamic pressure, spin rate
fig, axs= plt.subplots(5)
fig.suptitle('Altitude, Velocity, Air Density, Dynamic Pressure, and Spin Rate after ignition')
plt.xlabel("Time after motor ignition (seconds)")

# Plot altitude
axs[0].plot(time_approx_curve, altitude_curve,'tab:orange')
axs[0].set(ylabel='Altitude (m)')


# Plot normalized velocity curve with approximate Speed of Sound at 30km, ie Mach Number
# Plot speed of sound as function of altitude
axs[1].plot(time_approx_curve, abs(velocity_curve/300))
axs[1].set(ylabel='Mach Number')

# Plot air density
axs[2].plot(time_approx_curve, air_density_curve, 'tab:green')
axs[2].set(ylabel='Air density (kg/m^3)')


# Plot dynamic pressure
axs[3].plot(time_approx_curve, .5*air_density_curve*velocity_curve**2, 'tab:purple')
axs[3].set(ylabel= 'Q (N/M^2)')

# Plot spin rate
axs[4].plot(time_approx_curve, omega_curve, color = 'r')
axs[4].set(ylabel = 'Spin Rate (rad/sec)')

# Plot end of burn
axs[4].set_ylim(bottom = 0)
axs[4].axvline(x = 3.594, color = 'r',linestyle="dashed", label = "end of burn")
min_spin = min(range(len(time_approx_curve)), key=lambda i: abs(time_approx_curve[i]-3.594))
axs[4].axhline(y = omega_curve[min_spin], color = 'r',linestyle="dotted", label = "spin at end burn")
print(omega_curve[min_spin])

for ax in axs.flat:
    ax.label_outer()
    ax.grid()
plt.show()