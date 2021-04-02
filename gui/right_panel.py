import tkinter as tk 
import tkinter.ttk as ttk

from .output_panel import OutputPanel

class RightPanel(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ttk.Label(self, text='Output').grid(row=0, column=0)

        self.output = OutputPanel(self, controller)
        self.output.grid(row=1, column=0, stick='nsew')

        self.output_bar = ttk.Frame(self)
        self.output_bar.grid(row=2, column=0, stick='nsew')
        ttk.Label(self.output_bar, text='Apogee (km): ').grid(row=0, column=1)
        ttk.Label(self.output_bar, text='Min Speed (rad/s): ').grid(row=0, column=2)
