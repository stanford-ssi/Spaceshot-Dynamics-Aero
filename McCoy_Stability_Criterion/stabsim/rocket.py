import numpy as np
import scipy 
from .utility import read_csv

class Rocket:
    def __init__(self, rocket_params, c_n_pa=2):
        self.static_params = read_csv(rocket_params)
        self.static_params["Calibers"] = self.static_params["CG"] - self.static_params["CP"]
        self.c_n_pa = c_n_pa

    def cd(self): # Drag coefficient
        return 0.3
        # The profile.drag() function originally had 0.6 as the value (unknown source)
        # Source: https://www.hindawi.com/journals/ijae/2020/6043721/ (Figure 5)

    def cm_alpha(self): # Overturning (a.k.a. pitching/rolling) moment coefficient
        return 4
        # Source: https://www.hindawi.com/journals/ijae/2020/6043721/ (Figure 6e)

    def cl_alpha(self): # Lift force coefficient
        return 2
        # Source: https://www.hindawi.com/journals/ijae/2020/6043721/ (Figure 6c)

    def cm_alpha_dot_plus_cm_q(self): # Pitch damping moment coefficient (due to rate of change of angle of attack plus tranverse angular velocity)
        return -80
        # Source: https://apps.dtic.mil/dtic/tr/fulltext/u2/a417123.pdf (Figure 4)

<<<<<<< HEAD
    def cm_p_alpha(self):
        return self.c_n_pa * self.static_params["Calibers"]
=======
    def cm_p_alpha(self): # Magnus moment coefficient
        return 1
        # Source: https://apps.dtic.mil/dtic/tr/fulltext/u2/a417123.pdf (Figure 3)
>>>>>>> c5f8fd9fcfc79d0fed80d0b8ec9d638068050ce0

    def c_spin(self): # Spin damping coefficient
        return -0.06
        # Source: James & Matt graphing