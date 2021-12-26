import tkinter as tk 
import tkinter.ttk as ttk

class SimulationPanel(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.parent = parent
        self.controller = controller

        stab_frame = ttk.LabelFrame(self, text="Stability Parameters")
        stab_frame.pack(fill='both', expand='yes')

        ttk.Label(stab_frame, text="Spin speed (rad/s)").grid(row=0)
        self.init_spin = tk.StringVar()
        tk.Entry(stab_frame, textvariable=self.init_spin).grid(row=0, column=1)
        stab_frame.rowconfigure(0, weight=1)

        ttk.Label(stab_frame, text="Hangle (deg)").grid(row=1)
        self.hangle = tk.StringVar()
        tk.Entry(stab_frame, textvariable=self.hangle).grid(row=1, column=1)
        stab_frame.rowconfigure(1, weight=1)

        lops_frame = ttk.LabelFrame(self, text="Launch Operations")
        lops_frame.pack(fill='both', expand='yes')

        ttk.Label(lops_frame, text="Launch longitude").grid(row=0)
        self.longitude = tk.StringVar()
        tk.Entry(lops_frame, textvariable=self.longitude).grid(row=0, column=1)
        lops_frame.rowconfigure(0, weight=1)

        ttk.Label(lops_frame, text="Launch latitude").grid(row=1)
        self.latitude = tk.StringVar()
        tk.Entry(lops_frame, textvariable=self.latitude).grid(row=1, column=1)
        lops_frame.rowconfigure(1, weight=1)

        ttk.Label(lops_frame, text="Launch altitude").grid(row=2)
        self.altitude = tk.StringVar()
        tk.Entry(lops_frame, textvariable=self.altitude).grid(row=2, column=1)
        lops_frame.rowconfigure(2, weight=1)

        sim_frame = ttk.LabelFrame(self, text="Simulation Parameters")
        sim_frame.pack(fill='both', expand='yes')

        ttk.Label(sim_frame, text="Simulation Length (s)").grid(row=0)
        self.sim_len = tk.StringVar()
        tk.Entry(sim_frame, textvariable=self.sim_len).grid(row=0, column=1)
        sim_frame.rowconfigure(0, weight=1)

        ttk.Label(sim_frame, text="Timestep Frequency (Hz)").grid(row=1)
        self.sim_freq = tk.StringVar()
        tk.Entry(sim_frame, textvariable=self.sim_freq).grid(row=1, column=1)
        sim_frame.rowconfigure(1, weight=1)

    def set(self):
        try:
            self.controller.init_spin = float(self.init_spin.get())
            self.controller.launch_altit = float(self.altitude.get())
            self.controller.length = float(self.sim_len.get())
            self.controller.hangle = float(self.hangle.get())

            freq = float(self.sim_freq.get())
            length = float(self.sim_len.get())
            self.controller.timesteps = int(freq * length)
        except ValueError:
            self.log("Error: Improper simulation parameters")
            return -1

    def update(self):
        self.init_spin.set(str(self.controller.init_spin))
        self.hangle.set(str(self.controller.hangle))
        self.altitude.set(str(self.controller.launch_altit))
        self.sim_len.set(str(self.controller.length))
        if self.controller.length != 0:
            self.sim_freq.set(str(self.controller.timesteps / self.controller.length))
        else:
            self.sim_freq.set('0')

    def log(self, text):
        self.parent.master.log(text)