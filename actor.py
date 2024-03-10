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
		self.sell()


	def leave_location(self):
		#self.destination.prosperity -= 5

		dest = self.find_new_destination()
		self.buy(next_destination=dest)
		self.destination = dest

		#print(f"{self.name} setting out to {self.destination.name}")

		self.state = "moving"
		print()


	def buy(self, next_destination):
		self.destination.prosperity += 5

		# find item with highest supply
		supply = [s.supply.amount for s in self.destination.stocks]
		#stock = self.destination.stocks[supply.index(max([s.supply.amount for s in self.destination.stocks]))]
		resource = self.find_best_buy(self.destination, next_destination)
		if resource is None:
			print(f"No good buy.")
			return

		a = self.get_free_cargo_space()
		#buy as much as possible
		a = self.destination.give_resource(resource, a)


		if a > 0:
			self.add_cargo(ResourceStock(resource, a))

		print(f"{self.name} bought {a} {resource.name} from {self.destination.name} ({self.destination.stocks})")

		#self.debug_all_cargo()


	def sell(self):
		if len(self.cargo) == 0:
			return

		self.destination.prosperity -= 5
		
		ps = ""

		for stock in self.cargo:
			self.destination.get_resource(stock.resource, stock.amount)
			self.cargo.remove(stock)

			ps += f"{stock.amount} {stock.resource.name} "


		print(f"{self.name} sold {ps}to {self.destination.name} ({self.destination.stocks})")



	def add_cargo(self, resource_stock):
		for stock in self.cargo:
			if resource_stock.resource == stock.resource:
				stock.change(resource_stock.amount)
				return
		self.cargo.append(ResourceStock(resource_stock.resource, resource_stock.amount))


	def get_free_cargo_space(self):
		n = 0
		for stock in self.cargo:
			n += stock.amount

		return self.cargo_capacity - n


	def find_new_destination(self):
		d = self.destinations.copy()
		d.remove(self.destination)
		w, d = self.destination_weights(d, 1, 0)
		d = random.choices(d, weights = w)
		return d[0]


	def destination_weights(self, d, w_distance, w_prosperity):
		w = [0 for x in d]
		
		n = range(len(d))

		for i in n:
			w[i] += (1 + (1000000/Vector2.distance(self.position, d[i].position)**2)**1.5) * w_distance

		for i in n:
			w[i] += (d[i].prosperity * 3) * w_prosperity

		return w, d


	def find_best_buy(self, cur_destination, next_destination):
		p_buy = []
		weights = []
		for stock in cur_destination.stocks:
			if stock.supply.amount > stock.demand.amount:
				p_buy.append(stock.resource)
				weights.append(next_destination.get_demand(stock.resource))

		if len(p_buy) == 0 or max(weights) == 0:
			return None
		else:
			return random.choices(p_buy, weights)[0]


	def __str__(self):
		return f"{self.name}, {self.cargo_capacity}, {self.cargo}"



class Trader(Actor):
	def destination_weights(self, d, w_distance, w_prosperity):

		#possible things to buy
		p_supply = []

		for stock in self.destination.stocks:
			if stock.supply.amount > stock.demand.amount:
				p_supply.append(stock.resource)

		#find valid selling locations
		td = []
		for location in d:
			s = len(p_supply)
			for resource in p_supply:
				if location.get_demand(resource) <= 0:
					s -= 1
			if s <= 0:
				td.append(location)


		#delete others
		if len(td) != len(d):
			for l in td:
				d.remove(l)
		else:
			print("Inoperable. Moving.")

		print(f"Sell points: {d}")

		w = [0 for x in d]
		
		n = range(len(d))

		for i in n:
			w[i] += (1 + (1000000/Vector2.distance(self.position, d[i].position)**2)**1.5) * w_distance

		for i in n:
			w[i] += (d[i].prosperity * 3) * w_prosperity

		for i in n:
			w[i] += 0

		return w, d