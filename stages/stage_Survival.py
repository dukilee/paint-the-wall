import random
from user_data import data

from actors import ball, hero
from main import engine
from resources import constants, tools

class level_Hero(hero.Hero):
	"""
	Differences to the hero of the current stage
	"""
	pass
	
class level_Ball(ball.Ball):
	"""
	Differences to the ball of the current stage
	"""
	def __init__(self):
		ball.Ball.__init__(self)
		self.pos = tools.Vector2(400, 300)
		self.destructedBlocks = 0

	def update(self, grid):
		"""
		This ball is capable of destroying the wall, so this function updates the ball position,
		destroys the wall and check if the ball killed the hero.
		:param grid: current state of the game
		:return: returns if the ball killed or not the hero
		"""
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
			return constants.LOSE

		self.pos = tools.Vector2(self.pos.x + self.speed.x, self.pos.y + self.speed.y)

		return constants.UNDEFINED

class Stage_Survival(engine.Engine):
	"""	Defines stage win/lose conditions"""
	def createObjects(self):
		"""Instantiates the balls"""
		for i in range(self.numberBalls):
			self._ball.append(level_Ball())

	def winCondition(self):
		"""Checks if the player did enough to pass to next stage"""
		return False

	def initialSettings(self):
		"""Sets initial values to variables"""
		self.action = constants.SURVIVAL_MENU

	def stageDifferences(self, screen):
		"""
		Allows the stage to draw on the screen
		:param screen: game screen, comes from pygame
		"""
		for b in self._ball:
			self.cont += b.destructedBlocks

		self.minimum = 500-int(96000/(4*(data.getActualTime() - self.timeStart) + 120))
		n = int((self.minimum+300)/100)
		if n > self.numberBalls:
			self._ball.append(level_Ball())
			self.numberBalls = n

	def getInstructions(self):
		""":return: string with the info of what the player needs to do."""
		return 'Survive ;)  :b'