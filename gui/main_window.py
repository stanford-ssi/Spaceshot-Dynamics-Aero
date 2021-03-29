import tkinter as tk 
import tkinter.ttk as ttk
import sys

from .input_panels import InputPanel
from .output_panel import OutputPanel

class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title('Stabsim - Spaceshot')
        self.mainframe = ttk.Frame(self)

        # self.call('lappend', 'auto_path', '/full/path/to/awthemes-9.3.1')
        # self.call('package', 'require', 'awdark')

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.input_pane = InputPanel(self.mainframe)
        self.output_pane = OutputPanel(self.mainframe)

        self.input_pane.grid(row=0, column=0, rowspan = 2, sticky='nsew')
        self.output_pane.grid(row=0, column=1, stick='nsew')
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=1)
