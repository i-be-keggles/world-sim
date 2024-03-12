from tkinter import *
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random

from resource import Resource


class AnalyticsWindow():
    def __init__(self, locations):
        self.root = Tk()

        self.fig = plt.Figure(figsize=[20,5])

        self.graphs = []

        for i, location in enumerate(locations):
            self.graphs.append(ResourceGraph(location, [Resource("Fuel", 0), Resource("Food", 0)], self.fig, i + 1))

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

        ResourceGraph.canvas = self.canvas

        self.fig.tight_layout(pad=2, h_pad=None, w_pad=None, rect=None)

        self.root.after(50, self.root.mainloop)

        self.update()

    def update(self):
        for i in self.graphs:
            i.update()
        self.canvas.draw()

        self.root.after(500, self.update)


class ResourceGraph:
    tick_range = 300

    def __init__(self, location, resources, fig, index):
        self.location = location
        self.resources = resources

        self.fig = fig

        self.ax = self.fig.add_subplot(2, 5, index)
        
        self.ax.set_title(f"{self.location.name} supply")

        #display 0 axis
        self.ax.plot([0,self.tick_range], [0,0], color='grey', linestyle="dashed")

        self.time_axis = [x for x in range(self.tick_range)]

        self.supply_values = []
        self.supply_lines = [None for x in self.resources]

        for i, resource in enumerate(self.resources):
            self.supply_values.append([location.get_supply(resource) for x in range(self.tick_range)])
            self.supply_lines[i], = self.ax.plot(self.time_axis, self.supply_values[i], label=resource.name)

        self.ax.legend(fontsize="7")
        plt.show()

        self.update()


    def update(self):

        for i, resource in enumerate(self.resources):

            self.supply_values[i].append(self.location.get_supply(resource))
            self.supply_values[i].pop(0)

            self.supply_lines[i].set_data(self.time_axis, self.supply_values[i])

        self.ax.set_xlim(0, max(self.time_axis))
        self.ax.set_ylim(-50, 150)