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
		if self.score>400:
			return True
		return False
