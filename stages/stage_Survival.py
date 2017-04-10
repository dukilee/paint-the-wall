import random
import time

from actors import ball, hero
from main import engine
from resources import constants, tools

class level_Hero(hero.Hero):
	pass
	
class level_Ball(ball.Ball):
	def __init__(self):
		self.pos = tools.Vector2(400, 300)
		self.speed = tools.Vector2(3, 3)
		self.destructedBlocks = 0

		if random.randint(-1, 1) < 0:
			self.speed.x *=-1

		if random.randint(-1, 1) < 0:
			self.speed.y *=-1

	def update(self, grid):
		self.destructedBlocks = 0
		nextPos = tools.Vector2(self.pos.x + constants.BALL_RADIUS*(self.speed.x/abs(self.speed.x)), self.pos.y + constants.BALL_RADIUS*self.speed.y/abs(self.speed.y))
		actualGrid = tools.discretize(self.pos)
		nextGrid = tools.discretize(nextPos)
		
		if grid[nextGrid[0]][actualGrid[1]] == constants.CONQUERED:
			if nextGrid[0] > 0 and nextGrid[0] < len(grid) - 1:
				grid[nextGrid[0]][actualGrid[1]] = constants.NOTHING
				self.destructedBlocks -= 1
			self.speed.x *= -1
			nextPos.x = self.pos.x + self.speed.x
			nextGrid[0] = tools.conv(nextPos.x, 0)

		if grid[actualGrid[0]][nextGrid[1]] == constants.CONQUERED:
			if nextGrid[1] > 0 and nextGrid[1] < len(grid[actualGrid[0]]) - 1:
				grid[actualGrid[0]][nextGrid[1]] = constants.NOTHING
				self.destructedBlocks -= 1
			self.speed.y *= -1
			nextPos.y = self.pos.y + self.speed.y
			nextGrid[1] = tools.conv(nextPos.y, 1)

		if grid[nextGrid[0]][nextGrid[1]] == constants.PROCESS:
			print("YOU LOST :(");
			#sys.exit()
			return constants.LOSE

		self.pos = tools.Vector2(self.pos.x + self.speed.x, self.pos.y + self.speed.y)

		return constants.UNDEFINED

class Stage_Survival(engine.Engine):
	def createObjects(self):
		for i in range(self.numberBalls):
			self._ball.append(level_Ball())

	def winCondition(self):
		return False

	def stageDifferences(self, screen):
		for b in self._ball:
			self.cont += b.destructedBlocks

		self.minimum = 500-int(96000/(4*(time.clock() - self.timeStart) + 120))
		n = int((self.minimum+300)/100)
		if n > self.numberBalls:
			self._ball.append(level_Ball())
			self.numberBalls = n

	def getInstructions(self):
		return 'Survive ;)  :b'