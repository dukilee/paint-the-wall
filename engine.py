import ball
import time
import constants
import hero
import menu
import pygame
import vector2
import sys
import data
import theme

from pygame.locals import *

class Engine:

	def __init__(self):
		self._hero = hero.Hero() 
		self._ball = []		
		self.cont = 500
		self.numberBalls = 1
		self.dx = (1, -1, 0, 0)
		self.dy = (0, 0, 1, -1)
		self.grid = [[constants.NOTHING for i in range(constants.GRID_SIZE[0])] for j in range (constants.GRID_SIZE[1])]

		self.timerMax = -1
		self.numberRegions = 1
		self.ballsKilled = 0
		self.oldBallsKilled = 0
		self.numberMovements = 0
		self.numberMovementsMax = -1
		self.newBlocksConquered = 0

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
			return theme.procColor
		if n == constants.CONQUERED:
			return theme.conqColor
		if n == constants.HYPER:
			return theme.conqColor
		return theme.freeColor

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
					return repint, constants.QUIT
				
				if event.type == pygame.KEYDOWN:

					if event.key == constants.keys['q']:
						return repint, constants.UNDEFINED


					elif event.key == constants.keys['p']:
						_menu = menu.PauseMenu()
						screen.fill(constants.WHITE)
						action = _menu.update(screen, self.getInstructions())
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
		for b in self._ball:
			if b.update(self.grid) == constants.LOSE:
				return constants.LOSE
		return None

	def updateGrid(self):
		self.newBlocksConquered = 0
		_heroPos = vector2.Vector2(int(round(self._hero.pos.x/constants.SCALE[0])), int(round(self._hero.pos.y/constants.SCALE[1])))
		if self.grid[_heroPos.x][_heroPos.y] == constants.CONQUERED:
			if self.conquering:
				self.numberMovements += 1
				# s_conquered.play()
				self.conquering = False
				self.repint = True
				for y in range(constants.GRID_SIZE[1]):
					for x in range(constants.GRID_SIZE[0]):
						if self.grid[x][y] == constants.NOTHING:
							self.grid[x][y] = constants.SHYPER
						elif self.grid[x][y] == constants.PROCESS:
							self.grid[x][y] = constants.CONQUERED
							self.newBlocksConquered += 1
				self.numberRegions = 0
				for b in self._ball:
					b.area = self.DFS(int(round(b.pos.x/constants.SCALE[0])), int(round(b.pos.y/constants.SCALE[1])))
					if b.area > 4 and self.grid[int(round(b.pos.x/constants.SCALE[0]))][int(round(b.pos.y/constants.SCALE[1]))] == constants.HYPER:
						self.numberRegions += 1
				done = False
				while not done:
					done = True
					for b in self._ball:
						if b.area<constants.PRISION_AREA and self.grid[int(round(b.pos.x/constants.SCALE[0]))][int(round(b.pos.y/constants.SCALE[1]))]!=constants.NOTHING:
							self.numberRegions -= 1
							self.numberBalls -= 1
							self.ballsKilled += 1
							self.newBlocksConquered += self.DFS_PAINT(int(round(b.pos.x/constants.SCALE[0])), int(round(b.pos.y/constants.SCALE[1])))
							self._ball.remove(b)
							done = False
							print("You are going down baby, restarting");
							break

		else:
			self.conquering = True
			self.grid[_heroPos.x][_heroPos.y] = constants.PROCESS

	def drawGrid(self, screen):
		for x in range(constants.GRID_SIZE[0]):
			for y in range(constants.GRID_SIZE[1]):
				_color = theme.freeColor
				if self.grid[x][y] == constants.CONQUERED:
					_color = theme.conqColor
				elif self.grid[x][y] == constants.SHYPER:
					_color = theme.conqColor
					self.newBlocksConquered += 1
					self.grid[x][y] = constants.CONQUERED
				elif self.grid[x][y] == constants.HYPER:
					self.grid[x][y] = constants.NOTHING
				pygame.draw.rect(screen, _color, [x*constants.SCALE[0], y*constants.SCALE[1], constants.SCALE[0], constants.SCALE[1]])
		pygame.display.flip()

	def winCondition(self):
		return self.cont <= self.minimum

	def draw(self, screen):
		

		self.objectErase.append(Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCALE[1]))
		pygame.draw.rect(screen, theme.heroColor, [self._hero.pos.x, self._hero.pos.y, constants.HERO_SIZE[0], constants.HERO_SIZE[1]])

		#draw ball
		for i in range(self.numberBalls):
			pygame.draw.circle(screen, theme.ballColor, [self._ball[i].pos.x + constants.BALL_RADIUS, self._ball[i].pos.y + constants.BALL_RADIUS], constants.BALL_RADIUS)

		#Score
		font = pygame.font.SysFont('Calibri', 25, True, False)
		text = font.render("Left: {}  Minimum: {}  Score: {}".format(self.cont, self.minimum, self.score), True, constants.BLACK)
		screen.blit(text, [0, 0])
		
		
		pygame.display.update(self.objectErase)

	def achievementsCondition(self):
		if self.ballsKilled - self.oldBallsKilled > 1:
			print('New Achievement: Double Kill')
			data.i['doubleKill'] = 1
		if self.numberMovements == 1 and self.ballsKilled > 0:
			print('New Achievement: Yoga Master')
			data.i['yogaMaster'] = 1
		if self.cont + self.newBlocksConquered >= (constants.GRID_SIZE[0]-2)*(constants.GRID_SIZE[1]-2):
			print('New Achievement: World Emperor')
			data.i['worldEmperor'] = 1
		self.oldBallsKilled = self.ballsKilled

	def createObjects(self):
		pass

	def stageDifferences(self, screen):
		pass

	def initialSettings(self):
		pass

	def getInstructions(self, screen):
		pass

	#Functions to check some missions
	def timer(self, screen):
		if time.clock() - self.timeStart > self.timerMax:
			return constants.LOSE
		font = pygame.font.SysFont('Calibri', 25, True, False)
		text = font.render("{}".format(int(self.timerMax - time.clock() + self.timeStart)), True, constants.BLACK)
		screen.blit(text, [750, 0])
		return None

	def movesLeft(self, screen):
		if self.numberMovements > self.numberMovementsMax:
			return constants.LOSE
		font = pygame.font.SysFont('Calibri', 25, True, False)
		text = font.render("Movements Left:{}".format(int(self.numberMovementsMax - self.numberMovements)), True, constants.BLACK)
		screen.blit(text, [600, 0])
		return None


	def run(self, screen):
		self._ball = []
		self.conquering = False #true if there is any process block
		self.repint = True #true when the whole screen needs to be redrawn
		self.objectErase = [] #marks the position of everything that surrounds objects(balls or hero)
		self.cont = 0
		self.minimum = -1
		self.score = 0
		self.createObjects()

		self.initialSettings()
		self.initGrid()
		# self.updateGrid()
		self.drawGrid(screen)
	

		pygame.init()
		doneRunning = False
		clock = pygame.time.Clock()


		#startMenu
		screen.fill(constants.WHITE)
		_menu = menu.StartMenu()
		# self.writeInstructions(screen)
		action = _menu.update(screen, self.getInstructions())
		if action == constants.MAIN_MENU:
			return constants.MAIN_MENU

		# s_conquering = pygame.mixer.Sound('sounds/s_coin.wav')
		# s_conquered = pygame.mixer.Sound('sounds/s_up.wav')

		self.timeStart = time.clock()
		while not doneRunning:
			self.objectErase = [] 
			pygame.draw.rect(screen, theme.conqColor, [0, 0, constants.SCREEN_SIZE[0], constants.SCALE[1]])
		
			#handle player input(
			aux = time.clock() - self.timeStart
			self.repint, check = self.checkInput(self.repint, screen)
			if check !=None:
				return check
			# self.timeStart = time.clock() - aux

			#update game physics
			self.stageDifferences(screen)
			if self.timerMax > 0:
				lose = self.timer(screen)
				if lose != None:
					return lose
			if self.numberMovementsMax > 0:
				lose = self.movesLeft(screen)
				if lose != None:
					return lose
			lose = self.updateObjects()
			if lose != None:
				data.i['deaths'] += 1
				return lose

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
						if color != theme.freeColor:
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
			self.achievementsCondition()
			if self.winCondition():
				return constants.WIN

			#update score
			if self.newBlocksConquered > 0:
				self.cont += self.newBlocksConquered
				self.score += self.newBlocksConquered
				
			self.draw(screen)

			clock.tick(100)

	def __del__(self):
		data.i['ballsDestructed'] += self.ballsKilled
		data.i['blocksConquered'] += self.cont + self.newBlocksConquered