from context import stabsim

from stabsim.motor import load_motor
from stabsim.profile import Profile
from stabsim.rocket import Rocket
import stabsim.vis as vis

import os
script_dir = os.path.join(os.path.dirname(__file__), '..')

motor_dim = "data/N5800_dim.csv"
motor_thrust = "data/N5800.txt"
rocket = "data/Hitchiker.csv"

hitchhiker_body = Rocket(os.path.join(script_dir, rocket))
N5800 = load_motor(os.path.join(script_dir, motor_dim), os.path.join(script_dir, motor_thrust))
hitchhiker = Profile(hitchhiker_body, N5800, 366, launch_altit=29000, length=5, timesteps=100)

vis.kinematics(hitchhiker)
vis.spin(hitchhiker, label_end=True)