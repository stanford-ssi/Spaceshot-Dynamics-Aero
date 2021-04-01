import tkinter as tk 
import tkinter.ttk as ttk
import sys

from .input_panels import InputPanel
from .output_panel import OutputPanel
from .file_panels import FilePanel

class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title('Stabsim - Spaceshot')
        self.mainframe = ttk.Frame(self)
        self.mainframe.pack(fill=tk.BOTH, expand=1) 

        # self.call('lappend', 'auto_path', '/full/path/to/awthemes-9.3.1')
        # self.call('package', 'require', 'awdark')

        self.style = ttk.Style()
        self.style.theme_use('clam')

        ttk.Label(self.mainframe, text='Input').grid(row=0, column=0)

        self.left_panel = ttk.Notebook(self.mainframe)
        self.left_panel.grid(row=1, column=0, stick='nsew')

        self.input_pane = InputPanel(self.left_panel, 0)
        self.left_panel.add(self.input_pane, text='Simulation Params')

        self.file_pane = FilePanel(self.left_panel, 0)
        self.left_panel.add(self.file_pane, text='Upload files')

        self.left_panel.select(self.input_pane)
        self.left_panel.enable_traversal()

        ttk.Label(self.mainframe, text='Output').grid(row=0, column=1)
        self.output_pane = OutputPanel(self.mainframe, 0)

        # self.output_pane.grid(row=0, column=1, stick='nsew')
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=1)
