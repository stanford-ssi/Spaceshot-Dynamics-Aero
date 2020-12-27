import numpy as np
from scipy import integrate
from .utility import read_csv

"""
Simulates a spin-stabilized launch profile
"""
class Profile:
    def __init__(self, rocket, motor, init_spin, launch_altit=0, length=0, motor_pos=0, hangle=0, timesteps=50):
        self.rocket = read_csv(rocket)
        self.motor = motor
        self.init_spin = init_spin
        self.length = length
        # assume a length==0 implies simulation should end at end of motor burn
        if self.length == 0:
            self.length = self.motor.burn_time
        self.motor_pos = motor_pos

        # thrust is set to polynomial fit to get equally spaced timesteps for subsequent calcs
        t = np.linspace(0, self.motor.burn_time, len(self.motor.thrust))
        # simple integration and Newton's second
        self.tt = np.linspace(0, self.length, timesteps)
        self.mass = np.array([self.motor.mass(t) + self.rocket["Mass"] for t in self.tt])
        self.gravity = np.array([(self.rocket["Mass"] + self.motor.mass(t))* -9.80665 \
            for t in self.tt])
        # TODO: double check with prop that polynomial fit is sufficient and ask abt degree
        thrust = np.polyfit(t, self.motor.thrust, 4)
        self.thrust = thrust
        force = np.poly1d(thrust) + self.gravity # TODO: subtract the drag and gravity

        # Mass calcuations over time
        self.accel = np.array([force(t) / (self.motor.mass(t) + self.rocket["Mass"]) \
            for t in self.tt])
        vel = np.array(integrate.cumtrapz(self.accel, x=self.tt, initial=0))
        self.vel = vel 
        self.altit = np.array(integrate.cumtrapz(vel * np.cos(hangle), x=self.tt, initial=0)) + launch_altit
        self.launch_altit = launch_altit

    def odeint(self):
        # Returns a list of [x, v] over t
        z0 = [self.launch_altit, self.vel[0]]       # Initial condition
        t = self.tt
        z = integrate.odeint(self.model, z0, t)
        return z

    def model(self, z, t):
        #Function that returs a list of (dxdt, dvdt) over t
        # Hangle assumed to be 0
        # Equations based on https://www.overleaf.com/project/5fe249e8a42b0068add612ab
        x, v = z
        dxdt = v
        dvdt = self.thrust[t] / (self.mass[t]) + -9.80665 + self.drag[t] / (self.mass[t])
        dzdt = [dxdt, dvdt]
        return dzdt

    def drag(self):
        # ref_area and cd values missing
        return np.array([self.cd * self.ref_area * self.gravity[t] * 0.5 * (self.vel[t] ** 2) * self.rho  \
            for t in self.tt])

    def rho(self):
        temperature = -131.21 + .00299 * self.altit
        pressure = 2.488 * ((temperature + 273.1) / 216.6) ** -11.388
        rho = pressure / (0.2869 * (temperature + 273.1))
        return rho

    def iz(self):
        return np.array([self.rocket["I_z"] + self.motor.iz(time) + self.motor.mass(time) * self.motor_pos**2 \
            for time in self.tt])

    def ix(self):
        return np.array([self.rocket["I_x"] + self.motor.ix(time) + self.motor.mass(time) * self.motor_pos**2 \
            for time in self.tt])

    def gyro_stab_crit(self):
        # TODO: the number of calipers also changes as motor burns and CG changes, add fcn for this too
        return self.vel / self.ix() * np.sqrt(2 * self.rho() * self.iz() * self.rocket['Surface Area'] * \
            self.rocket['Calipers'] * self.rocket['Diameter']) 

    def dynamic_stab_crit(self):
        # McCoy dynamics stability criterion in radians per second
        # TODO: fill in values for coefficients
        cm_alpha = 1 # Pitching/rolling moment coeff
        cl_alpha = 1 # Lift force coeff
        cd = 1 # Drag coeff
        cm_q = 1 # Pitch damping moment due to transverse angular velocity
        cm_alpha_dot = 1 # Pitch damping moment coeff due to rate of change of angle of attack
        cm_p_alpha = 1 # Magnus moment coeff
        dyn_spin_crit = self.vel * np.sqrt(2 * self.rho() * self.rocket['Surface Area'] * self.rocket['Diameter'] * cm_alpha * self.ix()) * \
            (cl_alpha - cd - (self.mass * self.rocket['Diameter'] ** 2 / self.ix()) * (cm_q + cm_alpha_dot)) / \
                (2 * (self.iz() * cl_alpha + self.mass * self.rocket['Diameter'] ** 2 * cm_p_alpha))
        return np.abs(dyn_spin_crit)

    def spin(self):
        omega0 = self.init_spin
        C_spin = -10

        def spin_damping(omega, t, C, profile):
            ind = np.abs(profile.tt - t).argmin()

            ref_area = np.pi / 4 * (profile.rocket['Diameter'] ** 2)
            domegadt = 0.5 * C * profile.rho()[ind] * profile.vel[ind] * ref_area * omega * profile.rocket['Diameter']
            return domegadt

        return integrate.odeint(spin_damping, omega0, self.tt, args=(C_spin, self))

    def is_stable(self):
        return self.stab_crit() < self.spin()

    def min_spin(self):
        # TODO: incorporate skin drag despin
        return np.max(self.stab_crit())