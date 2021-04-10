import csv
from .utility import read_csv
import numpy as np

"""
Simple model for a solid rocket motor for mechanical simulations
"""
class Motor:
    def __init__(self, wet_mass, dry_mass, radius, length, thrust_curve, hole_radius=0., burn_time=4.):
        self.wet_mass = wet_mass
        self.dry_mass = dry_mass
        self.radius = radius
        self.hole_radius = hole_radius
        self.length = length

        #TODO: thrust data might not be in equal increments
        self.t = np.linspace(0, burn_time, len(thrust_curve))
        thrust_curve = np.polyfit(self.t, thrust_curve, 4)
        thrust_curve = np.poly1d(thrust_curve)
        def thrust(t):
            if t <= burn_time:
                return thrust_curve(t)
            return 0
        self.thrust = thrust

    def wet_mass_variable(self, time):
        return self.mass(time) - self.dry_mass

    def inner_radius(self, time):
        propellant_density = self.wet_mass / np.pi / self.length /(self.radius**2 - self.hole_radius**2)
        return np.sqrt((self.radius**2) - (self.wet_mass_variable(time) / (propellant_density * np.pi * self.length))) #derived from density equation

    # Moment of inertia along the axis of symmetry of rocket
    def iz(self, time):
        iz_dry_mass = 0.5 * self.dry_mass * self.radius**2 # 2 thin disks (iz = 1/2*(dry mass/2)r^2) on either end
        iz_wet_mass = max(0.5 * self.wet_mass_variable(time) * ((self.radius**2) + (self.inner_radius(time)**2)), 0) #cylinder with hole in center
        return iz_dry_mass + iz_wet_mass

    # Moment of inertia not along axis of symmetry of rocket
    def ix(self, time):
        ix_dry = 2 * (0.125 * self.dry_mass * self.radius**2 + 0.5 * self.dry_mass * (self.length/2)**2)  # 2 thin disks (ix = 1/4(dry mass/2)r^2) on either end, with parallel axis theorem ((dry mass/2)d^2)
        ix_wet = max((1/12) * self.wet_mass_variable(time) * (3 * (self.radius**2 + self.inner_radius(time)**2) + self.length**2), 0) #cylinder with hole in center
        return ix_dry + ix_wet

    def mass(self, time):        
        # values extrapolated through simple linear approximation
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
        force, hole_radius=motor["width"], burn_time=time[-1])  
