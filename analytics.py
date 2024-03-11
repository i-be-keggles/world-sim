from tkinter import *
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


class ResourceGraph:
    tick_range = 300

    def __init__(self, location, resource):
        self.root = Tk()

        self.location = location
        self.resource = resource

        self.demand_values = [location.get_demand(resource) for x in range(self.tick_range)]
        self.supply_values = [location.get_supply(resource) for x in range(self.tick_range)]
        self.time_axis = [x for x in range(self.tick_range)]

        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)
        
        self.ax.set_title(f"{self.location.name} supply-demand - {self.resource.name}")

        self.demand_line, = self.ax.plot(self.time_axis, self.demand_values, color='r', label='demand')
        self.supply_line, = self.ax.plot(self.time_axis, self.supply_values, color='b', label='supply')
        plt.show()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

        self.update()
        self.root.after(50, self.root.mainloop)


    def update(self):
        self.demand_values.append(self.location.get_demand(self.resource))
        self.demand_values.pop(0)

        self.supply_values.append(self.location.get_supply(self.resource))
        self.supply_values.pop(0)

        self.demand_line.set_data(self.time_axis, self.demand_values)
        self.supply_line.set_data(self.time_axis, self.supply_values)
        self.ax.set_xlim(0, max(self.time_axis))
        self.ax.set_ylim(0, 200)
        self.canvas.draw()

        self.root.after(500, self.update)