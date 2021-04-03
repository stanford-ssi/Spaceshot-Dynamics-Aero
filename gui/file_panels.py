import tkinter.filedialog
import tkinter as tk
import tkinter.ttk as ttk

class FilePanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.rocket_csv = tk.Label(self, text='Choose a rocket (csv)')
        self.rocket_csv.grid(row=0, column=0)
        ttk.Button(self, text='Upload', command=self.new_rocket).grid(row=0, column=1)

        self.rocket_dcm = tk.Label(self, text='Choose a rocket (dcm)')
        self.rocket_dcm.grid(row=1, column=0)
        ttk.Button(self, text='Upload', command=self.new_dcm).grid(row=1, column=1)

        self.motor = tk.Label(self, text='Choose motor dimensions')
        self.motor.grid(row=2, column=0)
        ttk.Button(self, text='Upload', command=self.new_motor).grid(row=2, column=1)

        self.thrust = tk.Label(self, text='Choose a thrust curve')
        self.thrust.grid(row=3, column=0)
        ttk.Button(self, text='Upload', command=self.new_thrust).grid(row=3, column=1)

    def new_rocket(self):
        csv = tk.filedialog.askopenfilename(title='Choose a csv with rocket dims',
            filetypes = [('CSVs', '*.csv*')])
        self.rocket_csv.configure(text="Rocket CSV:" + csv)

    def new_dcm(self):
        dcm = tk.filedialog.askopenfilename(title='Choose a dcm with rocket geometry',
            filetypes = [('DCM', '*.dcm*')])
        self.rocket_dcm.configure(text="Rocket Geom:" + dcm)

    def new_motor(self):
        motor = tk.filedialog.askopenfilename(title='Choose a csv with motor dims',
            filetypes = [('CSVs', '*.csv*')])
        self.motor.configure(text="Motor Geom:" + motor)

    def new_thrust(self):
        thrust = tk.filedialog.askopenfilename(title='Choose a thrust curve',
            filetypes = [('CSVs', '*.csv*'),
                ('txt', '*.txt*')])
        self.thrust.configure(text="Thrust Curve:" + thrust)