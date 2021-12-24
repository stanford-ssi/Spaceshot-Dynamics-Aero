from context import stabsim

from stabsim.motor import Motor
import stabsim.vis as vis

import os
script_dir = os.path.join(os.path.dirname(__file__), '..')

motor_dim = "data/H550_dim.csv"
motor_thrust = "data/H550_thrust.txt"
rocket = "data/Marvin.csv"

h550 = Motor.fromfile(os.path.join(script_dir, motor_thrust))
vis.motor(h550)