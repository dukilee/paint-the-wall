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
	def __init__(self):
		self.pos = vector2.Vector2(400, 300)
		self.speed = vector2.Vector2(3, 3)

		if random.randint(-1, 1) < 0:
			self.speed.x *=-1

		if random.randint(-1, 1) < 0:
			self.speed.y *=-1

	def update(self, grid):
		self.destructedBlocks = 0
		nextPos = vector2.Vector2(self.pos.x + constants.BALL_RADIUS*(self.speed.x/abs(self.speed.x)), self.pos.y + constants.BALL_RADIUS*self.speed.y/abs(self.speed.y))
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

		self.pos = vector2.Vector2(self.pos.x + self.speed.x, self.pos.y + self.speed.y)

		return constants.UNDEFINED

class Stage_Survival(engine.Engine):
	def run(self, screen):
		self._ball = []
		conquering = False #true if there is any process block
		repint = True #true when the whole screen needs to be redrawn
		objectErase = [] #marks the position of everything that surrounds objects(balls or hero)
		cont = 0
		minimum = -1
		score = 0
		timeStart = time.clock()

		for i in range(self.numberBalls):
			self._ball.append(level_Ball())

		pygame.init()
		doneRunning = False
		clock = pygame.time.Clock()

		# s_conquering = pygame.mixer.Sound('sounds/s_coin.wav')
		# s_conquered = pygame.mixer.Sound('sounds/s_up.wav')

		for i in range (constants.GRID_SIZE[0]):
			self.grid[i][0] = constants.CONQUERED
			self.grid[i][constants.GRID_SIZE[1]-1] = constants.CONQUERED
		for i in range (constants.GRID_SIZE[1]):
			self.grid[0][i] = constants.CONQUERED
			self.grid[constants.GRID_SIZE[0]-1][i] = constants.CONQUERED

		while not doneRunning:
			#handle player input
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == constants.KEY_q:
						sys.exit()
						return constants.UNDEFINED
					else:
						self._hero.update(event.key, True)
				if event.type == pygame.KEYUP:
					self._hero.update(event.key, False)

			#update game physics
			minimum = 500-int(96000/(4*(time.clock() - timeStart) + 120))
			n = int((minimum+300)/100)
			if n > self.numberBalls:
				self._ball.append(level_Ball())
				self.numberBalls = n

			self._hero.update(0, False)
			for i in range(self.numberBalls):
				if self._ball[i].update(self.grid) == constants.LOSE:
					return constants.LOSE
				cont += self._ball[i].destructedBlocks

			#draw ball
			for i in range(self.numberBalls):
				pygame.draw.circle(screen, constants.BLUE, [self._ball[i].pos.x + constants.BALL_RADIUS, self._ball[i].pos.y + constants.BALL_RADIUS], constants.BALL_RADIUS)
				
			#calculates what parts of the image needs to be redone
			objectErase = [] 
			_heroPos = vector2.Vector2(int(round(self._hero.pos.x/constants.SCALE[0])), int(round(self._hero.pos.y/constants.SCALE[1])))
			for i in [-1, 0, 1]:
				for j in [-1, 0, 1]:
					if _heroPos.x+i<0 or _heroPos.x+i>=constants.GRID_SIZE[0] or _heroPos.y+j<0 or _heroPos.y+j>=constants.GRID_SIZE[1]:
						continue
					r = Rect((_heroPos.x+i)*constants.SCALE[0], (_heroPos.y+j)*constants.SCALE[1], constants.SCALE[0], constants.SCALE[1])
					objectErase.append(r)
					color = self.getColor(self.grid[(_heroPos.x+i)][_heroPos.y+j])
					pygame.draw.rect(screen, color, r)

			for balls in self._ball: 
				_ballPos = vector2.Vector2(int(round(balls.pos.x/constants.SCALE[0])), int(round(balls.pos.y/constants.SCALE[1])))
				for i in [-1, 0, 1]:
					for j in [-1, 0, 1]:
						if _ballPos.x+i<0 or _ballPos.x+i>=constants.GRID_SIZE[0] or _ballPos.y+j<0 or _ballPos.y+j>=constants.GRID_SIZE[1]:
							continue
						color = self.getColor(self.grid[(_ballPos.x+i)][_ballPos.y+j])
						if color != constants.WHITE:
							continue
						r = Rect((_ballPos.x+i)*constants.SCALE[0], (_ballPos.y+j)*constants.SCALE[1], constants.SCALE[0], constants.SCALE[1])
						objectErase.append(r)
						pygame.draw.rect(screen, color, r)

			#update grid 
			_heroPos = vector2.Vector2(int(round(self._hero.pos.x/constants.SCALE[0])), int(round(self._hero.pos.y/constants.SCALE[1])))
			if self.grid[_heroPos.x][_heroPos.y] == constants.CONQUERED:
				if conquering:
					# s_conquered.play()
					conquering = False
					repint = True
					for y in range(constants.GRID_SIZE[1]):
						for x in range(constants.GRID_SIZE[0]):
							if self.grid[x][y] == constants.NOTHING:
								self.grid[x][y] = constants.HYPER
							elif self.grid[x][y] == constants.PROCESS:
								self.grid[x][y] = constants.CONQUERED
								cont += 1
								score += 1
					for i in range(self.numberBalls):
						self.DFS(int(round(self._ball[i].pos.x/constants.SCALE[0])), int(round(self._ball[i].pos.y/constants.SCALE[1])))
			else:
				conquering = True
				# if self.grid[_heroPos.x][_heroPos.y] != constants.PROCESS:
				# 	s_conquering.play()
				self.grid[_heroPos.x][_heroPos.y] = constants.PROCESS
			
			#draw grid
			if repint:
				repint = False
				for x in range(constants.GRID_SIZE[0]):
					for y in range(constants.GRID_SIZE[1]):
						_color = constants.WHITE
						if self.grid[x][y] == constants.CONQUERED:
							_color = constants.GREEN
						elif self.grid[x][y] == constants.HYPER:
							_color = constants.GREEN
							cont += 1
							score += 1
							self.grid[x][y] = constants.CONQUERED
						pygame.draw.rect(screen, _color, [x*constants.SCALE[0], y*constants.SCALE[1], constants.SCALE[0], constants.SCALE[1]])
				pygame.display.flip()
			
			#win condition
			if cont <= minimum:
				print("YOU LOST :( ")
				return constants.LOSE

			#draw hero
			objectErase.append(Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCALE[1]))
			pygame.draw.rect(screen, constants.GREEN, [0, 0, constants.SCREEN_SIZE[0], constants.SCALE[1]])
			pygame.draw.rect(screen, constants.RED, [self._hero.pos.x, self._hero.pos.y, constants.HERO_SIZE[0], constants.HERO_SIZE[1]])

			#draw ball
			for i in range(self.numberBalls):
				pygame.draw.circle(screen, constants.BLUE, [self._ball[i].pos.x + constants.BALL_RADIUS, self._ball[i].pos.y + constants.BALL_RADIUS], constants.BALL_RADIUS)

			#Score
			font = pygame.font.SysFont('Calibri', 25, True, False)
			text = font.render("Left: {}  Minimum: {}  Score: {}".format(cont, minimum, score), True, constants.BLACK)
			screen.blit(text, [0, 0])


			pygame.display.update(objectErase)
	
			clock.tick(100)