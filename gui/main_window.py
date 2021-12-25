import tkinter as tk 
import tkinter.ttk as ttk

from .menu_bar import MenuBar
from .left_panel import LeftPanel
from .right_panel import RightPanel
from .profile_controller import Controller

import os

class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Stabsim - Spaceshot")
        self.mainframe = ttk.Frame(self)
        self.mainframe.pack(fill=tk.BOTH, expand=1) 
        self.attributes('-fullscreen', True)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.tk.call('source', os.path.join(dir_path, 'sun-valley.tcl'))
        self.tk.call('set_theme', 'dark')

        self.controller = Controller()

        self.menubar = MenuBar(self, self.controller)
        self.config(menu = self.menubar)

        self.left_panel = LeftPanel(self.mainframe, self.controller)
        self.left_panel.grid(row=0, column=0, sticky='nsew')

        self.right_panel = RightPanel(self.mainframe, self.controller)
        self.right_panel.grid(row=0, column=1, sticky='nsew')

        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=3)
        self.mainframe.rowconfigure(0, weight=1)

        self.log("Welcome to Stabsim")

    def run(self):
        motor, rocket, kinem, spin = self.controller.vis()
        self.right_panel.output.draw(motor, rocket, kinem, spin)
        self.right_panel.update(self.controller.profile.apogee(), self.controller.profile.min_spin())

    def log(self, text):
        self.right_panel.log(text)
