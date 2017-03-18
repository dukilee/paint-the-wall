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
		self.timerMax = 100

	def createObjects(self):
		for i in range(self.numberBalls):
			self._ball.append(level_Ball())

	def winCondition(self):
		if self.ballsKilled == 4 :
			return True
		return False

	def writeInstructions(self, screen):
		font = pygame.font.SysFont('Calibri', 30, True, False)
		text = font.render("Destroy 4 balls in under 100 seconds.", True, constants.DARK_GREEN)
		screen.blit(text, [50, 200])
		
class Stage_2(engine.Engine):

	def initialSettings(self):
		self.numberMovementsMax = 7

	def createObjects(self):
		for i in range(self.numberBalls):
			self._ball.append(level_Ball())

	def winCondition(self):
		if self.cont >= 500:
			return True
		return False

	def writeInstructions(self, screen):
		font = pygame.font.SysFont('Calibri', 30, True, False)
		text = font.render("Conquer 500 blocks in less than 7 moves.", True, constants.DARK_GREEN)
		screen.blit(text, [50, 200])
		
