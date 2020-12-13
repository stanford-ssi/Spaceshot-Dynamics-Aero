import sys
sys.path.insert(0, 'path-to-top-foler')

from McCoy_Stability_Criterion.stabsim.motor import load_motor
from McCoy_Stability_Criterion.stabsim.profile import Profile
import McCoy_Stability_Criterion.stabsim.vis as vis

H550 = load_motor('path-to-H550_dim.csv', \
    'path-to-H550_thrust.txt')
marvin = Profile('path-to-Marvin.csv', H550, 262)
vis.kinematics(marvin)
vis.spin(marvin)