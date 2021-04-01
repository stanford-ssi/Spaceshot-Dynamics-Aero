import tkinter as tk 
import tkinter.ttk as ttk

class InputPanel(ttk.Frame):
    def __init__(self, parent, profile):
        super().__init__(parent)

        stab_frame = ttk.LabelFrame(self, text='Stability Params')
        stab_frame.pack(fill='both', expand='yes')

        ttk.Label(stab_frame, text='Spin speed (rad/s)').grid(row=0)
        init_spin = tk.Entry(stab_frame)    
        init_spin.grid(row=0, column=1)

        ttk.Label(stab_frame, text='Hangle (deg)').grid(row=1)
        hangle = tk.Entry(stab_frame)    
        hangle.grid(row=1, column=1)

        lops_frame = ttk.LabelFrame(self, text='Launch Ops Params')
        lops_frame.pack(fill='both', expand='yes')

        ttk.Label(lops_frame, text='Launch longitude').grid(row=2)
        longitude = tk.Entry(lops_frame)    
        longitude.grid(row=2, column=1)

        ttk.Label(lops_frame, text='Launch latitude').grid(row=3)
        latitude = tk.Entry(lops_frame)    
        latitude.grid(row=3, column=1)

        ttk.Label(lops_frame, text='Launch altitude').grid(row=4)
        altitude = tk.Entry(lops_frame)    
        altitude.grid(row=4, column=1)

        sim_frame = ttk.LabelFrame(self, text='Simulation Params')
        sim_frame.pack(fill='both', expand='yes')

        ttk.Label(sim_frame, text='Simulation Length (s)').grid(row=5)
        sim_len = tk.Entry(sim_frame)    
        sim_len.grid(row=5, column=1)

        ttk.Label(sim_frame, text='Timestep Frequency (Hz)').grid(row=6)
        sim_len = tk.Entry(sim_frame)    
        sim_len.grid(row=6, column=1)

        save_btn = ttk.Button(self, text='Save', command=self.save)

    def save(self):
        pass