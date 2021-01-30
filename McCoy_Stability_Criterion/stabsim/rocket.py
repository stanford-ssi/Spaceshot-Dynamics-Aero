import numpy as np
import scipy 
from .utility import read_csv

class Rocket:
    def __init__(self, rocket_params):
        self.static_params = read_csv(rocket_params)
        

    def cd(self):
        pass

    def cp(self):
        pass

    def cm_alpha(self):
        pass

    def cl_alpha(self):
        pass

    def cm_alpha_dot(self):
        pass

    def cm_p_alpha(self):
        pass

    def c_spin(self):
        pass