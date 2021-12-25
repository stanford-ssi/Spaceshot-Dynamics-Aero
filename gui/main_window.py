import tkinter as tk 
import tkinter.ttk as ttk

from .menu_bar import MenuBar
from .left_panel import LeftPanel
from .right_panel import RightPanel
from .profile_controller import Controller

import os
import threading
import queue

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
        self.queue = queue.Queue()

        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=3)
        self.mainframe.rowconfigure(0, weight=1)

        self.log("Welcome to Stabsim")

    def run(self):
        self.right_panel.pb.start()
        ThreadedTask(self.queue, self.controller).start()
        self.process_queue()

    def process_queue(self):
        try:
            self.queue.get_nowait()
            motor, rocket, kinem, spin = self.controller.vis()
            self.right_panel.graphs.draw(motor, rocket, kinem, spin)
            self.right_panel.update_output(self.controller.profile.apogee(), self.controller.profile.min_spin())   
            self.right_panel.pb.stop()
        except queue.Empty:
            self.after(100, self.process_queue)

    def log(self, text):
        self.right_panel.log(text)


class ThreadedTask(threading.Thread):
    def __init__(self, queue, controller):
        super().__init__()
        self.queue = queue
        self.controller = controller
    
    def run(self):
        self.controller.new_profile()
        self.queue.put("fini")
