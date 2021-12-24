import tkinter as tk 
import tkinter.ttk as ttk

from stabsim.vis import motor

class RocketPanel(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        airframe = ttk.LabelFrame(self, text="Airframe")
        airframe.pack(fill='both', expand='yes')

        ttk.Label(airframe, text="Mass (kg)").grid(row=0)
        self.mass = tk.Entry(airframe)    
        self.mass.grid(row=0, column=1)

        ttk.Label(airframe, text="CG").grid(row=1)
        self.cg = tk.Entry(airframe)    
        self.cg.grid(row=1, column=1)

        ttk.Label(airframe, text="Diameter (m)").grid(row=2)
        self.diameter = tk.Entry(airframe)    
        self.diameter.grid(row=2, column=1)

        ttk.Label(airframe, text="Iz (m)").grid(row=3)
        self.iz = tk.Entry(airframe)    
        self.iz.grid(row=3, column=1)

        ttk.Label(airframe, text="Ix (m)").grid(row=4)
        self.ix = tk.Entry(airframe)    
        self.ix.grid(row=4, column=1)

        ttk.Label(airframe, text="Surace Area (m^2)").grid(row=5)
        self.surf_area = tk.Entry(airframe)    
        self.surf_area.grid(row=5, column=1)

        ttk.Label(airframe, text="Nosecone Length (m)").grid(row=6)
        self.cone_len = tk.Entry(airframe)    
        self.cone_len.grid(row=6, column=1)

        ttk.Label(airframe, text="Airframe Length (m)").grid(row=7)
        self.frame_len = tk.Entry(airframe)    
        self.frame_len.grid(row=7, column=1)

        for i in range(9):
            airframe.rowconfigure(i, weight=1)

        motor_frame = ttk.LabelFrame(self, text="Motor")
        motor_frame.pack(fill='both', expand='yes')

        ttk.Label(motor_frame, text="Wet Mass (kg)").grid(row=0)
        self.wet_mass = tk.Entry(motor_frame)    
        self.wet_mass.grid(row=0, column=1)

        ttk.Label(motor_frame, text="Dry Mass (kg)").grid(row=1)
        self.dry_mass = tk.Entry(motor_frame)    
        self.dry_mass.grid(row=1, column=1)

        ttk.Label(motor_frame, text="Radius (m)").grid(row=2)
        self.radius = tk.Entry(motor_frame)    
        self.radius.grid(row=2, column=1)

        ttk.Label(motor_frame, text="Length (m)").grid(row=3)
        self.length = tk.Entry(motor_frame)    
        self.length.grid(row=3, column=1)

        for i in range(4):
            motor_frame.rowconfigure(i, weight=1)
    
    def update(self, motor, rocket):
        self.wet_mass.config(text=str(motor.wet_mass))
        self.dry_mass.config(text=str(motor.dry_mass))
        self.radius.config(text=str(motor.radius))
        self.length.config(text=str(motor.length))

        self.mass.config(text=str(rocket.static_params['Mass']))
        self.cg.config(text=str(rocket.static_params['CG']))
        self.diameter.config(text=str(rocket.static_params['Diameter']))
        self.iz.config(text=str(rocket.static_params['I_z']))
        self.ix.config(text=str(rocket.static_params['I_x']))
        self.surf_area.config(text=str(rocket.static_params['Surface Area']))
        self.cone_len.config(text=str(rocket.static_params['Nosecone Length']))
        self.frame_len.config(text=str(rocket.static_params['Airframe Length']))

    def set(self):
        self.controller.motor.wet_mass = float(self.rocket_pane.wet_mass.get())
        self.controller.motor.dry_mass = float(self.rocket_pane.dry_mass.get())
        self.controller.motor.radius = float(self.rocket_pane.radius.get())
        self.controller.motor.length = float(self.rocket_pane.length.get())

        self.controller.rocket.static_params['Mass'] = float(self.rocket_pane.mass.get())
        self.controller.rocket.static_params['CG'] = float(self.rocket_pane.cg.get())
        self.controller.rocket.static_params['Diameter'] = float(self.rocket_pane.diameter.get())
        self.controller.rocket.static_params['I_z'] = float(self.rocket_pane.iz.get())
        self.controller.rocket.static_params['I_x'] = float(self.rocket_pane.ix.get())
        self.controller.rocket.static_params['Surface Area'] = float(self.rocket_pane.surf_area.get())
        self.controller.rocket.static_params['Nosecone Length'] = float(self.rocket_pane.cone_len.get())
        self.controller.rocket.static_params['Airframe Length'] = float(self.rocket_pane.frame_len.get())
        self.controller.rocket.update_dcm()