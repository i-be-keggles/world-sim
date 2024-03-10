from util import *
from resource import *

class Location:
	canvas = None

	def __init__(self, name, position, stocks = [], prosperity = 50, p_graphic = None):
		self.name = name
		self.position = position
		self.prosperity = prosperity
		self.stocks = []

	def __str__(self):
		return f"{self.name}"

	def __repr__(self):
		return f"{self.name}"

	def update(self):
		self.update_graphics()

	def GetSupply(self, resource):
		for i in stocks:
			if i == resource:
				return i.supply.amount
		return 0

	def GetDemand(self, resource):
		for i in stocks:
			if i == resource:
				return i.demand.amount
		return 0


	def update_graphics(self):
		n = clamp(self.prosperity, 0, 255)
		pos = self.position
		size = n/10 + 10
		x1, y1 = (pos.x - size), (pos.y - size)
		x2, y2 = (pos.x + size), (pos.y + size)
		self.canvas.coords(self.p_graphic, x1, y1, x2, y2)
		self.canvas.itemconfig(self.p_graphic, fill=rgb_to_hex(n//2,n//2,n//2))


	def buy_resource(self, resource, amount):
		for i in self.stocks:
			if i.resource == resource:
				if i.supply.amount < amount:
					amount = i.supply.amount
				i.supply.change(-amount)
				return amount



class Stock():
	def __init__(self, resource, supply_value, demand_value):
		self.resource = resource
		self.supply = ResourceStock(resource, supply_value)
		self.demand = ResourceStock(resource, demand_value)

	def __str__(self):
		return f"{self.resource.name}, s:{self.supply.amount} d:{self.demand.amount}"

	def __repr__(self):
		return self.__str__()