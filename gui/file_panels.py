import tkinter.filedialog
import tkinter as tk
import tkinter.ttk as ttk

from stabsim.rocket import Rocket
from stabsim.motor import load_motor
from stabsim.utility import read_csv

class FilePanel(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.rocket_csv = tk.Label(self, text='Choose a rocket (csv)')
        self.rocket_csv.grid(row=0, column=0)
        ttk.Button(self, text='Upload', command=self.new_rocket).grid(row=0, column=1)

        self.rocket_dcm = tk.Label(self, text='Choose a rocket (dcm)')
        self.rocket_dcm.grid(row=1, column=0)
        ttk.Button(self, text='Upload', command=self.new_dcm).grid(row=1, column=1)

        self.motor = tk.Label(self, text='Choose motor dimensions')
        self.motor.grid(row=2, column=0)
        ttk.Button(self, text='Upload', command=self.new_motor).grid(row=2, column=1)
        self.motor_file = ''

        self.thrust = tk.Label(self, text='Choose a thrust curve')
        self.thrust.grid(row=3, column=0)
        ttk.Button(self, text='Upload', command=self.new_thrust).grid(row=3, column=1)
        self.thrust_file = ''

        for i in range(4):
            self.rowconfigure(i, weight=1)

    def new_rocket(self):
        csv = tk.filedialog.askopenfilename(title='Choose a csv with rocket dims',
            filetypes = [('CSVs', '*.csv*')])
        self.rocket_csv.configure(text="Rocket CSV:" + csv)

        self.controller.rocket = Rocket(csv)

    def new_dcm(self):
        dcm = tk.filedialog.askopenfilename(title='Choose a dcm with rocket geometry',
            filetypes = [('DCM', '*.dcm*')])
        self.rocket_dcm.configure(text="Rocket Geom:" + dcm)

    def new_motor(self):
        self.motor_file = tk.filedialog.askopenfilename(title='Choose a file with the motor specs',
            filetypes = [('CSVs', '*.csv*'),
                ('Eng', '*.eng')])
        self.motor.configure(text="Motor Geom:" + self.motor_file)

        if self.motor_file[-3:] == "eng":
            self.controller.motor = load_motor(self.motor_file)
        elif self.thrust_file != '':
            self.controller.motor = load_motor(self.motor_file, self.thrust_file)
        else:
            motor_params = read_csv(self.motor_file)
            self.controller.motor.wet_mass = motor_params['wet_mass']
            self.controller.motor.dry_mass = motor_params['dry_mass']
            self.controller.motor.radius = motor_params['radius']
            self.controller.motor.length = motor_params['length']

    def new_thrust(self):
        self.thrust_file = tk.filedialog.askopenfilename(title='Choose a thrust curve',
            filetypes = [('CSVs', '*.csv*'),
                ('txt', '*.txt*')])
        self.thrust.configure(text="Thrust Curve:" + self.thrust_file)

        if self.motor_file != '' and self.motor_file[-3] != 'eng':
            self.controller.motor = load_motor(self.motor_file, self.thrust_file)