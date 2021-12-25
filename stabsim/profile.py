import numpy as np
from scipy import integrate
from .utility import read_csv, atmo_model
import matplotlib.pyplot as mpl
from stabsim.rocket import Rocket

"""
Simulates a spin-stabilized launch profile
"""
class Profile:
    def __init__(self, rocket, motor, init_spin, launch_altit=0, length=0, motor_pos=0, hangle=4, timesteps=50):
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
        self.mass = np.array([self.motor.mass(t) + self.rocket.mass for t in self.tt])
        self.cg = np.array([self.motor.mass(t) * (self.rocket.cone_len + self.rocket.frame_len - self.motor.length / 2) for t in self.tt])
        self.cg = (self.rocket.mass * self.rocket.cg + self.cg) / self.mass

        # Solve eqns of motion #
        z0 = [launch_altit, 0] # Initial condition
        t = self.tt

        def model(z0, t):
            #Function that returns a list of (dxdt, dvdt) over t
            # Equations based on https://www.overleaf.com/project/5fe249e8a42b0068add612ab
            alt, v = z0
            ind = np.abs(self.tt - t).argmin()

            self.rocket.update_coeffs(self.mach(v=[v], alt=[alt]).tolist(), self.aoa, [alt], [self.mass[ind]], [self.cg[ind]])

            dxdt = v
            dvdt = self.motor.thrust(t) * np.cos(np.radians(hangle)) / self.mass[ind] + \
                -9.80665 + \
                self.drag(alt, v) / (self.mass[ind]) + \
                self.lift(alt, v) / (self.mass[ind])
            dzdt = [dxdt, dvdt]

            return dzdt
        
        z = integrate.odeint(model, z0, t)
        self.altit = z[:,0]
        self.vel = z[:, 1]
        self.rho = self.rho()
        self.mach = self.mach()

        self.rocket.update_coeffs(self.mach.tolist(), self.aoa, self.altit, self.mass, self.cg)

        # import pprint
        # pprint.pprint(self.rocket.memoize)

    def drag(self, x, v):
        cd = self.rocket.get_cd()
        ref_area = np.pi / 4 * (self.rocket.diameter ** 2)
        return -cd * ref_area  * 0.5 * (v ** 2) * self.rho([x])
    
    def lift(self, x, v):
        cl = self.rocket.get_cl_alpha()
        ref_area = np.pi / 4 * (self.rocket.diameter ** 2)
        return 0.5 * self.rho([x]) * (v ** 2) * ref_area * cl * np.sin(np.radians(self.aoa))

    def mach(self, v=-1, alt=-1):
        if v == -1:
            v = self.vel

        sos = 20.05 * np.sqrt(self.temp(alt))
        return v / sos

    def temp(self, alt=-1):
        if alt == -1:
            alt = self.altit

        return np.array([atmo_model(x)[1] for x in alt])

    def rho(self, alt=-1):
        if alt == -1:
            alt = self.altit

        return np.array([atmo_model(x)[0] for x in alt])

    def iz(self):
        return np.array([self.rocket.iz + self.motor.iz(t) for t in self.tt])

    def ix(self):
        rocket_ix = self.rocket.ix + self.rocket.mass * (self.rocket.cg - self.cg)**2
        motor_cg = self.rocket.cone_len + self.rocket.frame_len - self.motor.length / 2
        motor_ix = np.array([self.motor.ix(t) for t in self.tt])
        motor_mass = np.array([self.motor.mass(t) for t in self.tt])
        motor_ix = motor_ix + motor_mass * (motor_cg - self.cg)**2
        return rocket_ix + motor_ix

    """
    Gyroscopic stability criterion in radians per second
    Stability of moving spinning top
    """
    def gyro_stab_crit(self):
        ref_area = np.pi / 4 * (self.rocket.diameter ** 2)
        gyro_spin_crit = self.vel / self.ix() * np.sqrt(2 * self.rho * self.iz() * ref_area * \
            np.abs(self.rocket.get_cm_alpha()) * self.rocket.diameter) 
        return np.abs(gyro_spin_crit)

    """
    McCoy dynamics stability criterion in radians per second
    Incorporates aerodynamic effects
    """
    def dynamic_stab_crit(self):
        cm_alpha = np.abs(self.rocket.get_cm_alpha()) # Overturning (a.k.a. pitching/rolling) moment coeff
        cl_alpha = self.rocket.get_cl_alpha() # Lift force coeff
        cd = self.rocket.get_cd() # Drag coeff
        cm_alpha_dot_plus_cm_q = self.rocket.get_cm_dot() # Pitch damping moment coefficient (due to rate of change of angle of attack plus tranverse angular velocity)
        cm_p_alpha = self.rocket.get_cm_p_alpha() # Magnus moment coeff
        ref_area = np.pi / 4 * (self.rocket.diameter ** 2)

        dyn_spin_crit = self.vel * np.sqrt(2 * self.rho * ref_area * self.rocket.diameter * cm_alpha * self.ix()) * \
            (cl_alpha - cd - ((self.mass * self.rocket.diameter ** 2 / self.ix()) * (cm_alpha_dot_plus_cm_q))) / \
            (2 * (self.iz() * cl_alpha + self.mass * self.rocket.diameter ** 2 * cm_p_alpha))
        return np.abs(dyn_spin_crit)

    def spin(self):
        omega0 = self.init_spin
        C_spin = self.rocket.get_c_spin()

        def spin_damping(omega, t, C, profile):
            ind = np.abs(profile.tt - t).argmin()
            ref_area = np.pi / 4 * (profile.rocket.diameter ** 2)
            domegadt = 0.5 * C * profile.rho[ind] * profile.vel[ind] * ref_area * omega * profile.rocket.diameter
            return domegadt
        return integrate.odeint(spin_damping, omega0, self.tt, args=(C_spin, self))

    def is_stable(self):
        return all(self.spin() > self.gyro_stab_crit()) and \
            all(self.spin() > self.dynamic_stab_crit())

    def min_spin(self):
        gyro_max = np.max(self.gyro_stab_crit())
        dyn_max = np.max(self.dynamic_stab_crit())
        return max(gyro_max, dyn_max)

    def apogee(self):
        return np.max(self.altit)