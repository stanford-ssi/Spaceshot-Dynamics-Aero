import numpy as np
from scipy import integrate
from .utility import read_csv, atmo_model
import matplotlib.pyplot as mpl
from stabsim.rocket import Rocket

"""
Simulates a spin-stabilized launch profile
"""
class Profile:
    def __init__(self, rocket, motor, init_spin, launch_altit=0, length=0, motor_pos=0, hangle=0, timesteps=50):
        # Static constants #
        self.rocket = rocket # This should be from the Rocket class
        self.motor = motor
        self.init_spin = init_spin
        self.motor_pos = motor_pos
        self.aoa = hangle


        # Time varying constants #
        if length == 0: # assume a length==0 implies simulation should end at end of motor burn
            length = self.motor.t[-1]
        self.tt = np.linspace(0, length, timesteps)
        self.mass = np.array([self.motor.mass(t) + self.rocket.static_params["Mass"] for t in self.tt])


        # Solve eqns of motion #
        z0 = [launch_altit, 0] # Initial condition
        t = self.tt

        def model(z0, t):
            #Function that returs a list of (dxdt, dvdt) over t
            # Equations based on https://www.overleaf.com/project/5fe249e8a42b0068add612ab
            x, v = z0
            dxdt = v
            ind = np.abs(self.tt - t).argmin()
            dvdt = self.motor.thrust(t) / (self.mass[ind]) + -9.80665 + \
                self.drag(ind, x * np.cos(hangle), v) / (self.mass[ind])
            dzdt = [dxdt, dvdt]
            return dzdt
        
        z = integrate.odeint(model, z0, t)
        self.altit = z[:,0] * np.cos(hangle)
        self.vel = z[:, 1]

        self.rocket.update_coeffs(self.vel, self.aoa, self.altit, self.mass)

    def drag(self, t, x, v, cd = 0):
        cd = self.rocket.get_cd()
        ref_area = np.pi / 4 * (self.rocket.static_params['Diameter'] ** 2)
        return -cd * ref_area  * 0.5 * (v ** 2) * self.rho([x])

    def rho(self, altit=-1):
        if altit == -1:
            altit = self.altit

        return np.array([atmo_model(x)[0] for x in altit])

    def iz(self):
        return np.array([self.rocket.static_params["I_z"] + self.motor.iz(time) + self.motor.mass(time) * self.motor_pos**2 \
            for time in self.tt])

    def ix(self):
        return np.array([self.rocket.static_params["I_x"] + self.motor.ix(time) + self.motor.mass(time) * self.motor_pos**2 \
            for time in self.tt])

    """
    Gyroscopic stability criterion in radians per second
    Stability of moving spinning top
    """
    def gyro_stab_crit(self):
        print(self.rocket.get_cm_alpha())
        return self.vel / self.ix() * np.sqrt(2 * self.rho() * self.iz() * self.rocket.static_params['Surface Area'] * \
            self.rocket.get_cm_alpha() * self.rocket.static_params['Diameter']) 

    """
    McCoy dynamics stability criterion in radians per second
    Incorporates aerodynamic effects
    """
    def dynamic_stab_crit(self):
        cm_alpha = self.rocket.get_cm_alpha() # Overturning (a.k.a. pitching/rolling) moment coeff
        cl_alpha = self.rocket.get_cl_alpha() # Lift force coeff
        cd = self.rocket.get_cd() # Drag coeff
        cm_alpha_dot_plus_cm_q = self.rocket.get_cm_alpha_dot_plus_cm_q() # Pitch damping moment coefficient (due to rate of change of angle of attack plus tranverse angular velocity)
        cm_p_alpha = self.rocket.get_cm_p_alpha() # Magnus moment coeff

        dyn_spin_crit = self.vel * np.sqrt(2 * self.rho() * self.rocket.static_params['Surface Area'] * self.rocket.static_params['Diameter'] * cm_alpha * self.ix()) * \
            (cl_alpha - cd - ((self.mass * self.rocket.static_params['Diameter'] ** 2 / self.ix()) * (cm_alpha_dot_plus_cm_q))) / \
                (2 * (self.iz() * cl_alpha + self.mass * self.rocket.static_params['Diameter'] ** 2 * cm_p_alpha))
        return dyn_spin_crit

    def spin(self):
        omega0 = self.init_spin
        C_spin = self.rocket.get_c_spin()

        def spin_damping(omega, t, C, profile):
            ind = np.abs(profile.tt - t).argmin()
            ref_area = np.pi / 4 * (profile.rocket.static_params['Diameter'] ** 2)
            domegadt = 0.5 * C * profile.rho()[ind] * profile.vel[ind] * ref_area * omega * profile.rocket.static_params['Diameter']
            return domegadt
        return integrate.odeint(spin_damping, omega0, self.tt, args=(C_spin, self))

    def is_stable(self):
        return all(self.spin() > self.gyro_stab_crit()) and \
            all(self.spin() > self.dynamic_stab_crit())

    def min_spin(self):
        gyro_max = np.max(self.gyro_stab_crit())
        dyn_max = np.max(self.dynamic_stab_crit())
        return max(gyro_max, dyn_max)