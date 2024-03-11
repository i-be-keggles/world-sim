from tkinter import *
from location import *
from actor import *
from util import *
from resource import *
import random

simspeed = 5
n_actors = 10
resource_multiplier = 1

root = Tk()
root.title("World Simulation")
root.configure(bg="black")
canvas = Canvas(root, width=2000, height=1000, background='#181a1f')
canvas.pack()


Actor.tk_root = root
Actor.canvas = canvas
Actor.simspeed = simspeed
Location.canvas = canvas

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
        ["Junderswort", 500, 400, [[50,0],[0,0]]], ["Bellhaven", 800, 200, [[0,50],[0,0]]], ["Thim", 1500, 800, [[5,10],[5,10]]],
        ["Newport", 1800, 500, [[10,0],[0,20]]], ["Drackensfir", 200, 100, [[50,50],[0,20]]], ["March's Rest", 250, 900, [[100,0],[0,80]]],
        ["Senn", 1100, 400, [[50,30],[30,50]]], ["Marlin Cove", 600, 600, [[0,0],[80,0]]], ["The Dockyards", 900, 700, [[0,8000],[0,0]]],
        ["St Kierz'", 1600, 300, [[0,10],[30,0]]]]

for i in dl:
    l = add_location(Location(i[0], Vector2(i[1],i[2])))
    for j in range(len(i[3])):
        l.stocks.append(Stock(resources[j], i[3][j][0] * resource_multiplier, i[3][j][1] * resource_multiplier))

for i in locations:
    print(i, end=" ")
    print(i.stocks)

for i in range(n_actors):
    l = random.choice(locations)
    add_actor(Trader(random_name_ship(), l.position, l, random.randint(2, 5), random.randint(2, 15)))

add_actor(Trader("Jimmy", locations[0].position, locations[0], 3, 10))


print()

def tick():
    root.after(50, tick) # after 1,000 milliseconds, call tick() again
    for actor in actors:
        actor.update()

    for location in locations:
        location.update()


tick()

root.mainloop()
