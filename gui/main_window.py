import tkinter as tk 
import tkinter.ttk as ttk
import sys

from .menu_bar import MenuBar
from .left_panel import LeftPanel
from .right_panel import RightPanel
from .profile_controller import Controller

class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title('Stabsim - Spaceshot')
        self.mainframe = ttk.Frame(self)
        self.mainframe.pack(fill=tk.BOTH, expand=1) 

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.controller = Controller()

        self.menubar = MenuBar(self, self.controller)
        self.config(menu = self.menubar)

        self.left_panel = LeftPanel(self, self.controller)
        self.left_panel.grid(row=0, column=0, sticky='nsew')

        self.right_panel = RightPanel(self.mainframe, self.controller)
        self.right_panel.grid(row=0, column=1, sticky='nsew')

        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=1)

    def run(self):
        motor, kinem, spin = self.controller.run()
        self.right_panel.output.draw(motor, kinem, spin)
