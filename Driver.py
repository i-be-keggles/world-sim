from tkinter import *

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

root = Tk()
root.title("World Simulation")
#root.overrideredirect(1)
root.configure(bg="black")
canvas = Canvas(root, width=2000, height=1000, background='#181a1f')
canvas.pack()

def paint(event, size = 5):
    python_green = "#476042"
    x1, y1 = (event.x - size), (event.y - size)
    x2, y2 = (event.x + size), (event.y + size)
    return canvas.create_oval(x1, y1, x2, y2, fill=python_green)


circle = paint(Point(100, 200))


def tick():
    root.after(50, tick) # after 1,000 milliseconds, call tick() again
    canvas.move(circle, 1, 0)

tick()

root.mainloop()