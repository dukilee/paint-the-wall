import pygame

from actors import ball, hero
from main import engine
from pygame.locals import *
from resources import constants
from user_data import data

class Stage_1(engine.Engine):
	def initialSettings(self):
		self.timerMax = 60

	def createObjects(self):
		self.numberBalls = 2
		for i in range(self.numberBalls):
			self._ball.append(ball.Ball())

	def winCondition(self):
		if self.cont >= 60:
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
			self._ball.append(ball.Ball())

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
			self._ball.append(ball.Ball())

	def winCondition(self):
		if self.ballsKilled >= 1 :
			return True
		return False
	def getInstructions(self):
		return 'Destroy 1 ball in under 70 seconds.'

class Stage_4(engine.Engine):
	def initialSettings(self):
		self.timerMax = 40

	def createObjects(self):
		self.numberBalls = 6
		for i in range(self.numberBalls):
			self._ball.append(ball.Ball())

	def winCondition(self):
		if self.numberRegions == 2:
			return True
		return False

	def getInstructions(self):
		return 'Split the balls into two regions in under 40 seconds.'


class Stage_5(engine.Engine):
	def initialSettings(self):
		self.timerMax = 32

	def createObjects(self):
		self.numberBalls = 5
		for i in range(self.numberBalls):
			self._ball.append(ball.Ball())

	def winCondition(self):
		if self.cont >= 501:
			return True
		return False

	def getInstructions(self):
		return 'Conquer 501 blocks in less than 32 seconds.'

class Stage_6(engine.Engine):
	def initialSettings(self):
		self.timerMax = 23

	def createObjects(self):
		self.numberBalls = 7
		for i in range(self.numberBalls):
			self._ball.append(ball.Ball())

	def winCondition(self):
		if self.ballsKilled > 0:
			return True
		return False

	def getInstructions(self):
		return 'Destroy 1 ball in under 23 seconds.'


class Stage_7(engine.Engine):
	def stageDifferences(self, screen):
		r = Rect(self.xx*constants.SCALE[0], self.yy*constants.SCALE[1],
				constants.SCALE[0], constants.SCALE[1])
		pygame.draw.rect(screen, constants.DARK_GREEN, r)
		self.objectErase.append(r)

	def initialSettings(self):
		self.xx = int(constants.GRID_SIZE[0]/2)
		self.yy = int(constants.GRID_SIZE[1]/2)
		self.timerMax = 30

	def createObjects(self):
		self.numberBalls = 7
		for i in range(self.numberBalls):
			self._ball.append(ball.Ball())

	def winCondition(self):
		if self.grid[self.xx][self.yy] == constants.CONQUERED:
			return True
		return False

	def getInstructions(self):
		return 'Conquer the central square in under 30 seconds.'

class Stage_8(engine.Engine):
	def initialSettings(self):
		self.numberMovementsMax = 9

	def createObjects(self):
		self.numberBalls = 8
		for i in range(self.numberBalls):
			self._ball.append(ball.Ball())

	def winCondition(self):
		if self.numberRegions == 2:
			return True
		return False

	def getInstructions(self):
		return 'Split the balls in 2 regions with 9 moves.'


class Stage_9(engine.Engine):
	def initialSettings(self):
		self.timerMax = 32

	def createObjects(self):
		self.numberBalls = 3
		for i in range(self.numberBalls):
			self._ball.append(ball.Ball())

	def winCondition(self):
		if self.cont >= 920:
			if self.ballsKilled==0:
				print("Pacifist Unlocked")
				data.i['pacifist'] = 1
			return True
		return False

	def getInstructions(self):
		return 'Conquer 920 blocks in less than 32 seconds.'

class Stage_10(engine.Engine):
	def initialSettings(self):
		self.timerMax = 37

	def createObjects(self):
		self.numberBalls = 7
		for i in range(self.numberBalls):
			self._ball.append(ball.Ball())

	def winCondition(self):
		if self.numberRegions == 3:
			return True
		return False

	def getInstructions(self):
		return 'Split the balls into three regions in under 37 seconds.'

class Stage_11(engine.Engine):
	def initialSettings(self):
		self.timerMax = 35

	def createObjects(self):
		self.numberBalls = 5
		for i in range(self.numberBalls):
			self._ball.append(ball.Ball())

	def winCondition(self):
		if self.ballsKilled >= 2 :
			return True
		return False

	def getInstructions(self):
		return 'Destroy 2 balls in under 35 seconds.'


