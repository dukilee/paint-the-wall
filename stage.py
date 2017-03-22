import ball
import time
import constants
import engine
import grid
import hero
import pygame
import random
import sys
import tools
import vector2

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
		if self.cont >= 500:
			return True
		return False

	def writeInstructions(self, screen):
		font = pygame.font.SysFont('Calibri', 30, True, False)
		text = font.render("Conquer 500 blocks in less than 60 seconds.", True, constants.DARK_GREEN)
		screen.blit(text, [50, 200])
		
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

	def writeInstructions(self, screen):
		font = pygame.font.SysFont('Calibri', 30, True, False)
		text = font.render("Split the balls into two regions in under 80 seconds.", True, constants.DARK_GREEN)
		screen.blit(text, [50, 200])

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

	def writeInstructions(self, screen):
		font = pygame.font.SysFont('Calibri', 30, True, False)
		text = font.render("Kill 1 ball in under 70 seconds.", True, constants.DARK_GREEN)
		screen.blit(text, [50, 200])
		
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

	def writeInstructions(self, screen):
		font = pygame.font.SysFont('Calibri', 30, True, False)
		text = font.render("Conquer 700 blocks in less than 5 moves.", True, constants.DARK_GREEN)
		screen.blit(text, [50, 200])
		
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

	def writeInstructions(self, screen):
		font = pygame.font.SysFont('Calibri', 30, True, False)
		text = font.render("Destroy 4 balls in under 100 seconds.", True, constants.DARK_GREEN)
		screen.blit(text, [50, 200])

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
		print(self.xx, self.yy)
		if self.grid[self.xx][self.yy] == constants.CONQUERED:
			return True
		return False

	def writeInstructions(self, screen):
		font = pygame.font.SysFont('Calibri', 30, True, False)
		text = font.render("Conquer the central square in under 30 seconds.", True, constants.DARK_GREEN)
		screen.blit(text, [50, 200])


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

	def writeInstructions(self, screen):
		font = pygame.font.SysFont('Calibri', 30, True, False)
		text = font.render("Conquer 1200 blocks in under 45 seconds.", True, constants.DARK_GREEN)
		screen.blit(text, [50, 200])
