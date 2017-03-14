import constants
import vector2
import random
import sys
import tools

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

	def update(self, grid):
		nextPos = vector2.Vector2(self.pos.x + constants.BALL_RADIUS*(self.speed.x/abs(self.speed.x)), self.pos.y + constants.BALL_RADIUS*self.speed.y/abs(self.speed.y))
		actualGrid = tools.discretize(self.pos)
		nextGrid = tools.discretize(nextPos)
		
		if grid[nextGrid[0]][actualGrid[1]] == constants.CONQUERED:
			self.speed.x *= -1
			nextPos.x = self.pos.x + self.speed.x
			nextGrid[0] = tools.round_coord(nextPos.x, 0)
		
		if grid[actualGrid[0]][nextGrid[1]] == constants.CONQUERED:
			self.speed.y *= -1
			nextPos.y = self.pos.y + self.speed.y
			nextGrid[1] = tools.round_coord(nextPos.y, 1)
		
		if grid[nextGrid[0]][nextGrid[1]] == constants.PROCESS:
			print("YOU LOST :(");
			#sys.exit()
			return constants.LOSE

		self.pos = vector2.Vector2(self.pos.x + self.speed.x, self.pos.y + self.speed.y)

		return constants.UNDEFINED
