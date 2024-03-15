import math
import random

class Vector2():

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return f"({self.x}, {self.y})"

	def __add__(self, other):
		return Vector2(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return Vector2(self.x - other.x, self.y - other.y)

	def __mul__(self, a):
		return Vector2(self.x * a, self.y * a)

	def __truediv__(self, a):
		return Vector2(self.x / a, self.y / a)

	def magnitude(self):
		return math.sqrt(self.x**2 + self.y**2)

	def normalised(self):
		m = self.magnitude()
		if m == 0:
			return Vector2(0,0)
		return self / m

	def distance(a, b):
		return (a - b).magnitude()


def random_name_ship():
	a = ["Radiant", "Swift", "Majestic", "Vigilant", "Ethereal", "Cerulean", "Stalwart", "Nebulous", "Sapphire", "Fierce", "Celestial", "Resolute", "Infinite", "Luminous", "Gallant", "Phantom", "Sovereign", "Vivid", "Enigmatic", "Peregrine", "Vortex", "Epic", "Astral", "Blazing", "Nautical", "Eclipsed", "Daring", "Serene", "Thunderous", "Pristine", "Zenith", "Cascade", "Harmony", "Illustrious", "Velvet", "Roaring", "Ethereal", "Prowling", "Valiant", "Umbra", "Zephyr", "Halcyon", "Vesper", "Crimson", "Azure", "Quicksilver", "Inferno", "Radiant", "Adventurous", "Aureate", "Lustrous", "Vivid", "Dusky", "Solar", "Stellar", "Ethereal", "Dazzling", "Vibrant", "Sable", "Mystic", "Glorious", "Sculpted", "Iridescent", "Noble", "Epic", "Silent", "Rapid", "Eternal", "Obsidian", "Dynamic", "Celestial", "Harmonic", "Grand", "Reverent", "Whispering", "Illuminated", "Abyssal", "Marine", "Ornate", "Ephemeral", "Pendulum", "Radiant", "Galactic", "Cerulean", "Crimson", "Gossamer", "Sonorous", "Vorpal", "Ineffable", "Zephyrian", "Weeping", "Storm", "Spirit", "Widow's"]
	b = ["Horizon", "Tempest", "Aegis", "Crest", "Rhapsody", "Vanguard", "Serenity", "Cynosure", "Harbinger", "Pinnacle", "Labyrinth", "Quasar", "Sentinel", "Monolith", "Tranquility", "Eclipse", "Chronicle", "Odyssey", "Nebula", "Arcadia", "Citadel", "Aurora", "Oracle", "Zephyr", "Ephemera", "Oblivion", "Vortex", "Paragon", "Cascade", "Equinox", "Labyrinth", "Prelude", "Veracity", "Fathom", "Infinity", "Voyage", "Elysium", "Tempest", "Apex", "Halcyon", "Celestia", "Genesis", "Oasis", "Allegro", "Nimbus", "Echelon", "Pantheon", "Spectra", "Solitude", "Scepter", "Apogee", "Radiance", "Chalice", "Chronicle", "Abyss", "Aether", "Mirage", "Quintessence", "Peregrine", "Paradigm", "Harmony", "Nautica", "Aegis", "Epoch", "Luminosity", "Equilibrium", "Pinnacle", "Ephemeron", "Inception", "Vigil", "Provenance", "Resonance", "Scepter", "Myriad", "Silhouette", "Aegis", "Oblivion", "Ascendant", "Serenade", "Sculpture", "Zephyr", "Ethereality", "Synchrony", "Panorama", "Eclipse", "Phantom", "Talisman", "Storm", "Spirit", "Somnambulist", "Widow"]
	return f"{random.choice(a)} {random.choice(b)}"


def rgb_to_hex(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'


def clamp(a, min, max):
	if a < min:
		return min
	if a > max:
		return max
	return a


def scale(arr):
	a = arr.copy()
	_min = min(a)
	_max = max(a)

	for i in range(len(a)):
		a[i] = (a[i] - _min) / (_max - _min)

	return a