import tkinter as tk 
import tkinter.ttk as ttk

from .input_panels import InputPanel
from .file_panels import FilePanel
from .rocket_panel import RocketPanel

class LeftPanel(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.parent = parent

        ttk.Label(self, text='Input').grid(row=0, column=0, sticky='ns')
        self.rowconfigure(0, weight=0)
        self.columnconfigure(0, weight=1)

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, stick='nsew')
        self.rowconfigure(1, weight=1)

        self.input_pane = InputPanel(self.notebook)
        self.notebook.add(self.input_pane, text='Simulation Parameters')

        self.rocket_pane = RocketPanel(self.notebook)
        self.notebook.add(self.rocket_pane, text='Rocket Parameters')

        self.file_pane = FilePanel(self.notebook, self.controller)
        self.notebook.add(self.file_pane, text='Upload files')

        self.notebook.select(self.input_pane)
        self.notebook.enable_traversal()

        self.button_bar = ttk.Frame(self)
        self.button_bar.grid(row=2, column=0, stick='nsew')
        ttk.Button(self.button_bar, text='Save Configuration', style='Accent.TButton', command=self.save).grid(row=0, column=1)
        ttk.Button(self.button_bar, text='Run Configuration', style='Accent.TButton', command=self.run).grid(row=0, column=2)
        self.rowconfigure(2, weight=1)

    def save(self):
        self.rocket_pane.wet_mass.config(text=self.controller.motor.wet_mass)
        self.rocket_pane.dry_mass.config(text=self.controller.motor.dry_mass)
        self.rocket_pane.radius.config(text=self.controller.motor.radius)
        self.rocket_pane.length.config(text=self.controller.motor.length)

        self.rocket_pane.mass.config(text=self.controller.rocket.static_params["Mass"])
        self.rocket_pane.cg.config(text=self.controller.rocket.static_params["CG"])
        self.rocket_pane.cd.config(text=self.controller.rocket.static_params["CD"])
        self.rocket_pane.diameter.config(text=self.controller.rocket.static_params["Diameter"])
        self.rocket_pane.iz.config(text=self.controller.rocket.static_params["I_z"])
        self.rocket_pane.ix.config(text=self.controller.rocket.static_params["I_x"])
        self.rocket_pane.surf_area.config(text=self.controller.rocket.static_params["Surface Area"])

        self.controller.init_spin = int(self.input_pane.init_spin.get())
        self.controller.launch_altit = int(self.input_pane.altitude.get())
        self.controller.length = int(self.input_pane.sim_len.get())
        self.controller.hangle = int(self.input_pane.hangle.get())

        freq = int(self.input_pane.sim_freq.get())
        length = int(self.input_pane.sim_len.get())
        self.controller.timesteps = freq * length

    def run(self):
        self.parent.run()
