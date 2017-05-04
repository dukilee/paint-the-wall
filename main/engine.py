import pygame

from actors import hero
from main import menu
from pygame.locals import *
from resources import constants, tools
from user_data import data, dataManager
from visual import theme, themeManager

def set_environment():
	pygame.init()
	pygame.key.set_repeat(1, 200) # turn on "repeat" functionality
	pygame.display.set_caption('paintTheWall', 'The Game')

	dManager = dataManager.DataManager()
	data.startTime = data.getActualTime() - data.i['timePlayed']
	themeManager.changeTheme(data.i['theme'])

	return pygame.display.set_mode(constants.SCREEN_SIZE), dManager, menu.MainMenu(constants.QUIT), pygame.mixer.music

class Engine:
	def __init__(self):
		self._hero = hero.Hero() 
		self._ball = []		
		self.cont = 500
		self.numberBalls = 1
		self.dx = (1, -1, 0, 0)
		self.dy = (0, 0, 1, -1)
		self.grid = [[constants.NOTHING for i in range(constants.GRID_SIZE[0])] for j in range (constants.GRID_SIZE[1])]

		self.action = constants.STAGE_MENU
		self.timerMax = -1
		self.numberRegions = 1
		self.ballsKilled = 0
		self.oldBallsKilled = 0
		self.numberMovements = 0
		self.numberMovementsMax = -1
		self.newBlocksConquered = 0

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
				if tools.valid(nx, ny, self.grid) and self.grid[nx][ny] == val:
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
				if tools.valid(nx, ny, self.grid) and self.grid[nx][ny] != constants.CONQUERED:
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
					return repint, self.action
				elif event.key == constants.keys['p']:
					_menu = menu.PauseMenu(self.action)
					screen.fill(constants.WHITE)
					action = _menu.update(screen, self.getInstructions())
					if action == self.action:
						return repint, self.action
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
		
		if self.grid[self._hero.pos.Dx()][self._hero.pos.Dy()] == constants.CONQUERED:
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
					b.area = self.DFS(b.pos.Dx(), b.pos.Dy())
					if b.area > 4 and self.grid[b.pos.Dx()][b.pos.Dy()] == constants.HYPER:
						self.numberRegions += 1
				done = False
				while not done:
					done = True
					for b in self._ball:
						if b.area < constants.PRISION_AREA and self.grid[b.pos.Dx()][b.pos.Dy()]!=constants.NOTHING:
							self.numberRegions -= 1
							self.numberBalls -= 1
							self.ballsKilled += 1
							self.newBlocksConquered += self.DFS_PAINT(b.pos.Dx(), b.pos.Dy())
							self._ball.remove(b)
							done = False
							break

		else:
			self.conquering = True
			self.grid[self._hero.pos.Dx()][self._hero.pos.Dy()] = constants.PROCESS

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
		self.objectErase.append(constants.SCR)
		
		#draw hero
		screen.blit(self._hero.sprite.img, [self._hero.pos.x, self._hero.pos.y])

		#draw ball
		for b in self._ball:
			screen.blit(b.sprite.img, [b.pos.x, b.pos.y])

		#Score
		font = pygame.font.SysFont('Calibri', 25, True, False)
		text = font.render("Left: {}  Minimum: {}  Score: {}".format(self.cont, self.minimum, self.score), True, constants.WHITE)
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

	def getInstructions(self):
		pass

	#Functions to check some missions
	def timer(self, screen):
		if data.getActualTime() - self.timeStart > self.timerMax:
			return constants.LOSE
		font = pygame.font.SysFont('Calibri', 25, True, False)
		text = font.render("{}".format(int(self.timerMax - data.getActualTime() + self.timeStart)), True, theme.text_color)
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
		data.new_score = 0

		self.initialSettings()
		self.initGrid()
		self.drawGrid(screen)

		doneRunning = False
		clock = pygame.time.Clock()

		#startMenu
		screen.fill(constants.WHITE)
		_menu = menu.StartMenu(self.action)
		# self.writeInstructions(screen)
		action = _menu.update(screen, self.getInstructions())
		if action == self.action:
			return self.action

		# s_conquering = pygame.mixer.Sound('sounds/s_coin.wav')
		# s_conquered = pygame.mixer.Sound('sounds/s_up.wav')

		self.timeStart = data.getActualTime()
		while not doneRunning:
			self.objectErase = [] 
			pygame.draw.rect(screen, theme.conqColor, [0, 0, constants.SCREEN_SIZE[0], constants.SCALE[1]])
		
			#handle player input
			self.repint, check = self.checkInput(self.repint, screen)
			if check != None:
				return check
			#self.timeStart = time.clock() - aux

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
			for i in [-1, 0, 1]:
				for j in [-1, 0, 1]:
					if not tools.valid(self._hero.pos.Dx() + i, self._hero.pos.Dy() + j, self.grid):
						continue
					r = Rect((self._hero.pos.Dx() + i) * constants.SCALE[0], (self._hero.pos.Dy() + j) * constants.SCALE[1], constants.SCALE[0], constants.SCALE[1])
					self.objectErase.append(r)
					color = self.getColor(self.grid[(self._hero.pos.Dx() + i)][self._hero.pos.Dy() + j])
					pygame.draw.rect(screen, color, r)

			for balls in self._ball:
				for i in [-1, 0, 1]:
					for j in [-1, 0, 1]:
						if not tools.valid(balls.pos.Dx(), balls.pos.Dy(), self.grid):
							continue
						color = self.getColor(self.grid[(balls.pos.Dx() + i)][balls.pos.Dy() + j])
						if color != theme.freeColor:
							continue
						r = Rect((balls.pos.Dx() + i) * constants.SCALE[0], (balls.pos.Dy() + j) * constants.SCALE[1], constants.SCALE[0], constants.SCALE[1])
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
				self.score += self.newBlocksConquered//2
				data.new_score += self.newBlocksConquered//2

			#take time into account for score!
			self.draw(screen)
			clock.tick(100)

	def __del__(self):
		data.i['ballsDestructed'] += self.ballsKilled
		data.i['blocksConquered'] += self.cont + self.newBlocksConquered	