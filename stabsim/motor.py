import csv
from .utility import read_csv
import numpy as np

"""
Simple model for a solid rocket motor for mechanical simulations
"""
class Motor:
    def __init__(self, wet_mass, dry_mass, radius, length, thrust_curve, time=-1, hole_radius=0.):
        self.wet_mass = wet_mass
        self.dry_mass = dry_mass
        self.radius = radius
        self.hole_radius = hole_radius
        self.length = length

        self.t = np.array([])
        self.thrust = None
        if time != -1:
            self.update_thrust(time, thrust_curve)

    @classmethod
    def empty(cls):
        return Motor(0, 0, 0, 0, [])

    @classmethod
    def fromfile(cls, rasp):
        spec = []
        with open(rasp, 'r') as thrust_curve:
            thrust_curve = list(thrust_curve)
            spec = thrust_curve[1].split()

        time, force = Motor.get_thrust(rasp)
        if time == -1:
            return time

        try:
            return cls(float(spec[5]), # wet mass
                float(spec[5]) - float(spec[4]), # dry mass
                float(spec[1]) / 2000, # radius
                float(spec[2]) / 1000, # length
                force, time=time)
        except ValueError:
            return -1

    @classmethod
    def fromfiles(cls, spec, rasp):
        motor = Motor.fromfile(rasp)
        if motor == -1:
            return motor
        else:
            return -1 if motor.set_spec(spec) == -1 else motor

    @classmethod
    def get_thrust(cls, file):
        with open(file, 'r') as thrust_curve:
            thrust_curve = list(thrust_curve) # allows you to iterate twice
            try:
                firsts = [line[0] for line in thrust_curve]
                firsts.reverse()
                start = len(thrust_curve) - firsts.index(';')
            except ValueError:
                start = -1

            try:
                time = [float(line.split()[0]) for i, line in enumerate(thrust_curve) if i > start]
                force = [float(line.split()[1]) for i, line in enumerate(thrust_curve) if i > start]
            except ValueError:
                return -1, -1
        return time, force
        
    def set_spec(self, file):
        dict = read_csv(file)
        try:
            self.wet_mass = float(dict['wet_mass']) if 'wet_mass' in dict else 0
            self.dry_mass = float(dict['dry_mass']) if 'dry_mass' in dict else 0
            self.radius = float(dict['radius']) if 'radius' in dict else 0
            self.length = float(dict['length']) if 'length' in dict else 0
            self.hole_radius = float(dict['width']) if 'width' in dict else 0
        except ValueError:
            return -1

    def update_thrust(self, *args):
        if len(args) == 1:
            time, force = Motor.get_thrust(args[0])
        elif len(args) == 2:
            time = args[0]
            force = args[1]
        else:
            return

        if time == -1:
            return -1
        if len(force) == 0:
            return
        
        try:
            iter(time)
            self.t = np.array(time)
        except TypeError:
            self.t = np.linspace(0, time, len(force))
        burn_time = time[-1]
        thrust_curve = np.polyfit(self.t, force, 4)
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