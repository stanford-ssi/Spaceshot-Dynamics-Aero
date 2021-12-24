import numpy as np
import os 
from .utility import insert_newlines, read_csv, fill_list, join
import math
from .DigitalDATCOM.datcom_lookup import lookup

class Rocket:
    def __init__(self, rocket_params, dcm=''):
        self.static_params = read_csv(rocket_params)
        self.dcm = self.create_dcm() if dcm == '' else dcm
        self.clear_coeffs
        self.memoize = {}
        self.last_val = (0,0,0,0,0)

    def create_dcm(self):
        # generate ogive equation based off given parameters
        nos_lnt = float(self.static_params['Nosecone Length'])
        rad = float(self.static_params['Diameter']) / 2
        air_lnt = float(self.static_params['Airframe Length'])
        rho = (rad**2 + nos_lnt**2) / 2 / rad
        def ogive(x):
            ans = np.sqrt(rho**2 - (nos_lnt - x)**2) + rad - rho
            return abs(round(ans, 10))
        nosecone = np.arange(0, nos_lnt, 0.02)
        airframe = np.linspace(nos_lnt, nos_lnt + air_lnt, num=3) 
        xs = np.concatenate((nosecone, airframe)).tolist()
        rs = [ogive(x) for x in nosecone] + [rad for x in airframe]
        nx = len(xs)

        # replace template based off of calculated formulas
        path = os.path.dirname(os.path.abspath(__file__))
        with open(join((path, 'DIGITALDATCOM', 'datcom_template.txt')), 'r') as f:
            template = f.read()
        replacements = {
            'INSERT_NOSELEN' : str(nos_lnt),
            'INSERT_BODYLEN' : str(air_lnt),
            'INSERT_LEN' : str(nx),
            'INSERT_X' : insert_newlines(','.join([str(x) for x in xs])),
            'INSERT_R' : insert_newlines(','.join([str(r) for r in rs]))
        }
        for key, value in replacements.items():
            template = template.replace(key, value)
        
        # generate new template file
        new_template = 'rocket_'
        ind = 0
        while os.path.exists(join((path, 'DigitalDATCOM', new_template+str(ind)))):
            ind = ind + 1
        new_template = new_template + str(ind)
        with open(join((path, 'DigitalDATCOM', new_template)), 'w') as f:
            f.write(template)
        return new_template

    def update_dcm(self):
        path = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(join(path, 'DigitalDATCOM', self.dcm)):
            self.dcm = self.create_dcm()

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
            x_cm = (self.static_params['Mass'] * self.static_params['CG'] + (mass[i] - self.static_params['Mass'])) / mass[i]
            lookup_results = lookup([vel[i] / 343], # mach nuumber TODO: is constant ok?
                [aoa],                              # angle of attack
                [altit[i]],                         # altitude
                x_cm,                               # vehicle center of mass
                mass[i],                            # vehical mass
                template=self.dcm)                            
            coeffs = list(lookup_results.values())[0]  # coefficients from DATCOM
            self.cd.append(self.last_val[0] if coeffs['CD'] == 'NDM' or math.isnan(coeffs['CD']) else coeffs['CD'] )
            self.cm.append(self.last_val[1] if coeffs['CM'] == 'NDM' or math.isnan(coeffs['CM']) else coeffs['CM'])
            self.cl.append(self.last_val[2] if coeffs['CL'] == 'NDM' or math.isnan(coeffs['CL']) else coeffs['CL'])
            self.cma_dot.append(self.last_val[3] if math.isnan(coeffs['CMAD']) else coeffs['CMAD'])
            self.cmq_dot.append(self.last_val[4] if math.isnan(coeffs['CMQ']) else coeffs['CMQ'])
        
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