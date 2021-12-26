import tkinter as tk 
import tkinter.ttk as ttk

from .graph_panel import GraphPanel
from .output_bar import OutputBar
from .ScrollableFrame import ScrollableFrame

class RightPanel(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ttk.Label(self, text="Output").grid(row=0, column=0, stick='ns')
        self.rowconfigure(0, weight=0)

        self.graphs = GraphPanel(self, controller)
        self.graphs.grid(row=1, column=0, stick='ns')
        self.rowconfigure(1, weight=4)

        self.output_bar = OutputBar(self, controller)
        self.output_bar.grid(row=2, column=0, stick='nsew')
        self.rowconfigure(2, weight=0)

        self.console = ScrollableFrame(self)
        self.console.grid(row=3, column=0, sticky='nsew')
        self.rowconfigure(3, weight=1)

        self.columnconfigure(0, weight=1)

    def log(self, text):
        self.console.log(text)