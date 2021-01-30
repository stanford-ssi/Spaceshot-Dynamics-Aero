from context import stabsim

from stabsim.motor import load_motor
from stabsim.profile import Profile
import stabsim.vis as vis

import os
script_dir = os.path.join(os.path.dirname(__file__), '..')

motor_dim = "data/N5800_dim.csv"
motor_thrust = "data/N5800.txt"
rocket = "data/Hitchiker.csv"

H550 = load_motor(os.path.join(script_dir, motor_dim), os.path.join(script_dir, motor_thrust))
marvin = Profile(os.path.join(script_dir, rocket), H550, 262, launch_altit=26000, length=25, timesteps=100)
vis.kinematics(marvin)
vis.spin(marvin)