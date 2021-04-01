import tkinter as tk 
import tkinter.ttk as ttk

class FilePanel(ttk.Frame):
    def __init__(self, parent, profile):
        super().__init__(parent)

        self.rocket =  ttk.Label(self, text='Choose a rocket (csv)').grid(row=0, column=0)
        ttk.Button(self, text='Upload', command=self.new_rocket).grid(row=0, column=1)

        self.rocket =  ttk.Label(self, text='Choose a rocket (dcm)').grid(row=0, column=0)
        ttk.Button(self, text='Upload', command=self.new_dcm).grid(row=0, column=1)

        self.motor =  ttk.Label(self, text='Choose motor dimensions').grid(row=1, column=0)
        ttk.Button(self, text='Upload', command=self.new_motor).grid(row=1, column=1)

        self.thrust =  ttk.Label(self, text='Choose a thrust curve').grid(row=2, column=0)
        ttk.Button(self, text='Upload', command=self.new_thrust).grid(row=2, column=1)

    def new_rocket(self):
        pass

    def new_dcm(self):
        pass

    def new_motor(self):
        pass

    def new_thrust(self):
        pass