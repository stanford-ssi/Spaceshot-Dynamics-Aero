import numpy as np
from scipy import integrate
from .utility import read_csv

"""
Simulates a spin-stabilized launch profile
"""
class Profile:
    def __init__(self, rocket, motor, init_spin, launch_altit=0, length=0, motor_pos=0, hangle=0, timesteps=50):
        # Static constants #
        self.rocket = rocket
        self.motor = motor
        self.init_spin = init_spin
        self.motor_pos = motor_pos
        

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
                self.drag(ind, x * np.cos(hangle), v, cd=0.6) / (self.mass[ind])
            dzdt = [dxdt, dvdt]
            return dzdt
        
        z = integrate.odeint(model, z0, t)
        self.altit = z[:,0] * np.cos(hangle)
        self.vel = z[:, 1]

    def drag(self, t, x, v, cd = 0):
        ref_area = np.pi / 4 * (self.rocket.static_params['Diameter'] ** 2)
        return -cd * ref_area  * 0.5 * (v ** 2) * self.rho([x])

    def rho(self, x=-1):
        if x == -1:
            x = self.altit

        rho = []
        for altit in x:
            if altit < 11000:
                temperature = 15.04 - .00649 * altit
                pressure = 101.29 * ((temperature + 273.1) / 288.08) ** 5.256
            elif altit >= 11000 and altit < 25000:
                temperature = -56.46
                pressure = 22.65 * (2.718281828459045) ** (1.73 - .000157 * altit)
            else:
                temperature = -131.21 + .00299 * altit
                pressure = 2.488 * ((temperature + 273.1) / 216.6) ** -11.388
            rho.append(pressure / (.2869 * (temperature + 273.1)))
        
        return np.array(rho)

    def iz(self):
        return np.array([self.rocket.static_params["I_z"] + self.motor.iz(time) + self.motor.mass(time) * self.motor_pos**2 \
            for time in self.tt])

    def ix(self):
        return np.array([self.rocket.static_params["I_x"] + self.motor.ix(time) + self.motor.mass(time) * self.motor_pos**2 \
            for time in self.tt])

    def c_m_pa(self, vel):
        # TODO: do this lol
        pass

    """
    Gyroscopic stability criterion in radians per second
    Stability of moving spinning top
    """
    def gyro_stab_crit(self):
        # TODO: the number of calipers also changes as motor burns and CG changes, add fcn for this too
        return self.vel / self.ix() * np.sqrt(2 * self.rho() * self.iz() * self.rocket.static_params['Surface Area'] * \
            self.rocket.static_params['Calipers'] * self.rocket.static_params['Diameter']) 

    """
    McCoy dynamics stability criterion in radians per second
    Incorporates aerodynamic effects
    """
    def dynamic_stab_crit(self):
        # TODO: fill in values for coefficients
        # The following coefficients were received from: https://www.hindawi.com/journals/ijae/2020/6043721/
        cm_alpha = 4 # Overturning (a.k.a. pitching/rolling) moment coeff (Figure 6e)
        cl_alpha = 2.5 # Lift force coeff (Figure 6c)
        cd = 0.6 # Drag coeff (Figure 5)
        cm_q = 0 # Pitch damping moment due to transverse angular velocity
        cm_alpha_dot = -50 # Pitch damping moment coeff due to rate of change of angle of attack
        cm_p_alpha = 1 # Magnus moment coeff
        dyn_spin_crit = self.vel * np.sqrt(2 * self.rho() * self.rocket.static_params['Surface Area'] * self.rocket.static_params['Diameter'] * cm_alpha * self.ix()) * \
            (cl_alpha - cd - ((self.mass * self.rocket.static_params['Diameter'] ** 2 / self.ix()) * (cm_q + cm_alpha_dot))) / \
                (2 * (self.iz() * cl_alpha + self.mass * self.rocket.static_params['Diameter'] ** 2 * cm_p_alpha))
        return dyn_spin_crit

    def spin(self):
        omega0 = self.init_spin
        C_spin = -1

        def spin_damping(omega, t, C, profile):
            ind = np.abs(profile.tt - t).argmin()
            ref_area = np.pi / 4 * (profile.rocket['Diameter'] ** 2)
            domegadt = 0.5 * C * profile.rho()[ind] * profile.vel[ind] * ref_area * omega * profile.rocket['Diameter']
            return domegadt

        return integrate.odeint(spin_damping, omega0, self.tt, args=(C_spin, self))

    def is_stable(self):
        return all(self.spin() > self.gyro_stab_crit()) and \
            all(self.spin() > self.dynamic_stab_crit())

    def min_spin(self):
        gyro_max = np.max(self.gyro_stab_crit())
        dyn_max = np.max(self.dynamic_stab_crit())
        return max(gyro_max, dyn_max)