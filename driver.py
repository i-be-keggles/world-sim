from tkinter import *
from location import *
from actor import *
from util import *
from resource import *
from analytics import *
import random

simspeed = 3
n_actors = 20
resource_multiplier = 2
resource_generation_rate = 0.02

root = Tk()
root.title("World Simulation")
root.configure(bg="black")
canvas = Canvas(root, width=2000, height=1000, background='#181a1f')
canvas.pack()


Actor.tk_root = root
Actor.canvas = canvas
Actor.simspeed = simspeed
Location.canvas = canvas
Location.resource_multiplier = resource_multiplier
ResourceGraph.resource_multiplier = resource_multiplier

Generator.generation_rate = resource_generation_rate

locations = []
actors = []


def paint(pos, size = 5, colour="white"):
    x1, y1 = (pos.x - size), (pos.y - size)
    x2, y2 = (pos.x + size), (pos.y + size)
    return canvas.create_oval(x1, y1, x2, y2, fill=colour)


def add_location(location):
    locations.append(location)
    Actor.destinations = locations
    location.p_graphic = paint(location.position, 20, "white")
    paint(location.position, 10, "#f5800a")
    
    p = location.position + Vector2(0, 18)
    canvas.create_text(p.x, p.y, text=location.name, fill="white")

    return location


def add_actor(actor):
    actors.append(actor)
    actor.canvas = canvas
    actor.graphics = paint(actor.position, 5, colour="#476042")

    return actor



dl = [
        ["Junderswort", 500, 400, [[100,100, -1],[20,50, +0.5]]], ["Bellhaven", 800, 200, [[100,60, -1],[60,80, 1]]], ["Thim", 1500, 800, [[60,40, 0.75],[40,30,-0.5]]],
        ["Newport", 1800, 500, [[10,40, 1],[60,50, -1]]], ["Drackensfir", 200, 100, [[50,60, 1],[50,20, 0.2]]], ["March's Rest", 250, 900, [[100,60, 0.1],[60,80, -1]]],
        ["Senn", 1100, 400, [[80,100, 1],[100,80, -0.5]]], ["Marlin Cove", 600, 600, [[25,30, 0.2],[80,40, 3]]], ["The Dockyards", 900, 700, [[90,120, -1],[80,50, -0.5]]],
        ["St Kierz'", 1600, 300, [[30,30, -0.5],[70,100, -2]]]]

for i in dl:
    l = add_location(Location(i[0], Vector2(i[1],i[2])))
    for j in range(len(i[3])):
        l.stocks.append(Stock(resources[j], i[3][j][0] * resource_multiplier, i[3][j][1] * resource_multiplier))
        if len(i[3][j]) > 2:
            l.generators.append(Generator(resources[j], i[3][j][2]))


for i in locations:
    print(i, end=" ")
    print(i.stocks)

for i in range(n_actors):
    l = random.choice(locations)
    add_actor(Trader(random_name_ship(), l.position, l, random.randint(2, 5), random.randint(2, 15)))

add_actor(Trader("Jimmy", locations[0].position, locations[0], 3, 10))

print()

#graph = ResourceGraph(locations[0], resources)
analytics = AnalyticsWindow(locations)

def tick():
    root.after(50, tick) # after 1,000 milliseconds, call tick() again
    for actor in actors:
        actor.update()

    for location in locations:
        location.update()


tick()

root.mainloop()
