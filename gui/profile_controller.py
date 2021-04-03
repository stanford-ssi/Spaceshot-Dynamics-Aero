import sys
sys.path.append("..")

from stabsim.motor import load_motor
from stabsim.profile import Profile
from stabsim.rocket import Rocket
import stabsim.vis as vis

import os

class Controller:
    def __init__(self):
        self.rocket_csv = None
        self.rocket_dcm = None
        self.motor = None
        self.thrust = None

        self.init_spin = 0
        self.launch_altit = 0
        self.length = 0
        self.hangle = 0
        self.timesteps = 50

        self.script_dir = os.path.join(os.path.dirname(__file__), '..')

    def run(self):
        rocket = Rocket(self.rocket_csv)
        motor = load_motor(self.motor, self.thrust)
        profile = Profile(rocket, motor, self.init_spin, 
            launch_altit=self.launch_altit, 
            length=self.length, 
            hangle=self.hangle,
            timesteps=self.timesteps)

        kinem = vis.kinematics(profile, show=False)
        spin = vis.spin(profile, show=False)
        motor = vis.motor(motor, show=False)
        return motor, kinem, spin