import csv
from .utility import read_csv
import numpy as np

"""
Simple model for a solid rocket motor for mechanical simulations
"""
class Motor:
    def __init__(self, wet_mass, dry_mass, radius, length, thrust_curve, width=0., burn_time=4.):
        self.wet_mass = wet_mass
        self.dry_mass = dry_mass
        self.radius = radius
        self.width = width
        self.length = length

        self.t = np.linspace(0, burn_time, len(thrust_curve))
        thrust_curve = np.polyfit(self.t, thrust_curve, 4)
        thrust_curve = np.poly1d(thrust_curve)
        def thrust(t):
            if t <= burn_time:
                return thrust_curve(t)
            return 0
        self.thrust = thrust

    def iz(self, time):
        max_iz = 0.5 * self.wet_mass * self.radius**2
        min_iz = 0.5 * self.dry_mass * (self.radius**2 + (self.radius - self.width)**2)
        
        # values extrapolated through simple linear approximation
        # TODO: talk with prop about how accurate this is
        linear_approx = (max_iz - min_iz) * ((self.t[-1] - time) / self.t[-1]) + min_iz
        return max(linear_approx, min_iz)

    def ix(self, time):
        max_ix = 1 / 12 * self.wet_mass * (3 * self.radius**2 + self.length**2)
        min_ix = 1 / 12 * self.dry_mass * (3 * (self.radius**2 + (self.radius - self.width)**2) \
            + self.length**2)

        # values extrapolated through simple linear approximation
        # TODO: talk with prop about how accurate this is 
        linear_approx = (max_ix - min_ix) * ((self.t[-1] - time) / self.t[-1]) + min_ix
        return max(linear_approx, min_ix)

    def mass(self, time):        
        # values extrapolated through simple linear approximation
        # TODO: talk with prop about how accurate this is
        linear_approx = (self.wet_mass - self.dry_mass) * ((self.t[-1] - time) / self.t[-1]) + self.dry_mass
        return max(linear_approx, self.dry_mass) 

def load_motor(spec, thrust_curve):
    # get motor values from csv or spreadsheet
    motor = read_csv(spec)

    # get thrust values from txt file, usually found online
    time = []
    force = []
    with open(thrust_curve, 'r') as thrust_curve:
        thrust_curve = list(thrust_curve) # allows you to iterate twice
        time = [float(line.split()[0]) for i, line in enumerate(thrust_curve) if i > 1]
        force = [float(line.split()[1]) for i, line in enumerate(thrust_curve) if i > 1]

    return Motor(motor["wet_mass"], motor["dry_mass"], motor["radius"], motor["length"], \
        force, width = motor["width"], burn_time=time[-1])  