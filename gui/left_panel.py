import tkinter as tk 
import tkinter.ttk as ttk

from .input_panels import InputPanel
from .file_panels import FilePanel

class LeftPanel(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent.mainframe)

        self.controller = controller
        self.parent = parent

        ttk.Label(self, text='Input').grid(row=0, column=0)

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, stick='nsew')

        self.input_pane = InputPanel(self.notebook)
        self.notebook.add(self.input_pane, text='Simulation Params')

        self.file_pane = FilePanel(self.notebook)
        self.notebook.add(self.file_pane, text='Upload files')

        self.notebook.select(self.input_pane)
        self.notebook.enable_traversal()

        self.button_bar = ttk.Frame(self)
        self.button_bar.grid(row=2, column=0, stick='nsew')
        ttk.Button(self.button_bar, text='Save Configuration', command=self.save).grid(row=0, column=1)
        ttk.Button(self.button_bar, text='Run Configuration', command=self.run).grid(row=0, column=2)

    def save(self):
        self.controller.rocket_csv = self.file_pane.rocket_csv.cget('text').split(':')[1]
        self.controller.rocket_dcm = self.file_pane.rocket_dcm.cget('text').split(':')[1]
        self.controller.motor = self.file_pane.motor.cget('text').split(':')[1]
        self.controller.thrust = self.file_pane.thrust.cget('text').split(':')[1]

        self.controller.init_spin = int(self.input_pane.init_spin.get())
        self.controller.launch_altit = int(self.input_pane.altitude.get())
        self.controller.length = int(self.input_pane.sim_len.get())
        self.controller.hangle = int(self.input_pane.hangle.get())

        freq = int(self.input_pane.sim_freq.get())
        length = int(self.input_pane.sim_len.get())
        self.controller.timesteps = freq * length

    def run(self):
        self.parent.run()
