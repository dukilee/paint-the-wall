import ball
import constants
import grid
import hero
import menu
import pygame
import vector2
import sys
import tools

from pygame.locals import *

class Engine:
	def __init__(self, nballs):
		self._hero = hero.Hero() 
		self._ball = [ball.Ball() for i in range(nballs)]		
		self.cont = 500
		self.numberBalls = nballs
		self.dx = (1, -1, 0, 0)
		self.dy = (0, 0, 1, -1)
		self.grid = [[0 for i in range(constants.GRID_SIZE[0])] for j in range (constants.GRID_SIZE[1])]

	def valid(self, x, y):
		return x >= 0 and x < len(self.grid) and y >= 0 and y < len(self.grid[x])

	def DFS(self, startx, starty):
		stack = []
		aux = [startx, starty]
		stack.append(aux)
		while not stack == []:
			aux = stack.pop()
			for i in range(4):
				nx = aux[0] + self.dx[i]
				ny = aux[1] + self.dy[i]
				if self.valid(nx, ny) and self.grid[nx][ny] == constants.HYPER:
					self.grid[nx][ny] = constants.NOTHING
					stack.append([nx, ny])

	def getColor(self, n):
		if n == constants.PROCESS:
			return constants.LIGHT_GREEN
		if n == constants.CONQUERED:
			return constants.GREEN
		if n == constants.HYPER:
			return constants.GREEN
		return constants.WHITE

	def initGrid(self):
		for i in range (constants.GRID_SIZE[0]):
			self.grid[i][0] = constants.CONQUERED
			self.grid[i][constants.GRID_SIZE[1]-1] = constants.CONQUERED
		
		for i in range (constants.GRID_SIZE[1]):
			self.grid[0][i] = constants.CONQUERED
			self.grid[constants.GRID_SIZE[0]-1][i] = constants.CONQUERED		

	def checkInput(self, repint, screen):
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				
				if event.type == pygame.KEYDOWN:
					if event.key == constants.KEY_q:
						return repint, constants.UNDEFINED


					elif event.key == constants.KEY_p:
						_menu = menu.PauseMenu()
						action = _menu.update(screen)
						if action == constants.MAIN_MENU:
							return repint, constants.MAIN_MENU
						elif action == constants.RESTART:
							return repint, constants.RESTART
						repint = True
					else:
						self._hero.update(event.key, True)

				if event.type == pygame.KEYUP:
					self._hero.update(event.key, False)

		return repint, None

	def updateObjects(self):
		self._hero.update(0, False)
		for i in range(self.numberBalls):
			if self._ball[i].update(self.grid) == constants.LOSE:
				return constants.LOSE
		return None

	def drawGrid(self, screen, contador):
		for x in range(constants.GRID_SIZE[0]):
			for y in range(constants.GRID_SIZE[1]):
				_color = constants.WHITE
				if self.grid[x][y] == constants.PROCESS:
					_color = constants.LIGHT_GREEN
				elif self.grid[x][y] == constants.CONQUERED:
					_color = constants.GREEN
					contador -= 1
				elif self.grid[x][y] == constants.HYPER:
					_color = constants.GREEN
					self.grid[x][y] = constants.CONQUERED
				pygame.draw.rect(screen, _color, [x * constants.SCALE[0], y * constants.SCALE[1], constants.SCALE[0], constants.SCALE[1]])
		pygame.display.flip()
		return contador

	def updateGrid(self):
		for y in range(constants.GRID_SIZE[1]):
			for x in range(constants.GRID_SIZE[0]):
				if self.grid[x][y] == constants.NOTHING:
					self.grid[x][y] = constants.HYPER
				elif self.grid[x][y] == constants.PROCESS:
					self.grid[x][y] = constants.CONQUERED		

	def run(self, screen):
		conquering = False #true if there is any process block
		repint = True #true when the whole screen needs to be redrawn
		objectErase = [] #marks the position of everything that surrounds objects(balls or hero)

		#for i in range(self.numberBalls):
		#	self._ball[i].pos.print()

		pygame.init()
		doneRunning = False
		clock = pygame.time.Clock()
		
		self.initGrid() # sets inital configuration of grid

		while not doneRunning:
			#handle player input
			repint, check = self.checkInput(repint, screen)
			if check != None:
				return check

			#update game physics (and checks if player lost the game)
			lose = self.updateObjects()
			if lose != None:
				return lose

			#draw ball
			for i in range(self.numberBalls):
				pygame.draw.circle(screen, constants.BLUE, [self._ball[i].pos.x + constants.BALL_RADIUS, self._ball[i].pos.y + constants.BALL_RADIUS], constants.BALL_RADIUS)
				
			#calculates what parts of the image needs to be redone
			objectErase = [] 
			_heroPos = vector2.Vector2(tools.conv(self._hero.pos.x, 0), tools.conv(self._hero.pos.y, 1))
			for i in [-1, 0, 1]:
				for j in [-1, 0, 1]:
					if not self.valid(_heroPos.x + i, _heroPos.y + j):
						continue
					r = Rect((_heroPos.x+i)*constants.SCALE[0], (_heroPos.y+j)*constants.SCALE[1], constants.SCALE[0], constants.SCALE[1])
					objectErase.append(r)
					color = self.getColor(self.grid[(_heroPos.x+i)][_heroPos.y+j])
					pygame.draw.rect(screen, color, r)

			for balls in self._ball: 
				_ballPos = vector2.Vector2(tools.conv(balls.pos.x, 0), tools.conv(balls.pos.y, 1))
				for i in [-1, 0, 1]:
					for j in [-1, 0, 1]:
						if not self.valid(_ballPos.x + i, _ballPos.y + j):
							continue
						color = self.getColor(self.grid[(_ballPos.x+i)][_ballPos.y+j])
						if color != constants.WHITE:
							continue
						r = Rect((_ballPos.x+i)*constants.SCALE[0], (_ballPos.y+j)*constants.SCALE[1], constants.SCALE[0], constants.SCALE[1])
						objectErase.append(r)
						pygame.draw.rect(screen, color, r)

			#update grid 
			_heroPos = vector2.Vector2(tools.conv(self._hero.pos.x, 0), tools.conv(self._hero.pos.y, 1))
			if self.grid[_heroPos.x][_heroPos.y] == constants.CONQUERED:
				if conquering:
					conquering = False
					repint = True
					self.updateGrid()
					for i in range(self.numberBalls):
						self.DFS(tools.conv(self._ball[i].pos.x, 0), tools.conv(self._ball[i].pos.y, 1))
			else:
				conquering = True
				self.grid[_heroPos.x][_heroPos.y] = constants.PROCESS
			
			contador = int(3 * constants.GRID_SIZE[0] * constants.GRID_SIZE[1]/4)

			#draw grid
			if repint:
				repint = False
				contador = self.drawGrid(screen, contador)

			#win condition
			if contador <= 0:
				return constants.WIN

			#draw hero
			pygame.draw.rect(screen, constants.RED, [self._hero.pos.x, self._hero.pos.y, constants.HERO_SIZE[0], constants.HERO_SIZE[1]])

			#draw ball
			for i in range(self.numberBalls):
				pygame.draw.circle(screen, constants.BLUE, [self._ball[i].pos.x + constants.BALL_RADIUS, self._ball[i].pos.y + constants.BALL_RADIUS], constants.BALL_RADIUS)

			#Score
			font = pygame.font.SysFont('Calibri', 25, True, False)
			text = font.render("Left: {}".format(contador), True, constants.BLACK)
			screen.blit(text, [0, 0])

			pygame.display.update(objectErase)	
			clock.tick(100)