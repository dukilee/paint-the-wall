import ball
import constants
import engine
import hero
import pygame

from pygame.locals import *

class level_Hero(hero.Hero):
	pass
	
class level_Ball(ball.Ball):
	pass

		
class Stage_1(engine.Engine):

	def initialSettings(self):
		self.timerMax = 60

	def createObjects(self):
		self.numberBalls = 2
		for i in range(self.numberBalls):
			self._ball.append(level_Ball())

	def winCondition(self):
		if self.cont >= 1:
			return True
		return False

	def getInstructions(self):
		return 'Conquer 500 blocks in less than 60 seconds.'

class Stage_2(engine.Engine):

	def initialSettings(self):
		self.timerMax = 80

	def createObjects(self):
		self.numberBalls = 4
		for i in range(self.numberBalls):
			self._ball.append(level_Ball())

	def winCondition(self):
		if self.numberRegions == 2 :
			return True
		return False

	def getInstructions(self):
		return 'Split the balls into two regions in under 80 seconds.'

class Stage_3(engine.Engine):

	def initialSettings(self):
		self.timerMax = 70

	def createObjects(self):
		self.numberBalls = 2
		for i in range(self.numberBalls):
			self._ball.append(level_Ball())

	def winCondition(self):
		if self.ballsKilled == 1 :
			return True
		return False
	def getInstructions(self):
		return 'Kill 1 ball in under 70 seconds.'

class Stage_4(engine.Engine):

	def initialSettings(self):
		self.numberMovementsMax = 5

	def createObjects(self):
		self.numberBalls = 2
		for i in range(self.numberBalls):
			self._ball.append(level_Ball())

	def winCondition(self):
		if self.cont >= 700:
			return True
		return False

	def getInstructions(self):
		return 'Conquer 700 blocks in less than 5 moves.'
		
class Stage_5(engine.Engine):

	def initialSettings(self):
		self.timerMax = 100

	def createObjects(self):
		self.numberBalls = 5
		for i in range(self.numberBalls):
			self._ball.append(level_Ball())

	def winCondition(self):
		if self.ballsKilled >= 4 :
			return True
		return False

	def getInstructions(self):
		return 'Destroy 4 balls in under 100 seconds.'

class Stage_6(engine.Engine):

	def stageDifferences(self, screen):
		r = Rect(self.xx*constants.SCALE[0], self.yy*constants.SCALE[1],
				constants.SCALE[0], constants.SCALE[1])
		pygame.draw.rect(screen, constants.DARK_GREEN, r)
		self.objectErase.append(r)

	def initialSettings(self):
		self.xx = int(constants.GRID_SIZE[0]/2);
		self.yy = int(constants.GRID_SIZE[1]/2);
		self.timerMax = 30

	def createObjects(self):
		self.numberBalls = 10
		for i in range(self.numberBalls):
			self._ball.append(level_Ball())

	def winCondition(self):
		if self.grid[self.xx][self.yy] == constants.CONQUERED:
			return True
		return False

	def getInstructions(self):
		return 'Conquer the central square in under 30 seconds.'

class Stage_7(engine.Engine):

	def initialSettings(self):
		self.timerMax = 45

	def createObjects(self):
		self.numberBalls = 4
		for i in range(self.numberBalls):
			self._ball.append(level_Ball())

	def winCondition(self):
		if self.cont >= 700:
			return True
		return False

	def getInstructions(self):
		return 'Conquer 1200 blocks in under 45 seconds.'

class Stage_8(engine.Engine):

	def initialSettings(self):
		self.numberMovementsMax = 17

	def createObjects(self):
		self.numberBalls = 6
		for i in range(self.numberBalls):
			self._ball.append(level_Ball())

	def winCondition(self):
		if self.numberRegions == 3:
			return True
		return False

	def getInstructions(self):
		return 'Split the balls in 3 regions with 17 moves.'


class Stage_9(engine.Engine):

	def stageDifferences(self, screen):
		r = Rect(self.x1*constants.SCALE[0], self.y1*constants.SCALE[1],
				constants.SCALE[0], constants.SCALE[1])
		pygame.draw.rect(screen, constants.DARK_GREEN, r)
		self.objectErase.append(r)
		r = Rect(self.x1*constants.SCALE[0], self.y2*constants.SCALE[1],
				constants.SCALE[0], constants.SCALE[1])
		pygame.draw.rect(screen, constants.DARK_GREEN, r)
		self.objectErase.append(r)
		r = Rect(self.x2*constants.SCALE[0], self.y1*constants.SCALE[1],
				constants.SCALE[0], constants.SCALE[1])
		pygame.draw.rect(screen, constants.DARK_GREEN, r)
		self.objectErase.append(r)
		r = Rect(self.x2*constants.SCALE[0], self.y2*constants.SCALE[1],
				constants.SCALE[0], constants.SCALE[1])
		pygame.draw.rect(screen, constants.DARK_GREEN, r)
		self.objectErase.append(r)

	def initialSettings(self):
		self.x1 = int(constants.GRID_SIZE[0]/4);
		self.y1 = int(constants.GRID_SIZE[1]/4);
		self.x2 = int(3*constants.GRID_SIZE[0]/4);
		self.y2 = int(3*constants.GRID_SIZE[1]/4);
		self.timerMax = 79

	def createObjects(self):
		self.numberBalls = 10
		for i in range(self.numberBalls):
			self._ball.append(level_Ball())

	def winCondition(self):
		if self.grid[self.x1][self.y1] == constants.CONQUERED and self.grid[self.x1][self.y2] == constants.CONQUERED and self.grid[self.x2][self.y1] == constants.CONQUERED and self.grid[self.x2][self.y2] == constants.CONQUERED:
			return True
		return False

	def getInstructions(self):
		return 'Conquer ALL dark green squares in less than 50 seconds.'

class Stage_10(engine.Engine):

	def initialSettings(self):
		self.timerMax = 27

	def createObjects(self):
		self.numberBalls = 10
		for i in range(self.numberBalls):
			self._ball.append(level_Ball())

	def winCondition(self):
		if self.ballsKilled > 0:
			return True
		return False

	def getInstructions(self):
		return 'Destroy 1 ball in under 27 seconds.'
