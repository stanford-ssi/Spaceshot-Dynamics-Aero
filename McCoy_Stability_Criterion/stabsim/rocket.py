import numpy as np
import scipy 
from .utility import read_csv

class Rocket:
    def __init__(self, rocket_params):
        self.static_params = read_csv(rocket_params)

    def cd(self):
        return 0.6

    def cm_alpha(self):
        return 4

    def cl_alpha(self):
        return 2.5

    def cm_alpha_dot(self):
        return -100

    def cm_p_alpha(self):
        return 1

    def c_spin(self):
        return -1