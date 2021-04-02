import tkinter as tk 
import tkinter.ttk as ttk

from .input_panels import InputPanel
from .file_panels import FilePanel

class LeftPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        ttk.Label(self, text='Input').grid(row=0, column=0)

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, stick='nsew')

        self.input_pane = InputPanel(self.notebook, 0)
        self.notebook.add(self.input_pane, text='Simulation Params')

        self.file_pane = FilePanel(self.notebook, 0)
        self.notebook.add(self.file_pane, text='Upload files')

        self.notebook.select(self.input_pane)
        self.notebook.enable_traversal()

        self.button_bar = ttk.Frame(self)
        self.button_bar.grid(row=2, column=0, stick='nsew')
        ttk.Button(self.button_bar, text='Save Configuration', command=self.save).grid(row=0, column=1)
        ttk.Button(self.button_bar, text='Run Configuration', command=self.run).grid(row=0, column=2)

    def save(self):
        pass

    def run(self):
        pass
