from context import stabsim

from stabsim.motor import Motor
from stabsim.profile import Profile
from stabsim.rocket import Rocket
import stabsim.vis as vis

import os
script_dir = os.path.join(os.path.dirname(__file__), '..')

motor_dim = "data/H550_dim.csv"
motor_thrust = "data/H550_thrust.txt"
rocket = "data/Marvin.csv"

marvin = Rocket.fromfile(os.path.join(script_dir, rocket))
h550 = Motor.fromfiles(os.path.join(script_dir, motor_dim), os.path.join(script_dir, motor_thrust))
baby_spacehot = Profile(marvin, h550, 262, launch_altit=26000, length=5, timesteps=100)

vis.kinematics(baby_spacehot)
vis.spin(baby_spacehot)