class Stage_12(engine.Engine):
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
		self.timerMax = 50

	def createObjects(self):
		self.numberBalls = 7
		for i in range(self.numberBalls):
			self._ball.append(ball.Ball())

	def winCondition(self):
		if self.grid[self.x1][self.y1] == constants.CONQUERED and self.grid[self.x1][self.y2] == constants.CONQUERED and self.grid[self.x2][self.y1] == constants.CONQUERED and self.grid[self.x2][self.y2] == constants.CONQUERED:
			return True
		return False

	def getInstructions(self):
		return 'Conquer ALL dark green squares in less than 50 seconds.'

class Stage_13(engine.Engine):
	def initialSettings(self):
		self.numberMovementsMax = 15

	def createObjects(self):
		self.numberBalls = 8
		for i in range(self.numberBalls):
			self._ball.append(ball.Ball())

	def winCondition(self):
		if self.numberRegions == 3:
			return True
		return False

	def getInstructions(self):
		return 'Split the balls in 3 regions with 15 moves.'


class Stage_14(engine.Engine):
	def initialSettings(self):
		self.timerMax = 28

	def createObjects(self):
		self.numberBalls = 5
		for i in range(self.numberBalls):
			self._ball.append(ball.Ball())

	def winCondition(self):
		if self.cont >= 600:
			return True
		return False

	def getInstructions(self):
		return 'Conquer 600 blocks in less than 28 seconds.'

class Stage_15(engine.Engine):
	def stageDifferences(self, screen):
		r = Rect(self.x1 * constants.SCALE[0], self.y1 * constants.SCALE[1],
				 constants.SCALE[0], constants.SCALE[1])
		pygame.draw.rect(screen, constants.DARK_GREEN, r)
		self.objectErase.append(r)
		r = Rect(self.x1 * constants.SCALE[0], self.y2 * constants.SCALE[1],
				 constants.SCALE[0], constants.SCALE[1])
		pygame.draw.rect(screen, constants.DARK_GREEN, r)
		self.objectErase.append(r)
		r = Rect(self.x2 * constants.SCALE[0], self.y1 * constants.SCALE[1],
				 constants.SCALE[0], constants.SCALE[1])
		pygame.draw.rect(screen, constants.DARK_GREEN, r)
		self.objectErase.append(r)
		r = Rect(self.x2 * constants.SCALE[0], self.y2 * constants.SCALE[1],
				 constants.SCALE[0], constants.SCALE[1])
		pygame.draw.rect(screen, constants.DARK_GREEN, r)
		self.objectErase.append(r)

	def initialSettings(self):
		self.x1 = int(3*constants.GRID_SIZE[0] / 8)
		self.y1 = int(3*constants.GRID_SIZE[1] / 8)
		self.x2 = int(5 * constants.GRID_SIZE[0] / 8)
		self.y2 = int(5 * constants.GRID_SIZE[1] / 8)
		self.numberMovementsMax = 10

	def createObjects(self):
		self.numberBalls = 7
		for i in range(self.numberBalls):
			self._ball.append(ball.Ball())

	def winCondition(self):
		if self.grid[self.x1][self.y1] == constants.CONQUERED and self.grid[self.x1][self.y2] == constants.CONQUERED and \
						self.grid[self.x2][self.y1] == constants.CONQUERED and self.grid[self.x2][
			self.y2] == constants.CONQUERED:
			return True
		return False

	def getInstructions(self):
		return 'Conquer ALL dark green squares in less than 10 moves.'

class Stage_16(engine.Engine):
	def initialSettings(self):
		self.timerMax = 35

	def createObjects(self):
		self.numberBalls = 7
		for i in range(self.numberBalls):
			self._ball.append(ball.Ball())

	def winCondition(self):
		if self.ballsKilled >= 3 :
			return True
		return False

	def getInstructions(self):
		return 'Destroy 3 balls in under 35 seconds.'

