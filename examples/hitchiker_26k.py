from context import stabsim

from stabsim.motor import Motor
from stabsim.profile import Profile
from stabsim.rocket import Rocket
import stabsim.vis as vis

import os
script_dir = os.path.join(os.path.dirname(__file__), '..')

motor_dim = "data/N5800_dim.csv"
motor_thrust = "data/N5800.txt"
rocket = "data/Hitchiker.csv"

hitchhiker_body = Rocket(os.path.join(script_dir, rocket))
n5800 = Motor.fromfiles(os.path.join(script_dir, motor_dim), os.path.join(script_dir, motor_thrust))
hitchhiker = Profile(hitchhiker_body, n5800, 262, launch_altit=29000, timesteps=100)

vis.rocket(hitchhiker, label_mach=True)
vis.kinematics(hitchhiker)
vis.spin(hitchhiker, label_end=True, label_mach=True)