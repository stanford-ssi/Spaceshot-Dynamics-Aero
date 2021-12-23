import tkinter as tk

class MenuBar(tk.Menu):
    def __init__(self, parent, controller):
        super().__init__(parent)

        filemenu = tk.Menu(self, tearoff=0)
        filemenu.add_command(label="Save...", command = self.save_controller)
        filemenu.add_command(label="Save as...", command = self.save_new_controller)
        filemenu.add_command(label="Open", command = self.load_controller)
        self.add_cascade(label='File', menu=filemenu)

        helpmenu = tk.Menu(self, tearoff=0)
        helpmenu.add_command(label="Help", command = self.open_readme)
        helpmenu.add_command(label="Acknoledgment", command = self.open_ack)
        self.add_cascade(label='Help', menu=helpmenu)

        self.last_controller = None

    def save_controller(self):
        pass

    def save_new_controller(self):
        pass

    def load_controller(self):
        pass

    def open_readme(self):
        pass

    def open_ack(self):
        pass