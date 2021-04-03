import tkinter as tk 
import tkinter.ttk as ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

class OutputPanel(ttk.Notebook):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.motor_frame = ttk.Frame(self)
        self.kinem_frame = ttk.Frame(self)
        self.stab_frame = ttk.Frame(self)

        self.add(self.motor_frame, text='Thrust Curve')
        self.add(self.kinem_frame, text='Kinematics')
        self.add(self.stab_frame, text='Stabiity Thresholds')

    def draw(self, motor, kinematics, stability):
        self.draw_frame(motor, self.motor_frame)
        self.draw_frame(kinematics, self.kinem_frame)
        self.draw_frame(stability, self.stab_frame)

    def draw_frame(self, fig, frame):
        canvas = FigureCanvasTkAgg(fig, master=frame)  
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)