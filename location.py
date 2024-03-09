class Location:
	def __init__(self, name, position):
		self.name = name
		self.position = position

	def __str__(self):
		return f"{self.name}"

	def __repr__(self):
		return f"{self.name}"