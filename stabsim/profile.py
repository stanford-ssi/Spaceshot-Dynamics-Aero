import numpy as np
from scipy import integrate
from .utility import read_csv, atmo_model
import matplotlib.pyplot as mpl
from stabsim.rocket import Rocket

class Profile:
    """
    Simulates a spin-stabilized launch profile
    
    Attributes
    ----------
    rocket : Rocket
        vehicle airframe
    motor : Motor
        vehicle motor
    init_spin : float
        spin speed (rad/s) at ignition
    aoa : float
        initial angle of attack (deg) interpreted as hangle
    tt : np.array
        discretization of time
    mass : np.array
        mass of vehicle at each time
    cg : np.array
        cg of vehicle (in m from nosecone) at each time
    altit : np.array
        altitude of vehicle (m) at each time
    vel : np.array
        velocity of vehicle (m/s) at each time
    rho : np.array
        density of vehicle (kg/m^3) at each time
    mach : np.array
        mach speed of vehicle (unitless) at each time

    Methods
    -------
    gyro_stab_crit() => np.array
        return minimum spin speed (rad/s) for gyroscopic stability at each time
    dynamic_stab_crit() => np.array
        return minimum spin speed (rad/s) for dynamic stability at each time
    spin() => np.array
        returns vehicle spin speed (rad/s) at each time
    is_stable() => boolean
        returns if flight is stable
    min_spin
        returns minimum spin speed (rad/s) for stable flight
    apogee
        returns apogee (m) of simulated flight - not apogee of total flight
    """
    G = -9.80665

    COARSE = 0
    NORMAL = 1
    FINE = 2
    # mach, altitude, and mass precision
    MODES = { 
        COARSE : (0.2, 1000, 0.2), 
        NORMAL : (0.1, 100, 0.1),
        FINE : (0.01, 20, 0.01)
    }

    def __init__(self, rocket, motor, init_spin, launch_altit=0, length=0, hangle=4, timesteps=50, mode=NORMAL):
        """
        Parameters
        ----------
        rocket : Rocket
        motor : Motor
        init_spin : float
        launch_altit : float, optional
            launch altitude (m)
        length : float, optional
            simulation length (s), if no input use motor burnout
        hangle : float, optional
            hangle (deg) interpreted as angle of attack
        timesteps : int, optional
            number of steps to break time into
        mode : int, optional
            fidelity of airframe coefficient memoization
        """
        # static constants
        self.rocket = rocket 
        self.motor = motor
        self.init_spin = init_spin
        self.aoa = hangle

        # time varying constants 
        if length == 0: 
            length = self.motor.t[-1]
        self.tt = np.linspace(0, length, timesteps)
        self.mass = np.array([self.motor.mass(t) + self.rocket.mass for t in self.tt])
        self.cg = np.array([self.motor.mass(t) * (self.rocket.cone_len + self.rocket.frame_len - self.motor.length / 2) for t in self.tt])
        self.cg = (self.rocket.mass * self.rocket.cg + self.cg) / self.mass

        # solve eqns of motion 
        z0 = [launch_altit, 0] # initial condition
        t = self.tt
        def model(z0, t):
            """
            Returns a list of (dxdt, dvdt) over t
            """
            alt, v = z0
            ind = np.abs(self.tt - t).argmin()

            # update vehicles aerodynamic coefficients while solving eqs of motion
            self.rocket.update_coeffs(self.mach(v=[v], alt=[alt]).tolist(), 
                self.aoa, [alt], [self.mass[ind]], [self.cg[ind]],
                precis=Profile.MODES[mode])

            dxdt = v
            dvdt = self.motor.thrust(t) * np.cos(np.radians(hangle)) / self.mass[ind] + \
                Profile.G + \
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

    def drag(self, x, v):
        cd = self.rocket.get_cd()
        ref_area = np.pi / 4 * (self.rocket.diameter ** 2)
        return -cd * ref_area  * 0.5 * (v ** 2) * self.rho([x])
    
    def lift(self, x, v):
        cl = self.rocket.get_cl_alpha()
        ref_area = np.pi / 4 * (self.rocket.diameter ** 2)
        return 0.5 * self.rho([x]) * (v ** 2) * ref_area * cl * np.sin(np.radians(self.aoa))

    def mach(self, v=-1, alt=-1):
        """"
        Mach speed of vehicle accounting for altitude
        """
        if v == -1:
            v = self.vel

        sos = 20.05 * np.sqrt(self.temp(alt))
        return v / sos

    def temp(self, alt=-1):
        """
        Temperature (K) at altitude using NRLMSISE00 atmospheric model
        """
        if alt == -1:
            alt = self.altit

        return np.array([atmo_model(x)[1] for x in alt])

    def rho(self, alt=-1):
        """
        Air density (kg/m^3) at altitude using NRLMSISE00 atmospheric model
        """
        if alt == -1:
            alt = self.altit

        return np.array([atmo_model(x)[0] for x in alt])

    def iz(self):
        """
        Moment of ineratia along axis of symmetry of vehicle
        """
        return np.array([self.rocket.iz + self.motor.iz(t) for t in self.tt])

    def ix(self):
        """
        Moment of inertia along axis perpendicular to axis of symmetry of vehicle
        """
        rocket_ix = self.rocket.ix + self.rocket.mass * (self.rocket.cg - self.cg)**2
        motor_cg = self.rocket.cone_len + self.rocket.frame_len - self.motor.length / 2
        motor_ix = np.array([self.motor.ix(t) for t in self.tt])
        motor_mass = np.array([self.motor.mass(t) for t in self.tt])
        motor_ix = motor_ix + motor_mass * (motor_cg - self.cg)**2
        return rocket_ix + motor_ix

    def gyro_stab_crit(self):
        """
        Minimum speed (rad/s) for stability of moving spinning top
        """
        cm = self.rocket.get_cm_alpha()
        cm[cm < 0] = 0 # static stability means no spin required!
        ref_area = np.pi / 4 * (self.rocket.diameter ** 2)
        radicand = 2 * self.rho * ref_area * self.rocket.diameter * cm * self.ix()
        gyro_spin_crit = self.vel / self.iz() * np.sqrt(radicand) 
        return gyro_spin_crit

    def dynamic_stab_crit(self):
        """
        Stability criterion (rad/s) with aerodynamic effects
        """
        cl = self.rocket.get_cl_alpha() # Lift force coeff
        cd = self.rocket.get_cd() # Drag coeff
        cm_adq = self.rocket.get_cm_dot() # Total pitch damping moment coefficient 
        cm_pa = self.rocket.get_cm_p_alpha() # Magnus moment coeff
        
        gyro = self.gyro_stab_crit()
        kx = np.sqrt(self.ix() / self.mass / self.rocket.diameter**2)
        kz = np.sqrt(self.iz() / self.mass / self.rocket.diameter**2)

        dyna = gyro * (cl - cd - (kx**-2) * cm_adq) / 2 / (cl + (kz**-2) * cm_pa)
        return dyna

    def spin(self):
        """
        Vehicle spin speed (rad/s) over flight
        """
        omega0 = self.init_spin
        C_spin = self.rocket.get_c_spin()

        def spin_damping(omega, t, C, profile):
            ind = np.abs(profile.tt - t).argmin()
            ref_area = np.pi / 4 * (profile.rocket.diameter ** 2)
            domegadt = 0.5 * C * profile.rho[ind] * profile.vel[ind] * ref_area * omega * profile.rocket.diameter
            return domegadt
        return integrate.odeint(spin_damping, omega0, self.tt, args=(C_spin, self))

    def is_stable(self):
        gyr = (self.spin() > self.gyro_stab_crit())[0]
        dyn = (self.spin() > self.dynamic_stab_crit())[0]
        return all(gyr) and all(dyn)

    def min_spin(self):
        gyro_max = np.max(self.gyro_stab_crit())
        dyn_max = np.max(self.dynamic_stab_crit())
        return round(max(gyro_max, dyn_max))

    def apogee(self):
        return round(np.max(self.altit))