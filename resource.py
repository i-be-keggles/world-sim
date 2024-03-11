import math

class Resource():
	def __init__(self, name, value, legality = 5):
		self.name = name
		self.value = value
		self.legality = legality

	def __str__(self):
		return f"{self.name}: c{self.value}, l{self.legality}"

	def __repr__(self):
		return self.__str__()

	def __eq__(self, other):
		return self.name == other.name


class ResourceStock():
	def __init__(self, resource, amount):
		self.resource = resource
		self.amount = amount


	def __str__(self):
		return f"{self.amount} {self.resource.name} (for c{self.resource.value * self.amount})"

	def __repr__(self):
		return self.__str__()

	def change(self, n):
		self.amount += n


def Generator():
	def __init__(self, resource, rate, cap=None):
		self.resource = resource
		self.rate = rate
		self.cap = cap

	def generate(self):
		n = self.rate
		if cap is not None:
			if math.abs(n) > cap:
				n = cap * (n/math.abs(n)) # set sign
			cap -= math.abs(n)

		return n


#turn unto dictionary. separate class for resources unecessary
#resources = [{"id":0, "name": "Fuel", "value": 3}, {"id":1, "name": "Food", "value": 3}]
resources = [Resource("Fuel", 3), Resource("Food", 3)]