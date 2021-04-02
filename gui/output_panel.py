import tkinter as tk 
import tkinter.ttk as ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

class OutputPanel(ttk.Notebook):
    def __init__(self, parent, profile):
        super().__init__(parent)

        self.motor_frame = ttk.Frame(self)
        self.kinematics_frame = ttk.Frame(self)
        self.stab_frame = ttk.Frame(self)

        fig = Figure(figsize = (5, 5), dpi = 100)
        y = [i**2 for i in range(101)]
        plot1 = fig.add_subplot(111)
        plot1.plot(y)
    
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=self.motor_frame)  
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self.motor_frame)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.add(self.motor_frame, text='Thrust Curve')
        self.add(self.kinematics_frame, text='Kinematics')
        self.add(self.stab_frame, text='Stabiity Thresholds')