from context import stabsim

from stabsim.motor import load_motor
from stabsim.profile import Profile
from stabsim.rocket import Rocket
import stabsim.vis as vis

import os
script_dir = os.path.join(os.path.dirname(__file__), '..')

motor_dim = "data/H550_dim.csv"
motor_thrust = "data/H550_thrust.txt"
rocket = "data/Marvin.csv"
marvin_body = Rocket(os.path.join(script_dir, rocket))

H550 = load_motor(os.path.join(script_dir, motor_dim), os.path.join(script_dir, motor_thrust))
<<<<<<< HEAD
marvin = Profile(os.path.join(script_dir, rocket), H550, 164)
=======
marvin = Profile(marvin_body, H550, 161.9821)
>>>>>>> c5f8fd9fcfc79d0fed80d0b8ec9d638068050ce0
vis.kinematics(marvin)
vis.spin(marvin, dynamic=False, gyro=False)