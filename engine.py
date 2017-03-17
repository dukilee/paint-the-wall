import ball
import time
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
		self.grid = [[constants.NOTHING for i in range(constants.GRID_SIZE[0])] for j in range (constants.GRID_SIZE[1])]

		self.timerMax = -1
		self.numberRegions = 1
		self.ballsKilled = 0
		self.numberMovements = 0

	def valid(self, x, y):
		return x >= 0 and x < len(self.grid) and y >= 0 and y < len(self.grid[x])

	def DFS(self, startx, starty):
		stack = []
		aux = [startx, starty]
		stack.append(aux)
		area = 0

		val = self.grid[startx][starty]
		if val == constants.NOTHING:
			return 0

		while not stack == []:
			aux = stack.pop()
			area += 1
			for i in range(4):
				nx = aux[0] + self.dx[i]
				ny = aux[1] + self.dy[i]
				if self.valid(nx, ny) and self.grid[nx][ny] == val:
					self.grid[nx][ny] -= 1
					stack.append([nx, ny])
		return area

	def DFS_PAINT(self, startx, starty):
		stack = []
		aux = [startx, starty]
		stack.append(aux)
		area = 0

		while not stack == []:
			aux = stack.pop()
			area += 1
			for i in range(4):
				nx = aux[0] + self.dx[i]
				ny = aux[1] + self.dy[i]
				if self.valid(nx, ny) and self.grid[nx][ny] != constants.CONQUERED:
					self.grid[nx][ny] = constants.CONQUERED
					stack.append([nx, ny])
		return area

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

	def updateGrid(self):
		_heroPos = vector2.Vector2(int(round(self._hero.pos.x/constants.SCALE[0])), int(round(self._hero.pos.y/constants.SCALE[1])))
		if self.grid[_heroPos.x][_heroPos.y] == constants.CONQUERED:
			self.numberMovements += 1
			if self.conquering:
				# s_conquered.play()
				self.conquering = False
				self.repint = True
				for y in range(constants.GRID_SIZE[1]):
					for x in range(constants.GRID_SIZE[0]):
						if self.grid[x][y] == constants.NOTHING:
							self.grid[x][y] = constants.SHYPER
						elif self.grid[x][y] == constants.PROCESS:
							self.grid[x][y] = constants.CONQUERED
							self.cont += 1
							self.score += 1
				self.numberRegions = 0
				for b in self._ball:
					b.area = self.DFS(int(round(b.pos.x/constants.SCALE[0])), int(round(b.pos.y/constants.SCALE[1])))
					if b.area > 4 and self.grid[int(round(b.pos.x/constants.SCALE[0]))][int(round(b.pos.y/constants.SCALE[1]))] == constants.HYPER:
						self.numberRegions += 1
				for b in self._ball:
					if b.area<constants.PRISION_AREA and self.grid[int(round(b.pos.x/constants.SCALE[0]))][int(round(b.pos.y/constants.SCALE[1]))]!=constants.NOTHING:
						self.numberRegions -= 1
						self.numberBalls -= 1
						self.ballsKilled += 1
						self.cont += self.DFS_PAINT(int(round(b.pos.x/constants.SCALE[0])), int(round(b.pos.y/constants.SCALE[1])))
						self._ball.remove(b)
						print("You are going down baby");
		else:
			self.conquering = True
			self.grid[_heroPos.x][_heroPos.y] = constants.PROCESS

	def drawGrid(self, screen):
		for x in range(constants.GRID_SIZE[0]):
			for y in range(constants.GRID_SIZE[1]):
				_color = constants.WHITE
				if self.grid[x][y] == constants.CONQUERED:
					_color = constants.GREEN
				elif self.grid[x][y] == constants.SHYPER:
					_color = constants.GREEN
					self.cont += 1
					self.score += 1
					self.grid[x][y] = constants.CONQUERED
				elif self.grid[x][y] == constants.HYPER:
					self.grid[x][y] = constants.NOTHING
				pygame.draw.rect(screen, _color, [x*constants.SCALE[0], y*constants.SCALE[1], constants.SCALE[0], constants.SCALE[1]])
		pygame.display.flip()

	def winCondition(self):
		return self.cont <= self.minimum

	def draw(self, screen):
		

		self.objectErase.append(Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCALE[1]))
		pygame.draw.rect(screen, constants.RED, [self._hero.pos.x, self._hero.pos.y, constants.HERO_SIZE[0], constants.HERO_SIZE[1]])

		#draw ball
		for i in range(self.numberBalls):
			pygame.draw.circle(screen, constants.BLUE, [self._ball[i].pos.x + constants.BALL_RADIUS, self._ball[i].pos.y + constants.BALL_RADIUS], constants.BALL_RADIUS)

		#Score
		font = pygame.font.SysFont('Calibri', 25, True, False)
		text = font.render("Left: {}  Minimum: {}  Score: {}".format(self.cont, self.minimum, self.score), True, constants.BLACK)
		screen.blit(text, [0, 0])
		
		
		pygame.display.update(self.objectErase)

	def createObjects(self):
		pass

	def stageDifferences(self):
		pass

	def initialSettings(self):
		pass

	#Functions to check some missions
	def timer(self, screen):
		if time.clock() - self.timeStart > self.timerMax:
			return constants.LOSE
		font = pygame.font.SysFont('Calibri', 25, True, False)
		text = font.render("{}".format(int(self.timerMax - time.clock() + self.timeStart)), True, constants.BLACK)
		screen.blit(text, [750, 0])
		return None


	def run(self, screen):
		self._ball = []
		self.conquering = False #true if there is any process block
		self.repint = True #true when the whole screen needs to be redrawn
		self.objectErase = [] #marks the position of everything that surrounds objects(balls or hero)
		self.cont = 0
		self.minimum = -1
		self.score = 0
		self.timeStart = time.clock()
		self.createObjects()

		self.initialSettings()


		pygame.init()
		doneRunning = False
		clock = pygame.time.Clock()

		# s_conquering = pygame.mixer.Sound('sounds/s_coin.wav')
		# s_conquered = pygame.mixer.Sound('sounds/s_up.wav')

		self.initGrid()
		while not doneRunning:
			self.objectErase = [] 
			pygame.draw.rect(screen, constants.GREEN, [0, 0, constants.SCREEN_SIZE[0], constants.SCALE[1]])
		
			#handle player input
			self.repint, check = self.checkInput(self.repint, screen)
			if check !=None:
				return check

			#update game physics
			self.stageDifferences()
			if self.timerMax > 0:
				lose = self.timer(screen)
				if lose != None:
					return lose

			lose = self.updateObjects()
			if lose != None:
				return lose

			#draw ball
			for b in self._ball:
				pygame.draw.circle(screen, constants.BLUE, [b.pos.x + constants.BALL_RADIUS, b.pos.y + constants.BALL_RADIUS], constants.BALL_RADIUS)
			
			#calculates what parts of the image needs to be redone
			_heroPos = vector2.Vector2(int(round(self._hero.pos.x/constants.SCALE[0])), int(round(self._hero.pos.y/constants.SCALE[1])))
			for i in [-1, 0, 1]:
				for j in [-1, 0, 1]:
					if _heroPos.x+i<0 or _heroPos.x+i>=constants.GRID_SIZE[0] or _heroPos.y+j<0 or _heroPos.y+j>=constants.GRID_SIZE[1]:
						continue
					r = Rect((_heroPos.x+i)*constants.SCALE[0], (_heroPos.y+j)*constants.SCALE[1], constants.SCALE[0], constants.SCALE[1])
					self.objectErase.append(r)
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
						self.objectErase.append(r)
						pygame.draw.rect(screen, color, r)

			#update grid 
			self.updateGrid()

			#draw grid
			if self.repint:
				self.repint = False
				self.drawGrid(screen)

			#win condition
			if self.winCondition():
				return constants.WIN

			self.draw(screen)

			clock.tick(100)