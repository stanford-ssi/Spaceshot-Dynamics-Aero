import tkinter.filedialog
import tkinter as tk
import tkinter.ttk as ttk

class FilePanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.rocket_csv =  ttk.Label(self, text='Choose a rocket (csv)').grid(row=0, column=0)
        ttk.Button(self, text='Upload', command=self.new_rocket).grid(row=0, column=1)

        self.rocket_dcm =  ttk.Label(self, text='Choose a rocket (dcm)').grid(row=1, column=0)
        ttk.Button(self, text='Upload', command=self.new_dcm).grid(row=1, column=1)

        self.motor =  ttk.Label(self, text='Choose motor dimensions').grid(row=2, column=0)
        ttk.Button(self, text='Upload', command=self.new_motor).grid(row=2, column=1)

        self.thrust =  ttk.Label(self, text='Choose a thrust curve').grid(row=3, column=0)
        ttk.Button(self, text='Upload', command=self.new_thrust).grid(row=3, column=1)

    def new_rocket(self):
        csv = tk.filedialog.askopenfilename(title='Choose a csv with rocket dims',
            filetypes = [('CSVs', '*.csv*')])
        self.rocket_csv.configure("Rocket CSV:" + csv)

    def new_dcm(self):
        dcm = tk.filedialog.askopenfilename(title='Choose a dcm with rocket geometry',
            filetypes = [('DCM', '*.dcm*')])
        self.rocket_dcm.configure("Rocket Geom:" + dcm)

    def new_motor(self):
        motor = tk.filedialog.askopenfilename(title='Choose a csv with motor dims',
            filetypes = [('CSVs', '*.csv*')])
        self.motor.configure("Motor Geom:" + motor)

    def new_thrust(self):
        thrust = tk.filedialog.askopenfilename(title='Choose a thrust curve',
            filetypes = [('CSVs', '*.csv*'),
                ('txt', '*.txt*')])
        self.thrust.configure("Thrust Curve:" + thrust)