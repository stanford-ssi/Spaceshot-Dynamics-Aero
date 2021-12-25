import tkinter as tk 
import tkinter.ttk as ttk

from matplotlib.pyplot import text

from stabsim.vis import motor

class RocketPanel(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.parent = parent
        self.controller = controller

        airframe = ttk.LabelFrame(self, text="Airframe")
        airframe.pack(fill='both', expand='yes')

        ttk.Label(airframe, text="Mass (kg)").grid(row=0)
        self.mass = tk.StringVar()
        tk.Entry(airframe, textvariable=self.mass).grid(row=0, column=1)

        ttk.Label(airframe, text="CG").grid(row=1)
        self.cg = tk.StringVar()
        tk.Entry(airframe, textvariable=self.cg).grid(row=1, column=1)

        ttk.Label(airframe, text="Diameter (m)").grid(row=2)
        self.diameter = tk.StringVar()
        tk.Entry(airframe, textvariable=self.diameter).grid(row=2, column=1)

        ttk.Label(airframe, text="Iz (m)").grid(row=3)
        self.iz = tk.StringVar()
        tk.Entry(airframe, textvariable=self.iz).grid(row=3, column=1)

        ttk.Label(airframe, text="Ix (m)").grid(row=4)
        self.ix = tk.StringVar()
        tk.Entry(airframe, textvariable=self.ix).grid(row=4, column=1)

        ttk.Label(airframe, text="Surace Area (m^2)").grid(row=5)
        self.surf_area = tk.StringVar()
        tk.Entry(airframe, textvariable=self.surf_area).grid(row=5, column=1)

        ttk.Label(airframe, text="Nosecone Length (m)").grid(row=6)
        self.cone_len = tk.StringVar()
        tk.Entry(airframe, textvariable=self.cone_len).grid(row=6, column=1)

        ttk.Label(airframe, text="Airframe Length (m)").grid(row=7)
        self.frame_len = tk.StringVar()
        tk.Entry(airframe, textvariable=self.frame_len).grid(row=7, column=1)

        for i in range(9):
            airframe.rowconfigure(i, weight=1)

        motor_frame = ttk.LabelFrame(self, text="Motor")
        motor_frame.pack(fill='both', expand='yes')

        ttk.Label(motor_frame, text="Wet Mass (kg)").grid(row=0)
        self.wet_mass = tk.StringVar()
        tk.Entry(motor_frame, textvariable=self.wet_mass).grid(row=0, column=1)

        ttk.Label(motor_frame, text="Dry Mass (kg)").grid(row=1)
        self.dry_mass = tk.StringVar()
        tk.Entry(motor_frame, textvariable=self.dry_mass).grid(row=1, column=1)

        ttk.Label(motor_frame, text="Radius (m)").grid(row=2)
        self.radius = tk.StringVar()
        tk.Entry(motor_frame, textvariable=self.radius).grid(row=2, column=1)

        ttk.Label(motor_frame, text="Length (m)").grid(row=3)
        self.length = tk.StringVar()
        tk.Entry(motor_frame, textvariable=self.length).grid(row=3, column=1)

        for i in range(4):
            motor_frame.rowconfigure(i, weight=1)
    
    def update(self, motor, rocket):
        self.wet_mass.set(str(motor.wet_mass))
        self.dry_mass.set(str(motor.dry_mass))
        self.radius.set(str(motor.radius))
        self.length.set(str(motor.length))

        self.mass.set(str(rocket.mass))
        self.cg.set(str(rocket.cg))
        self.diameter.set(str(rocket.diameter))
        self.iz.set(str(rocket.iz))
        self.ix.set(str(rocket.ix))
        self.surf_area.set(str(rocket.surf_area))
        self.cone_len.set(str(rocket.cone_len))
        self.frame_len.set(str(rocket.frame_len))

    def set(self):
        try:
            self.controller.motor.wet_mass = float(self.wet_mass.get())
            self.controller.motor.dry_mass = float(self.dry_mass.get())
            self.controller.motor.radius = float(self.radius.get())
            self.controller.motor.length = float(self.length.get())
        except ValueError:
            self.log("Error: Invalid motor specification")
            return -1

        try:
            self.controller.rocket.mass = float(self.mass.get())
            self.controller.rocket.cg = float(self.cg.get())
            self.controller.rocket.diameter = float(self.diameter.get())
            self.controller.rocket.iz = float(self.iz.get())
            self.controller.rocket.ix = float(self.ix.get())
            self.controller.rocket.surf_area = float(self.surf_area.get())
            self.controller.rocket.cone_len = float(self.cone_len.get())
            self.controller.rocket.frame_len = float(self.frame_len.get())
        except ValueError:
            self.log("Error: Invalid airframe specifications")
            return -1

        try:
            self.controller.rocket.update_dcm()
        except ZeroDivisionError:
            self.log("Error: Invalid airframe specifications")
            return -1

    def log(self, text):
        self.parent.master.log(text)