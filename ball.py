import constants
import vector2
import random
import sys
import tools

class Ball:
	def __init__(self):
		self.pos = tools.random_pos() # random position on screen
		self.speed = vector2.Vector2(3, 3)

		if random.randint(-1, 1) < 0:
			self.speed.x *=-1

		if random.randint(-1, 1) < 0:
			self.speed.y *=-1

	def valid_x(self, x, grid):
		return x >= 0 and x < len(grid)

	def valid_y(self, y, grid):
		if len(grid) > 0:
			return y >= 0 and y < len(grid[0])
		return False

	def valid(self, x, y, grid):
		return self.valid_x(x, grid) and self.valid_y(y, grid)

	def update(self, grid):
		nextPos = vector2.Vector2(self.pos.x + constants.BALL_RADIUS*(self.speed.x/abs(self.speed.x)), self.pos.y + constants.BALL_RADIUS*self.speed.y/abs(self.speed.y))
		actualGrid = tools.discretize(self.pos)
		nextGrid = tools.discretize(nextPos)
		
		if self.valid(nextGrid[0], actualGrid[1], grid) and grid[nextGrid[0]][actualGrid[1]] == constants.CONQUERED or not self.valid_x(nextGrid[0], grid):
			self.speed.x *= -1
			nextPos.x = self.pos.x + self.speed.x
			nextGrid[0] = tools.conv(nextPos.x, 0)
		
		if self.valid(actualGrid[0], nextGrid[1], grid) and grid[actualGrid[0]][nextGrid[1]] == constants.CONQUERED or not self.valid_y(nextGrid[1], grid):
			self.speed.y *= -1
			nextPos.y = self.pos.y + self.speed.y
			nextGrid[1] = tools.conv(nextPos.y, 1)
		
		if self.valid(nextGrid[0], nextGrid[1], grid) and grid[nextGrid[0]][nextGrid[1]] == constants.PROCESS:
			return constants.LOSE

		self.pos = vector2.Vector2(self.pos.x + self.speed.x, self.pos.y + self.speed.y)

		return constants.UNDEFINED