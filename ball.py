import constants
import vector2
import random
import sys
class Ball:
	def __init__(self, x = 0):
		self.pos = vector2.Vector2(100*(x+1) + random.randint(-50, 50), random.randint(50, 200))
		self.speed = vector2.Vector2(3, 3)
		aux = random.randint(-1, 1)
		if aux<0:
			self.speed.x *=-1
		aux = random.randint(-1, 1)
		if aux<0:
			self.speed.y *=-1
		while self.pos.x > constants.SCREEN_SIZE[0]:
			self.pos.x -= constants.SCREEN_SIZE[0]
			self.pos.y += 200
		# self.pos.x = 200*(x+1)
		# self.pos.y = 100

	def update(self, grid):
		nextPos = vector2.Vector2(self.pos.x + constants.BALL_RADIUS*(self.speed.x/abs(self.speed.x)), self.pos.y + constants.BALL_RADIUS*self.speed.y/abs(self.speed.y))
		actualGrid = [int(round(self.pos.x/constants.SCALE[0])), int(round(self.pos.y/constants.SCALE[1]))]		
		nextGrid = [int(round(nextPos.x/constants.SCALE[0])), int(round(nextPos.y/constants.SCALE[1]))]
		if grid[nextGrid[0]][actualGrid[1]] == constants.CONQUERED:
			self.speed.x *= -1
			nextPos.x = self.pos.x + self.speed.x
			nextGrid[0] = int(round(nextPos.x/constants.SCALE[0]))
		if grid[actualGrid[0]][nextGrid[1]] == constants.CONQUERED:
			self.speed.y *= -1
			nextPos.y = self.pos.y + self.speed.y
			nextGrid[1] = int(round(nextPos.y/constants.SCALE[1]))

		if grid[nextGrid[0]][nextGrid[1]] == constants.PROCESS:
			print("YOU LOST :(");
			sys.exit()
		self.pos = vector2.Vector2(self.pos.x + self.speed.x, self.pos.y + self.speed.y)
