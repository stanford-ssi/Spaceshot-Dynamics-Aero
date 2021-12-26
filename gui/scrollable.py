import tkinter as tk
from tkinter import ttk

class ScrollableFrame(ttk.Frame):
    BLUE = '#2f60d8'
    GREY = '#1c1c1c'

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.counter = 0

    def log(self, text):
        bg = ScrollableFrame.GREY if self.counter % 2 == 0 else ScrollableFrame.BLUE
        ttk.Label(self.scrollable_frame, text=text, background=bg, width=200).pack()
        self.counter = self.counter + 1