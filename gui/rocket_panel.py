import tkinter as tk 
import tkinter.ttk as ttk

from stabsim.vis import motor

class RocketPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        airframe = ttk.LabelFrame(self, text='Airframe')
        airframe.pack(fill='both', expand='yes')

        ttk.Label(airframe, text='Mass (kg)').grid(row=0)
        self.mass = tk.Entry(airframe)    
        self.mass.grid(row=0, column=1)

        ttk.Label(airframe, text='CG').grid(row=1)
        self.cg = tk.Entry(airframe)    
        self.cg.grid(row=1, column=1)

        ttk.Label(airframe, text='CD').grid(row=2)
        self.cd = tk.Entry(airframe)    
        self.cd.grid(row=2, column=1)

        ttk.Label(airframe, text='Diameter (m)').grid(row=3)
        self.diameter = tk.Entry(airframe)    
        self.diameter.grid(row=3, column=1)

        ttk.Label(airframe, text='Iz (m)').grid(row=4)
        self.iz = tk.Entry(airframe)    
        self.iz.grid(row=4, column=1)

        ttk.Label(airframe, text='Ix (m)').grid(row=5)
        self.ix = tk.Entry(airframe)    
        self.ix.grid(row=5, column=1)

        ttk.Label(airframe, text='Surace Area (m^2)').grid(row=6)
        self.surf_area = tk.Entry(airframe)    
        self.surf_area.grid(row=6, column=1)

        for i in range(7):
            airframe.rowconfigure(i, weight=1)

        motor_frame = ttk.LabelFrame(self, text='Motor')
        motor_frame.pack(fill='both', expand='yes')

        ttk.Label(motor_frame, text='Wet Mass (kg)').grid(row=0)
        self.wet_mass = tk.Entry(motor_frame)    
        self.wet_mass.grid(row=0, column=1)

        ttk.Label(motor_frame, text='Dry Mass (kg)').grid(row=1)
        self.dry_mass = tk.Entry(motor_frame)    
        self.dry_mass.grid(row=1, column=1)

        ttk.Label(motor_frame, text='Radius (m)').grid(row=2)
        self.radius = tk.Entry(motor_frame)    
        self.radius.grid(row=2, column=1)

        ttk.Label(motor_frame, text='Length (m)').grid(row=3)
        self.length = tk.Entry(motor_frame)    
        self.length.grid(row=3, column=1)

        for i in range(4):
            motor_frame.rowconfigure(i, weight=1)