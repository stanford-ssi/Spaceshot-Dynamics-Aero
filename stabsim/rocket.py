import numpy as np
import scipy 
from .utility import read_csv, fill_list
import math
from .DigitalDATCOM.datcom_lookup import lookup

class Rocket:
    def __init__(self, rocket_params):
        self.static_params = read_csv(rocket_params)
        self.clear_coeffs
        self.memoize = {}
        self.last_val = (0,0,0,0,0)

    def clear_coeffs(self):
        self.cd = []
        self.cm = []
        self.cl = []
        self.cma_dot = []
        self.cmq_dot = []

    def fill_coeffs(self):
        fill_list(self.cd)
        fill_list(self.cm)
        fill_list(self.cl)
        fill_list(self.cma_dot)
        fill_list(self.cmq_dot)

    def update_coeffs(self, vel, aoa, altit, mass, single=True):
        self.clear_coeffs()

        key = (round(vel[0]), round(altit[0])) # Memoization so we can use this during odeint
        if single and key in self.memoize.keys():
            cd, cm, cl, cma, cmq = self.memoize[key]
            self.cd = [cd]
            self.cm = [cm]
            self.cl = [cl]
            self.cma_dot = [cma]
            self.cmq_dot = [cmq]
            return

        for i in range(len(vel)):
            x_cm = (self.static_params["Mass"] * self.static_params["CG"] + (mass[i] - self.static_params["Mass"])) / mass[i]
            lookup_results = lookup([vel[i] / 343], # mach nuumber TODO: is constant ok
                [aoa],                              # angle of attack
                [altit[i]],                         # altitude
                x_cm,                               # vehicle center of mass
                mass[i])                            # vehical mass
            coeffs = list(lookup_results.values())[0]  # coefficients from DATCOM
            self.cd.append(self.last_val[0] if coeffs['CD'] == 'NDM' or math.isnan(coeffs['CD']) else coeffs['CD'] )
            self.cm.append(self.last_val[1] if coeffs['CM'] == 'NDM' or math.isnan(coeffs['CM']) else coeffs['CM'])
            self.cl.append(self.last_val[2] if coeffs['CL'] == 'NDM' or math.isnan(coeffs['CL']) else coeffs['CL'])
            self.cma_dot.append(self.last_val[3] if math.isnan(coeffs['CMA']) else coeffs['CMA'])
            self.cmq_dot.append(self.last_val[4] if math.isnan(coeffs['CNB']) else coeffs['CNB'])
        
        self.fill_coeffs()

        if single:
            self.last_val = (self.cd[0], self.cm[0], self.cl[0], self.cma_dot[0], self.cmq_dot[0])
            self.memoize[key] = self.last_val

    def get_cd(self, datcom=True): # Drag coefficient
        return np.array(self.cd) if datcom else 0.3
        # Source: https://www.hindawi.com/journals/ijae/2020/6043721/ (Figure 5)

    def get_cm_alpha(self, datcom=True): # Overturning (a.k.a. pitching/rolling) moment coefficient
        return np.array(self.cm) if datcom else 4
        # Source: https://www.hindawi.com/journals/ijae/2020/6043721/ (Figure 6e)

    def get_cl_alpha(self, datcom=True): # Lift force coefficient
        return np.array(self.cl) if datcom else 2
        # Source: https://www.hindawi.com/journals/ijae/2020/6043721/ (Figure 6c)

    def get_cm_dot(self, datcom=True): # Pitch damping moment coefficient (due to rate of change of angle of attack plus tranverse angular velocity)
        return np.array(self.cma_dot) + np.array(self.cmq_dot) if datcom else -80
        # Source: https://apps.dtic.mil/dtic/tr/fulltext/u2/a417123.pdf (Figure 4)

    def get_cm_p_alpha(self): # Magnus moment coefficient
        #TODO: there is a way to get magnus stuff out datcom, look into SPIN control card
        return 1
        # Source: https://apps.dtic.mil/dtic/tr/fulltext/u2/a417123.pdf (Figure 3)

    def get_c_spin(self): # Spin damping coefficient
        return -0.06
        # Source: James & Matt graphing