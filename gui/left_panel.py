import tkinter as tk 
import tkinter.ttk as ttk

from .sim_panel import SimulationPanel
from .file_panels import FilePanel
from .rocket_panel import RocketPanel

class LeftPanel(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.parent = parent

        ttk.Label(self, text="Input").grid(row=0, column=0, sticky='ns')
        self.rowconfigure(0, weight=0)
        self.columnconfigure(0, weight=1)

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, stick='nsew')
        self.rowconfigure(1, weight=1)

        self.input_pane = SimulationPanel(self.notebook, self.controller)
        self.notebook.add(self.input_pane, text="Simulation Parameters")

        self.rocket_pane = RocketPanel(self.notebook, self.controller)
        self.notebook.add(self.rocket_pane, text="Rocket Parameters")

        self.file_pane = FilePanel(self.notebook, self.controller)
        self.notebook.add(self.file_pane, text="Upload files")

        self.notebook.select(self.input_pane)
        self.notebook.enable_traversal()

        self.button_bar = ttk.Frame(self)
        self.button_bar.grid(row=2, column=0, stick='nsew')
        self.ub = ttk.Button(self.button_bar, text="Upload Files", style='Accent.TButton', command=self.save)
        self.ub.grid(row=0, column=0, padx=5)
        self.cb = ttk.Button(self.button_bar, text="Clear Data", style='Accent.TButton', command=self.clear)
        self.cb.grid(row=0, column=1, padx=5)
        self.rb = ttk.Button(self.button_bar, text="Run Configuration", style='Accent.TButton', command=self.run)
        self.rb.grid(row=0, column=2, padx=5)
        self.rowconfigure(2, weight=1)

    def save(self):
        self.ub.config(state=tk.DISABLED)
        self.input_pane.update()
        self.rocket_pane.update(self.controller.motor, self.controller.rocket)
        self.log("Updated specs using uploaded files")
        self.ub.config(state=tk.NORMAL)

    def run(self):
        self.rb.config(state=tk.DISABLED)
        self.log("Running new flight profile")
        if (self.input_pane.set() == -1 or self.rocket_pane.set() == -1):
            self.log("Aborted running flight profile")
        else:
            self.parent.master.run()
            self.file_pane.clear()

    def clear(self):
        self.cb.config(state=tk.DISABLED)
        self.controller.clear()
        self.input_pane.update()
        self.rocket_pane.update(self.controller.motor, self.controller.rocket)
        self.file_pane.clear()
        self.log("Cleared flight data")
        self.cb.config(state=tk.NORMAL)

    def log(self, text):
        self.parent.master.log(text)