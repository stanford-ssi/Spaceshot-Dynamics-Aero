import tkinter as tk 
import tkinter.ttk as ttk

class OutputBar(ttk.Frame):
    STABLE_COLOR = '#00ff00'
    UNSTABLE_COLOR = '#ff0000'

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.parent = parent
        self.controller = controller

        ttk.Label(self, text="Apogee (km): ").grid(row=0, column=0, padx=5)
        self.apogee = ttk.Label(self, text="NA")
        self.apogee.grid(row=0, column=1, padx=15)

        ttk.Label(self, text="Min Speed (rad/s): ").grid(row=0, column=2, padx=5)
        self.speed = ttk.Label(self, text="NA")
        self.speed.grid(row=0, column=3, padx=15)

        self.pb = ttk.Progressbar(self, mode='indeterminate')
        self.pb.grid(row=0, column=4, padx=15)

        self.success = ttk.Label(self, text="RUN A FLIGHT PROFILE")
        self.success.grid(row=0, column=5, padx=5)

    def log(self, text):
        self.parent.log(text)

    def update(self, apogee, speed, success):
        self.apogee.config(text=str(apogee))
        self.speed.config(text=str(speed))
        if success:
            self.success.config(text='STABLE', background=OutputBar.STABLE_COLOR)
        else:
            self.success.config(text='UNSTABLE', background=OutputBar.UNSTABLE_COLOR)
