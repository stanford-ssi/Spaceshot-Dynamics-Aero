import numpy as np
import scipy 
from .utility import read_csv
import math
from .DigitalDATCOM.datcom_lookup import lookup

class Rocket:
    def __init__(self, rocket_params):
        self.static_params = read_csv(rocket_params)
        
        self.cd = 0.3
        self.cm_alpha = 4
        self.cl_alpha = 2
        self.cm_p_alpha = 1
        self.c_spin = -0.06 # experimentally determined

    def update_coeffs(self, vel, aoa, altit, mass):
        self.cd = []
        self.cm_alpha = []
        self.cl_alpha = []

        for i in range(len(vel)):
            x_cm = (self.static_params["Mass"] * self.static_params["CG"] + (mass[i] - self.static_params["Mass"])) / mass[i]
            lookup_results = lookup([vel[i] / 343], # mach nuumber TODO: is constant ok?
                [aoa],                              # angle of attack
                [altit[i]],                         # altitude
                x_cm,                               # vehicle center of mass
                mass[i])                            # vehical mass
            coeffs = list(lookup_results.values())[0]  # coefficients from DATCOM
            self.cd.append(0.3 if coeffs['CD'] == 'NDM' or math.isnan(coeffs['CD']) else coeffs['CD'] )
            #TODO: how were these defaults chosen?
            self.cm_alpha.append(0.2613 if coeffs['CMA'] == 0 or math.isnan(coeffs['CMA']) else coeffs['CMA'])
            self.cl_alpha.append(0.03092 if coeffs['CLA'] == 0 or math.isnan(coeffs['CLA']) else coeffs['CLA'])
            #TODO: how to get rest of coeffs out datcom

    def get_cd(self, datcom=True): # Drag coefficient
        if datcom:
            return np.array(self.cd)
        else:
            return 0.3
        # The profile.drag() function originally had 0.6 as the value (unknown source)
        # Source: https://www.hindawi.com/journals/ijae/2020/6043721/ (Figure 5)

    def get_cm_alpha(self, datcom=True): # Overturning (a.k.a. pitching/rolling) moment coefficient
        if datcom:
            return np.array(self.cm_alpha)
        else:
            return 4
        # Source: https://www.hindawi.com/journals/ijae/2020/6043721/ (Figure 6e)

    def get_cl_alpha(self, datcom=True): # Lift force coefficient
        if datcom:
            return np.array(self.cl_alpha) 
        else:
            return 2
        # Source: https://www.hindawi.com/journals/ijae/2020/6043721/ (Figure 6c)

    def get_cm_alpha_dot_plus_cm_q(self): # Pitch damping moment coefficient (due to rate of change of angle of attack plus tranverse angular velocity)
        return -80
        # Source: https://apps.dtic.mil/dtic/tr/fulltext/u2/a417123.pdf (Figure 4)

    def get_cm_p_alpha(self): # Magnus moment coefficient
        return 1
        # Source: https://apps.dtic.mil/dtic/tr/fulltext/u2/a417123.pdf (Figure 3)

    def get_c_spin(self): # Spin damping coefficient
        return -0.06
        # Source: James & Matt graphing