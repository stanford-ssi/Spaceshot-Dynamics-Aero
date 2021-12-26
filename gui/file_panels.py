import tkinter as tk
import tkinter.ttk as ttk

from stabsim.motor import Motor
from stabsim.rocket import Rocket
from stabsim.utility import read_csv

class FilePanel(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.parent = parent
        self.controller = controller

        self.rocket_csv = tk.Label(self, text="Choose a rocket (csv)")
        self.rocket_csv.grid(row=0, column=0)
        ttk.Button(self, text="Upload", command=self.new_rocket).grid(row=0, column=1)
        self.rocket_file = ''

        self.rocket_dcm = tk.Label(self, text="Choose a rocket (dcm)")
        self.rocket_dcm.grid(row=1, column=0)
        ttk.Button(self, text="Upload", command=self.new_dcm).grid(row=1, column=1)
        self.dcm_file = ''

        self.motor = tk.Label(self, text="Choose a motor")
        self.motor.grid(row=2, column=0)
        ttk.Button(self, text="Upload", command=self.new_motor).grid(row=2, column=1)
        self.motor_file = ''

        self.thrust = tk.Label(self, text="Choose a thrust curve")
        self.thrust.grid(row=3, column=0)
        ttk.Button(self, text="Upload", command=self.new_thrust).grid(row=3, column=1)
        self.thrust_file = ''

        for i in range(4):
            self.rowconfigure(i, weight=1)

    def new_rocket(self):
        self.rocket_file = tk.filedialog.askopenfilename(title="Choose a csv with rocket dims",
            filetypes = [('CSVs', '*.csv*')])
        self.rocket_csv.configure(text="Rocket CSV:" + self.rocket_file)

        if self.controller.rocket.set_spec(self.rocket_file) == -1:
            self.log("Error: Improperly formatted airframe file")
        else:
            self.log("Loaded new airframe dimensions")

    def new_dcm(self):
        self.rocket_dcm = tk.filedialog.askopenfilename(title="Choose a dcm with rocket geometry",
            filetypes = [('DCM', '*.dcm*'),
                ('txt', '*.txt')])
        self.rocket_dcm.configure(text="Rocket Geom:" + self.rocket_dcm)

        self.controller.rocket.dcm = self.rocket_dcm
        self.log("Loaded new dcm file")

    def new_motor(self):
        self.motor_file = tk.filedialog.askopenfilename(title="Choose a file with the motor specs",
            filetypes = [('Text', '*.txt'),
                ('RASP', '*.eng'),
                ('CSVs', '*.csv*')])
        self.motor.configure(text="Motor Geom:" + self.motor_file)
        
        if self.motor_file[-3:] == 'csv':
            if self.controller.motor.set_spec(self.motor_file) == Motor.ERROR:
                self.log("Error: Improperly formatted motor file")
            else:
                self.log("Loaded new motor dimensions")
        elif self.thrust_file != '':
            self.controller.motor = Motor.fromfiles(self.motor_file, self.thrust_file)
            if self.controller.motor == Motor.ERROR:
                self.log("Error: Improperly formatted motor or thrust curve file")
            else:
                self.log("Loaded new motor dimensions and thrust curve")
        else:
            self.controller.motor = Motor.fromfile(self.motor_file)
            if self.controller.motor == Motor.ERROR:
                self.log("Error: Improperly formatted motor file")
            else:
                self.log("Loaded new motor dimensions and thrust curve")  

    def new_thrust(self):
        self.thrust_file = tk.filedialog.askopenfilename(title="Choose a thrust curve",
            filetypes = [('Text', '*.txt'),
                ('RASP', '*.eng'),
                ('CSVs', '*.csv*')])
        self.thrust.configure(text="Thrust Curve:" + self.thrust_file)

        if self.motor_file == '':
            if self.controller.motor.update_thrust(self.thrust_file) == Motor.ERROR:
                self.log("Error: Improperly formatted thrust curve")
            else:
                self.log("Loaded new thrust curve")

    def log(self, text):
        self.parent.master.log(text)

    def clear(self):
        self.rocket_csv.configure(text="Choose a rocket (csv)")
        self.rocket_file = ''

        self.rocket_dcm.configure(text="Choose a rocket (dcm)")
        self.dcm_file = ''

        self.motor.configure(text="Choose a motor")
        self.motor_file = ''

        self.thrust.configure(text="Choose a thrust curve")
        self.thrust_file = ''
