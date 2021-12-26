import tkinter as tk 
import tkinter.ttk as ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from .scrollable import ScrollableFrame

class GraphPanel(ttk.Notebook):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.motor_frame = ScrollableFrame(self)
        self.rocket_frame = ScrollableFrame(self)
        self.kinem_frame = ScrollableFrame(self)
        self.stab_frame = ScrollableFrame(self)

        self.add(self.motor_frame, text="Motor")
        self.add(self.rocket_frame, text="Aerodynamic Coefficients")
        self.add(self.kinem_frame, text="Kinematics")
        self.add(self.stab_frame, text="Stabiity Thresholds")

    def draw(self, motor, rocket, kinematics, stability):
        GraphPanel.draw_frame(motor, self.motor_frame.scrollable_frame)
        GraphPanel.draw_frame(rocket, self.rocket_frame.scrollable_frame)
        GraphPanel.draw_frame(kinematics, self.kinem_frame.scrollable_frame)
        GraphPanel.draw_frame(stability, self.stab_frame.scrollable_frame)

    def clear(self):
        GraphPanel.clear_frame(self.motor_frame.scrollable_frame)
        GraphPanel.clear_frame(self.rocket_frame.scrollable_frame)
        GraphPanel.clear_frame(self.kinem_frame.scrollable_frame)
        GraphPanel.clear_frame(self.stab_frame.scrollable_frame)

    @classmethod
    def draw_frame(cls, fig, frame):
        canvas = FigureCanvasTkAgg(fig, master=frame)  
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    @classmethod
    def clear_frame(cls, frame):
        for widget in frame.winfo_children():
            widget.destroy()