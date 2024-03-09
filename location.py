from util import *

class Location:
	canvas = None

	def __init__(self, name, position, prosperity = 50, p_graphic = None):
		self.name = name
		self.position = position
		self.prosperity = prosperity

	def __str__(self):
		return f"{self.name}"

	def __repr__(self):
		return f"{self.name}"


	def update(self):
		self.update_graphics()


	def update_graphics(self):
		n = clamp(self.prosperity, 0, 255)
		pos = self.position
		size = n/10 + 10
		x1, y1 = (pos.x - size), (pos.y - size)
		x2, y2 = (pos.x + size), (pos.y + size)
		self.canvas.coords(self.p_graphic, x1, y1, x2, y2)
		self.canvas.itemconfig(self.p_graphic, fill=rgb_to_hex(n,n,n))