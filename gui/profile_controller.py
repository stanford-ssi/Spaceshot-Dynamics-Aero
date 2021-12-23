from stabsim.profile import Profile
from stabsim.rocket import Rocket
from stabsim.motor import *
import stabsim.vis as vis

import sys
sys.path.append("..")
import os

class Controller:
    def __init__(self):
        self.rocket = Rocket(None)
        self.motor = Motor(0, 0, 0, 0, [])
        
        self.init_spin = 0
        self.launch_altit = 0
        self.length = 0
        self.hangle = 0
        self.timesteps = 0

        # self.script_dir = os.pfath.join(os.path.dirname(__file__), '..')

    def run(self):
        profile = Profile(self.rocket, self.motor, self.init_spin, 
            launch_altit=self.launch_altit, 
            length=self.length, 
            hangle=self.hangle, 
            timesteps=self.timesteps)
        kinem = vis.kinematics(profile, show=False)
        spin = vis.spin(profile, show=False)
        motor = vis.motor(self.motor, show=False)
        return motor, kinem, spin