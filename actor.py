import random
from util import *

class Actor():
	destinations = []
	tk_root = None
	canvas = None
	simspeed = 1

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
		d = (self.destination.position - self.position).normalised() * self.speed * self.simspeed
		self.position += d
		self.canvas.move(self.graphics, d.x, d.y)

		if Vector2.distance(self.position, self.destination.position) <= 15:
			self.arrive_at_location()


	def arrive_at_location(self):
		self.state = "waiting"
		self.tk_root.after(3000 // self.simspeed, self.leave_location)
		#print(f"{self.name} arrived at {self.destination.name}")
		self.destination.prosperity += 5


	def leave_location(self):
		self.destination.prosperity -= 5

		self.destination = self.find_new_destination()

		#print(f"{self.name} setting out to {self.destination.name}")

		self.state = "moving"


	def find_new_destination(self):
		d = self.destinations.copy()
		d.remove(self.destination)
		w = self.destination_weights(d, 1, 1)
		d = random.choices(d, weights = w)
		return d[0]


	def destination_weights(self, d, w_distance, w_prosperity):
		w = [0 for x in d]
		
		n = range(len(d))

		for i in n:
			w[i] += (1/Vector2.distance(self.position, d[i].position)**2) * w_distance

		for i in n:
			w[i] += (d[i].prosperity * 3) * w_prosperity

		return w