import tkinter as tk 
import tkinter.ttk as ttk

class InputPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        stab_frame = ttk.LabelFrame(self, text='Stability Parameters')
        stab_frame.pack(fill='both', expand='yes')

        ttk.Label(stab_frame, text='Spin speed (rad/s)').grid(row=0)
        self.init_spin = tk.Entry(stab_frame)    
        self.init_spin.grid(row=0, column=1)
        stab_frame.rowconfigure(0, weight=1)

        ttk.Label(stab_frame, text='Hangle (deg)').grid(row=1)
        self.hangle = tk.Entry(stab_frame)    
        self.hangle.grid(row=1, column=1)
        stab_frame.rowconfigure(1, weight=1)

        lops_frame = ttk.LabelFrame(self, text='Launch Operations')
        lops_frame.pack(fill='both', expand='yes')

        ttk.Label(lops_frame, text='Launch longitude').grid(row=0)
        self.longitude = tk.Entry(lops_frame)    
        self.longitude.grid(row=0, column=1)
        lops_frame.rowconfigure(0, weight=1)

        ttk.Label(lops_frame, text='Launch latitude').grid(row=1)
        self.latitude = tk.Entry(lops_frame)    
        self.latitude.grid(row=1, column=1)
        lops_frame.rowconfigure(1, weight=1)

        ttk.Label(lops_frame, text='Launch altitude').grid(row=2)
        self.altitude = tk.Entry(lops_frame)    
        self.altitude.grid(row=2, column=1)
        lops_frame.rowconfigure(2, weight=1)

        sim_frame = ttk.LabelFrame(self, text='Simulation Parameters')
        sim_frame.pack(fill='both', expand='yes')

        ttk.Label(sim_frame, text='Simulation Length (s)').grid(row=0)
        self.sim_len = tk.Entry(sim_frame)    
        self.sim_len.grid(row=0, column=1)
        sim_frame.rowconfigure(0, weight=1)

        ttk.Label(sim_frame, text='Timestep Frequency (Hz)').grid(row=1)
        self.sim_freq = tk.Entry(sim_frame)    
        self.sim_freq.grid(row=1, column=1)
        sim_frame.rowconfigure(1, weight=1)