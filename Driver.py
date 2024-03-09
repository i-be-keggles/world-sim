from tkinter import *
from location import *
from actor import *
from util import *
import random

simspeed = 3

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


def add_actor(actor):
    actors.append(actor)
    actor.canvas = canvas
    actor.graphics = paint(actor.position, 5, colour="#476042")



dl = [["Junderswort", 500, 400], ["Bellhaven", 800, 200], ["Thim", 1500, 800], ["Newport", 1800, 500], ["Drackensfir", 200, 100], ["March's Rest", 250, 900], ["Senn", 1100, 400], ["Marlin Cove", 600, 600], ["The Dockyards", 900, 700], ["St Kierz'", 1600, 300]]

for i in dl:
    add_location(Location(i[0], Vector2(i[1],i[2])))

for i in range(300):
    add_actor(Actor(random_name_ship(), random.choice(locations).position, random.choice(locations), random.randint(2, 5)))



def tick():
    root.after(50, tick) # after 1,000 milliseconds, call tick() again
    for actor in actors:
        actor.update()

    for location in locations:
        location.update()


tick()

root.mainloop()