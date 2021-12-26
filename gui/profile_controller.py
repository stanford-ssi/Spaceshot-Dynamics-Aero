from stabsim.profile import Profile
from stabsim.rocket import Rocket
from stabsim.motor import *
import stabsim.vis as vis

class Controller:
    def __init__(self):
        self.rocket = Rocket.empty()
        self.motor = Motor.empty()
        
        self.init_spin = 0
        self.launch_altit = 0
        self.length = 0
        self.hangle = 0
        self.timesteps = 0
        self.mode = Profile.NORMAL

        self.profile = None

    def new_profile(self):
        self.profile = Profile(self.rocket, self.motor, self.init_spin, 
            launch_altit=self.launch_altit, 
            length=self.length, 
            hangle=self.hangle, 
            timesteps=self.timesteps,
            mode=self.mode)

    def vis(self):
        kinem = vis.kinematics(self.profile, rho=True, show=False)
        rocket = vis.rocket(self.profile, label_mach=True, show=False)
        spin = vis.spin(self.profile, label_end=True, label_mach=True, show=False)
        motor = vis.motor(self.motor, show=False)
        return motor, rocket, kinem, spin

    def clear(self):
        self.rocket = Rocket.empty()
        self.motor = Motor.empty()
        
        self.init_spin = 0
        self.launch_altit = 0
        self.length = 0
        self.hangle = 0
        self.timesteps = 0