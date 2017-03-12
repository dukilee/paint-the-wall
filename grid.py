class Foo:
	pos = [3, 3]
	def __init__(self, y):
		self.pos[0] = 100*(y+1)

	def print(self):
		print("x = ", self.x)