class Stage_17(engine.Engine):
	def stageDifferences(self, screen):
		r = Rect((self.x1) * constants.SCALE[0], self.y1 * constants.SCALE[1],
				 constants.SCALE[0], constants.SCALE[1])
		pygame.draw.rect(screen, constants.DARK_GREEN, r)
		self.objectErase.append(r)
		r = Rect((self.x1 - 1) * constants.SCALE[0], (self.y2 - 1) * constants.SCALE[1],
				 constants.SCALE[0], constants.SCALE[1])
		pygame.draw.rect(screen, constants.DARK_GREEN, r)
		self.objectErase.append(r)

		r = Rect((self.x1) * constants.SCALE[0], (self.y2) * constants.SCALE[1],
				 constants.SCALE[0], constants.SCALE[1])
		pygame.draw.rect(screen, constants.DARK_GREEN, r)
		self.objectErase.append(r)

		r = Rect((self.x1 + 1) * constants.SCALE[0], (self.y2 + 1) * constants.SCALE[1],
				 constants.SCALE[0], constants.SCALE[1])
		pygame.draw.rect(screen, constants.DARK_GREEN, r)
		self.objectErase.append(r)

		r = Rect((self.x2) * constants.SCALE[0], self.y1 * constants.SCALE[1],
				 constants.SCALE[0], constants.SCALE[1])
		pygame.draw.rect(screen, constants.DARK_GREEN, r)
		self.objectErase.append(r)
		r = Rect((self.x2 + 1) * constants.SCALE[0], (self.y2 - 1) * constants.SCALE[1],
				 constants.SCALE[0], constants.SCALE[1])
		pygame.draw.rect(screen, constants.DARK_GREEN, r)
		self.objectErase.append(r)

		r = Rect((self.x2) * constants.SCALE[0], (self.y2) * constants.SCALE[1],
				 constants.SCALE[0], constants.SCALE[1])
		pygame.draw.rect(screen, constants.DARK_GREEN, r)
		self.objectErase.append(r)

		r = Rect((self.x2 -1) * constants.SCALE[0], (self.y2 + 1) * constants.SCALE[1],
				 constants.SCALE[0], constants.SCALE[1])
		pygame.draw.rect(screen, constants.DARK_GREEN, r)
		self.objectErase.append(r)

	def initialSettings(self):
		self.x1 = int(constants.GRID_SIZE[0] / 2) - 2;
		self.y1 = int(constants.GRID_SIZE[1] / 2)-  4;
		self.x2 = self.x1 + 3
		self.y2 = self.y1 + 5
		self.timerMax = 25

	def createObjects(self):
		self.numberBalls = 9
		for i in range(self.numberBalls):
			self._ball.append(ball.Ball())

	def winCondition(self):
		if self.grid[self.x1][self.y1] == constants.CONQUERED and self.grid[self.x1][self.y2] == constants.CONQUERED and \
						self.grid[self.x1-1][self.y2-1] == constants.CONQUERED and self.grid[self.x1+1][
			self.y2+1] == constants.CONQUERED and self.grid[self.x2][self.y1] == constants.CONQUERED and self.grid[self.x2][self.y2] == constants.CONQUERED and \
						self.grid[self.x2+1][self.y2-1] == constants.CONQUERED and self.grid[self.x2-1][
			self.y2+1] == constants.CONQUERED:
			return True
		return False

	def getInstructions(self):
		return 'Conquer ALL dark green squares in less than 25 seconds.'

class Stage_18(engine.Engine):
	def initialSettings(self):
		self.timerMax = 37

	def createObjects(self):
		self.numberBalls = 9
		for i in range(self.numberBalls):
			self._ball.append(ball.Ball())

	def winCondition(self):
		if self.numberRegions == 4:
			return True
		return False

	def getInstructions(self):
		return 'Split the balls into four regions in under 37 seconds.'

class Stage_19(engine.Engine):
	def initialSettings(self):
		self.timerMax = 29

	def createObjects(self):
		self.numberBalls = 7
		for i in range(self.numberBalls):
			self._ball.append(ball.Ball())

	def winCondition(self):
		if self.cont >= 650:
			return True
		return False

	def getInstructions(self):
		return 'Conquer 650 blocks in less than 29 seconds.'

class Stage_20(engine.Engine):
	def initialSettings(self):
		self.timerMax = 31

	def createObjects(self):
		self.numberBalls = 10
		for i in range(self.numberBalls):
			self._ball.append(ball.Ball())

	def winCondition(self):
		if self.ballsKilled >= 4:
			return True
		return False

	def getInstructions(self):
		return 'Destroy 4 balls in under 31 seconds.'