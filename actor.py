import random
from util import *

class Actor():
	destinations = []
	tk_root = None
	canvas = None

	def __init__(self, name, position, destination, speed, graphics=None):
		self.name = name
		self.position = position
		self.destination = destination
		self.speed = speed

		self.graphics = graphics

		self.state = "moving"


	def update(self):
		if self.state == "moving":
			self.move()


	def move(self):
		d = (self.destination.position - self.position).normalised() * self.speed
		self.position += d
		self.canvas.move(self.graphics, d.x, d.y)

		if Vector2.distance(self.position, self.destination.position) <= 10:
			self.state = "waiting"
			self.tk_root.after(6000, self.find_new_destination)
			print(f"{self.name} arrived at {self.destination.name}")


	def find_new_destination(self):
		d = self.destination
		while d == self.destination:
			d = random.choice(self.destinations)

		self.destination = d

		self.state = "moving"
		print(f"{self.name} setting out to {self.destination.name}")