import random
from resource import *
from util import *

class Actor():
	destinations = []
	tk_root = None
	canvas = None
	simspeed = 1

	def __init__(self, name, position, destination, speed, cargo_cap, lawfulness = 10, graphics=None):
		self.name = name
		self.position = position
		self.destination = destination
		self.speed = speed

		self.lawfulness = lawfulness

		self.cargo_capacity = cargo_cap
		self.cargo = []

		self.graphics = graphics

		self.state = "moving"

		self.prev_sell = []


	def update(self):
		if self.state == "moving":
			self.move()


	def move(self):
		d = (self.destination.position - self.position).normalised() * self.speed * self.simspeed
		self.position += d
		self.canvas.move(self.graphics, d.x, d.y)

		if Vector2.distance(self.position, self.destination.position) <= self.speed * self.simspeed:
			self.arrive_at_location()


	def arrive_at_location(self):
		self.state = "waiting"
		self.tk_root.after(random.randint(2000,6000) // self.simspeed, self.leave_location)

		#print(f"{self.name} arrived at {self.destination.name}")

		self.sell()
		#print()


	def leave_location(self):

		dest = self.find_new_destination()

		self.buy(next_destination=dest)
		#print(f"{self.name} starting from {self.destination.name} to {dest.name}")
		self.destination = dest

		self.state = "moving"
		#print()


	def buy(self, next_destination):
		self.destination.prosperity += 5

		# find item with highest supply
		supply = [s.supply for s in self.destination.stocks]
		#stock = self.destination.stocks[supply.index(max([s.supply.amount for s in self.destination.stocks]))]
		resource = self.find_best_buy(self.destination, next_destination, log=False)
		if resource is None:
			#print(f"No good buy.")
			return

		self.prev_sell = []

		a = self.get_free_cargo_space()
		#buy as much as possible
		a = self.destination.give_resource(resource, a)


		if a > 0:
			self.add_cargo(ResourceStock(resource, a))

		#print(f"Bought {a} {resource['name']}")
		if resource['name'] == 'Drugs':
				print(f"Drug run from l{self.lawfulness}")
		print()


	def sell(self):
		if len(self.cargo) == 0:
			return

		self.destination.prosperity -= 5
		
		ps = ""

		for stock in self.cargo:
			self.destination.get_resource(stock.resource, stock.amount)
			self.cargo.remove(stock)

			self.prev_sell.append(stock)

			ps += f"{stock.amount} {stock.resource['name']} "

			if stock.resource['name'] == "Drugs":
				print(f"selling {stock.amount} rugs")

		#print(f"Sold {ps}")



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
		w, d = self.destination_weights(d, 1, 1, 1)
		d = random.choices(d, weights = w)
		return d[0]


	def destination_weights(self, d, w_distance, w_prosperity, w_potential):
		w = [0 for x in d]
		
		n = range(len(d))

		for i in n:
			w[i] += (1 + (1000000/Vector2.distance(self.position, d[i].position)**2)**1.5) * w_distance

		for i in n:
			w[i] += (d[i].prosperity * 3) * w_prosperity

		return w, d


	def find_best_buy(self, cur_destination, next_destination, w_demand = 1, w_lawfulness = 10, log=False):
		p_buy = []
		weights = []

		ignore_understocked = True

		for stock in cur_destination.stocks:
			if ((stock.supply > stock.target) or ignore_understocked) and stock.resource not in [p.resource for p in self.prev_sell] and next_destination.get_target_supply(stock.resource):
					p_buy.append(stock.resource)
					w = 0
					w += (next_destination.get_demand(stock.resource) - cur_destination.get_demand(stock.resource)) * stock.resource['value'] * w_demand
					w += (stock.resource['legality'] - max(stock.resource['legality'], self.lawfulness)) * w_lawfulness * stock.resource['value']
					weights.append(w)

					if log:
						print(f"stock: {stock.resource['name']}, lawfulness: {self.lawfulness}, weight:{w}")

		if len(p_buy) == 0 or max(weights) <= 0 or sum(weights) == 0:
			#print(f"everything fucked at {cur_destination.name}")
			return None
		else:
			m = min(weights)
			if m < 0:
				for i in range(len(weights)):
					weights[i] -= m
			return random.choices(p_buy, weights)[0]


	def __str__(self):
		return f"{self.name}, {self.cargo_capacity}, {self.cargo}"



class Trader(Actor):
	def destination_weights(self, d, w_distance, w_prosperity, w_potential):

		#possible things to buy
		p_supply = []

		for stock in self.destination.stocks:
			if stock.supply > stock.target:
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
			#print("Inoperable. Moving.")
			pass

		w = [0 for x in d]
		
		n = range(len(d))

		for i in n:
			dis = (1 + (1000000/Vector2.distance(self.position, d[i].position)**2)**1.5)
			w[i] += dis * w_distance

		for i in n:
			s = []
			for stock in self.destination.stocks:
				s.append(d[i].get_demand(stock.resource) - self.destination.get_demand(stock.resource))
				if stock.resource not in [x.resource for x in d[i].stocks]:
					s[-1] = 0
				else:
					s[-1] *= stock.resource['value']/3
				#print(f"{d[i].name} {stock.resource['name']} {s[-1]}")


			best = s.index(max(s))

			w[i] += s[best]/6 * w_prosperity


		for i in n:
			# FUTURE-POTENTIAL WEIGHT (eg looking ahead bc something on another dest will make them rich)
			s = 0
			for stock in d[i].stocks:
				s += max(0, -d[i].get_demand(stock.resource))
			w[i] += s * w_potential


		for i in n:
			w[i] = max(w[i], 0.00001)

		for i in n:
			w[i] += 0

		return w, d