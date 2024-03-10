import random
from resource import *
from util import *

class Actor():
	destinations = []
	tk_root = None
	canvas = None
	simspeed = 1

	def __init__(self, name, position, destination, speed, cargo_cap, graphics=None):
		self.name = name
		self.position = position
		self.destination = destination
		self.speed = speed

		self.cargo_capacity = cargo_cap
		self.cargo = []

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
		self.tk_root.after(random.randint(2000,6000) // self.simspeed, self.leave_location)
		#print(f"{self.name} arrived at {self.destination.name}")
		#self.destination.prosperity += 5


	def leave_location(self):
		print(f"{self.name}:")
		self.buy()

		#self.destination.prosperity -= 5

		self.destination = self.find_new_destination()

		#print(f"{self.name} setting out to {self.destination.name}")

		self.state = "moving"
		print()


	def buy(self):
		self.destination.prosperity += 5

		# find item with highest supply
		supply = [s.supply.amount for s in self.destination.stocks]
		stock = self.destination.stocks[supply.index(max([s.supply.amount for s in self.destination.stocks]))]
		a = self.get_free_cargo_space()
		print(f"{a} cargo free")

		#buy as much as possible
		a = self.destination.buy_resource(stock.resource, a)


		if a > 0:
			self.add_cargo(ResourceStock(stock.resource, a))

		print(f"{self.name} bought {a} {stock.resource.name} from {self.destination.name} ({self.destination.stocks})")

		#self.debug_all_cargo()


	def add_cargo(self, resource_stock):
		for stock in self.cargo:
			if resource_stock.resource == stock.resource:
				stock.change(resource_stock.amount)
				return
		self.cargo.append(ResourceStock(resource_stock.resource, resource_stock.amount))


	def get_free_cargo_space(self):
		print("Checking cargo:")
		print(self.cargo)
		n = 0
		for stock in self.cargo:
			n += stock.amount

		return self.cargo_capacity - n


	def find_new_destination(self):
		d = self.destinations.copy()
		d.remove(self.destination)
		w = self.destination_weights(d, 1, 0)
		d = random.choices(d, weights = w)
		return d[0]


	def destination_weights(self, d, w_distance, w_prosperity):
		w = [0 for x in d]
		
		n = range(len(d))

		for i in n:
			w[i] += (1 + (1000000/Vector2.distance(self.position, d[i].position)**2)**1.5) * w_distance

		for i in n:
			w[i] += (d[i].prosperity * 3) * w_prosperity

		print(w)
		return w



	def __str__(self):
		return f"{self.name}, {self.cargo_capacity}, {self.cargo}"