import math

resources = [
	{'id': 0, "name":"Fuel", "value":5, "legality": 10},
	{'id': 1, "name":"Food", "value":2, "legality": 10},
]


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


class Generator:
	generation_rate = 0.01

	def __init__(self, resource, rate, cap=None):
		self.resource = resource
		self.rate = rate
		self.cap = cap

	def generate(self):
		n = self.rate * self.generation_rate
		if self.cap is not None:
			if math.abs(n) > self.cap:
				n = self.cap * (n/math.abs(n)) # set sign
			self.cap -= math.abs(n) * self.generation_rate

		return n