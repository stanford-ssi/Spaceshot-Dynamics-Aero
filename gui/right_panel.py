import tkinter as tk 
import tkinter.ttk as ttk

from .output_panel import GraphPanel
from .ScrollableFrame import ScrollableFrame

class RightPanel(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ttk.Label(self, text="Output").grid(row=0, column=0, stick='ns')
        self.rowconfigure(0, weight=0)

        self.graphs = GraphPanel(self, controller)
        self.graphs.grid(row=1, column=0, stick='ns')
        self.rowconfigure(1, weight=4)

        self.output_bar = ttk.Frame(self)
        self.output_bar.grid(row=2, column=0, stick='nsew')
        ttk.Label(self.output_bar, text="Apogee (km): ").grid(row=0, column=0, padx=5)
        self.apogee = ttk.Label(self.output_bar, text="NA")
        self.apogee.grid(row=0, column=1, padx=15)
        ttk.Label(self.output_bar, text="Min Speed (rad/s): ").grid(row=0, column=2, padx=5)
        self.speed = ttk.Label(self.output_bar, text="NA")
        self.speed.grid(row=0, column=3, padx=15)
        self.pb = ttk.Progressbar(self.output_bar, mode='indeterminate')
        self.pb.grid(row=0, column=4, padx=5)
        self.rowconfigure(2, weight=0)

        self.console = ScrollableFrame(self)
        self.console.grid(row=3, column=0, sticky='nsew')
        self.rowconfigure(3, weight=1)

        self.columnconfigure(0, weight=1)

    def log(self, text):
        self.console.log(text)

    def update_output(self, apogee, speed):
        self.apogee.config(text=str(apogee))
        self.speed.config(text=str(speed))