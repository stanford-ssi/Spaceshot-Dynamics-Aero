import numpy as np
import os 
from .utility import insert_newlines, read_csv, fill_list, join
import math
from .DigitalDATCOM.datcom_lookup import lookup

class Rocket:
    def __init__(self, mass, cg, diameter, iz, ix, surf_area, cone_len, frame_len, dcm=None):
        self.mass = mass
        self.cg = cg
        self.diameter = diameter
        self.iz = iz
        self.ix = ix
        self.surf_area = surf_area
        self.cone_len = cone_len
        self.frame_len = frame_len

        self.dcm = dcm if dcm != None else self.create_dcm()
        
        self.clear_coeffs()
        self.memoize = {}
        self.last_val = (0,0,0,0,0)

    @classmethod
    def empty(cls):
        return Rocket(0, 0, 0, 0, 0, 0, 0, 0, dcm='')

    @classmethod
    def fromfile(cls, rocket_params, dcm=None):
        rocket = Rocket.empty()
        rocket.set_spec(rocket_params)
        rocket.dcm = dcm
        rocket.update_dcm()
        return rocket

    def set_spec(self, file):
        dict = read_csv(file)
        try: 
            self.mass = float(dict['Mass']) if 'Mass' in dict else 0
            self.cg = float(dict['CG']) if 'CG' in dict else 0
            self.diameter = float(dict['Diameter']) if 'Diameter' in dict else 0
            self.iz = float(dict['I_z']) if 'I_z' in dict else 0
            self.ix = float(dict['I_x']) if 'I_x' in dict else 0
            self.surf_area = float(dict['Surface Area']) if 'Surface Area' in dict else 0
            self.cone_len = float(dict['Nosecone Length']) if 'Nosecone Length' in dict else 0
            self.frame_len = float(dict['Airframe Length']) if 'Airframe Length' in dict else 0
        except ValueError:
            return -1

    def create_dcm(self):
        # generate ogive equation based off given parameters
        rad = self.diameter / 2
        rho = (rad**2 + self.cone_len**2) / 2 / rad
        def ogive(x):
            ans = np.sqrt(rho**2 - (self.cone_len - x)**2) + rad - rho
            return abs(round(ans, 10))
        nosecone = np.arange(0, self.cone_len, 0.02)
        airframe = np.linspace(self.cone_len, self.cone_len + self.frame_len, num=3) 
        xs = np.concatenate((nosecone, airframe)).tolist()
        rs = [ogive(x) for x in nosecone] + [rad for x in airframe]
        nx = len(xs)

        # replace template based off of calculated formulas
        path = os.path.dirname(os.path.abspath(__file__))
        with open(join((path, 'DIGITALDATCOM', 'datcom_template.txt')), 'r') as f:
            template = f.read()
        replacements = {
            'INSERT_NOSELEN' : str(self.cone_len),
            'INSERT_BODYLEN' : str(self.frame_len),
            'INSERT_ZCG' : str(rad),
            'INSERT_LEN' : str(nx),
            'INSERT_XS' : insert_newlines(','.join([str(x) for x in xs])),
            'INSERT_RS' : insert_newlines(','.join([str(r) for r in rs]))
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
        if not self.dcm or not os.path.exists(join((path, 'DigitalDATCOM', str(self.dcm)))):
            self.dcm = self.create_dcm()

    def clear_coeffs(self):
        self.cd = []
        self.cm = []
        self.cl = []
        self.cma_dot = []
        self.cmq_dot = []

    def update_coeffs(self, machs, aoa, altits, masses, cgs, mach_scale=10, altit_scale=0.01, mass_scale=10):
        self.clear_coeffs()

        for mach, altit, mass, cg in zip(machs, altits, masses, cgs):
            key = (round(mach*mach_scale), round(altit*altit_scale), round(mass*mass_scale))
            if key in self.memoize:
                cd, cm, cl, cma, cmq = self.memoize[key]
                self.cd.append(cd)
                self.cm.append(cm)
                self.cl.append(cl)
                self.cma_dot.append(cma)
                self.cmq_dot.append(cmq)
                continue

            lookup_results = lookup([mach], # mach number 
                [aoa],                      # angle of attack
                [altit],                    # altitude
                cg,                         # vehicle center of mass
                mass,                       # vehical mass
                template=self.dcm)

            coeffs = list(lookup_results.values())[0]  # coefficients from DATCOM
            self.cd.append(self.last_val[0] if coeffs['CD'] == 'NDM' or math.isnan(coeffs['CD']) else coeffs['CD'] )
            self.cm.append(self.last_val[1] if coeffs['CM'] == 'NDM' or math.isnan(coeffs['CM']) else coeffs['CM'])
            self.cl.append(self.last_val[2] if coeffs['CL'] == 'NDM' or math.isnan(coeffs['CL']) else coeffs['CL'])
            self.cma_dot.append(self.last_val[3] if math.isnan(coeffs['CMAD']) else coeffs['CMAD'])
            self.cmq_dot.append(self.last_val[4] if math.isnan(coeffs['CMQ']) else coeffs['CMQ'])

            self.last_val = (self.cd[-1], self.cm[-1], self.cl[-1], self.cma_dot[-1], self.cmq_dot[-1])
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