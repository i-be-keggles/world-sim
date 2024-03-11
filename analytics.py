import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random

class MyApp:
    def __init__(self, root):
        self.root = root
        self.value = 0
        self.x = [0]
        self.y = [0]

        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)
        self.line, = self.ax.plot(self.x, self.y, 'r-')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

        self.update()

    def update(self):
        self.value += random.randint(1, 3)
        self.x.append(self.x[-1] + 1)
        self.y.append(self.value)
        self.line.set_data(self.x, self.y)
        self.ax.set_xlim(min(self.x), max(self.x))
        self.ax.set_ylim(min(self.y), max(self.y))
        self.canvas.draw()
        self.root.after(50, self.update)

root = tk.Tk()
app = MyApp(root)
root.mainloop()