from util import *
from resource import *
import math

class Location:
	canvas = None

	def __init__(self, name, position, stocks = None, generators = None, prosperity = 50, p_graphic = None):
		self.name = name
		self.position = position
		self.prosperity = prosperity

		self.stocks = stocks
		if self.stocks is None:
			self.stocks = []

		self.generators = generators
		if self.generators is None:
			self.generators = []


	def __str__(self):
		return f"{self.name}"


	def __repr__(self):
		return f"{self.name}"


	def update(self):

		gtd = []
		for generator in self.generators:
			n = generator.generate()
			self.get_resource(generator.resource, n)
			if generator.cap is not None and generator.cap <= 0:
				gtd.append(generator)

		for f in gtd:
			self.generators.remove(g)

		self.update_graphics()


	def get_supply(self, resource):
		for i in self.stocks:
			if i.resource == resource:
				return i.supply.amount
		return 0


	def get_demand(self, resource):
		for i in self.stocks:
			if i.resource == resource:
				return i.demand.amount
		return 0


	def get_total_supply(self):
		t = 0
		for i in self.stocks:
			t += i.supply.amount
		return t


	def get_total_demand(self):
		t = 0
		for i in self.stocks:
			t += i.demand.amount
		return t


	def update_graphics(self):
		#n = clamp((int)((self.get_total_demand() + self.get_total_supply())**(1/1.5)*5)//1, 10, 255)
		n = clamp((int)((self.get_total_demand() + self.get_total_supply())**(1/1)*1)//1, 10, 255)
		pos = self.position
		size = n/10 + 10
		x1, y1 = (pos.x - size), (pos.y - size)
		x2, y2 = (pos.x + size), (pos.y + size)
		self.canvas.coords(self.p_graphic, x1, y1, x2, y2)
		self.canvas.itemconfig(self.p_graphic, fill=rgb_to_hex(n//2,n//2,n//2))


	#returns the amount of resources given
	def give_resource(self, resource, amount):
		for i in self.stocks:
			if i.resource == resource:
				if i.supply.amount < amount:
					amount = i.supply.amount
				i.supply.change(-amount)
				i.demand.change(amount)
				return amount


	
	def get_resource(self, resource, amount):
		for i in self.stocks:
			if i.resource == resource:
				i.supply.change(amount)
				i.demand.change(-amount)



class Stock():
	def __init__(self, resource, supply_value, demand_value):
		self.resource = resource
		self.supply = ResourceStock(resource, supply_value)
		self.demand = ResourceStock(resource, demand_value)

	def __str__(self):
		return f"{self.resource.name}, s:{self.supply.amount} d:{self.demand.amount}"

	def __repr__(self):
		return self.__str__()