import pygame
import time

from actors import hero
from audiovisual import theme, themeManager
from main import menu
from pygame.locals import *
from resources import constants, tools
from user_data import data, dataManager
from user_data import soundManager

class Engine:
	def __init__(self):
		"""
		Instantiates every object and give their initial values.
		"""
		self.pause_time=0.0
		self._hero = hero.Hero() #the player
		self._ball = []	#the enemies
		self.cont = 0 #blocks that remains conquered on screen
		self.numberBalls = 1 #number of initial enemies on screen
		self.grid = [[constants.NOTHING for i in range(constants.GRID_SIZE[0])] for j in range (constants.GRID_SIZE[1])]

		self.action = constants.STAGE_MENU #where to go when quitting
		self.timerMax = -1
		self.numberRegions = 1 #num of regions the screen is split
		self.ballsKilled = 0    #used to check how many balls ..
		self.oldBallsKilled = 0 #were killed at once
		self.numberMovements = 0 #number of movements made by the player
		self.numberMovementsMax = -1
		self.newBlocksConquered = 0

	def DFS(self, startx, starty, mode = False):
		"""
		depth first search, to paint new conquered perimeter
		:param startx: horizontal position where the dfs starts
		:param starty: vertical position where the dfs starts
		:param mode: True - painting the screen; False - looking for HYPER blocks
		:return: the quantity of new blocks conquered
		"""

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
				nx = aux[0] + constants.dx[i]
				ny = aux[1] + constants.dy[i]
				if tools.valid(nx, ny, self.grid) and self.grid[nx][ny] == val:
					if not mode:
						self.grid[nx][ny] -= 1
					else:
						self.grid[nx][ny] = constants.CONQUERED	
					stack.append([nx, ny])
		return area

	#get grid color represented by 'n'
	def getColor(self, n):
		"""
		Given the condition of a block (PROCESS, CONQUERED, HYPER, FREE), returns the color it should
		be painted.
		:param n: Current condition of a block
		:return: Color of the block
		"""
		if n == constants.PROCESS:
			return theme.procColor
		if n == constants.CONQUERED:
			return theme.conqColor
		if n == constants.HYPER:
			return theme.conqColor
		return theme.freeColor

	def initGrid(self):
		"""
		Initial game state, initialize grid
		"""
		for i in range (constants.GRID_SIZE[0]):
			self.grid[i][0] = constants.CONQUERED
			self.grid[i][constants.GRID_SIZE[1]-1] = constants.CONQUERED
		
		for i in range (constants.GRID_SIZE[1]):
			self.grid[0][i] = constants.CONQUERED
			self.grid[constants.GRID_SIZE[0]-1][i] = constants.CONQUERED		

	def checkInput(self, repint, screen):
		startpause = time.clock()
		"""
		Handles player inputs. Get the pressed keys and execute the corresponding action
		:param repint: if true, repints the whole screen
		:param screen: game screen, comes from pygame
		:return: repint, next action of the game
		"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return repint, constants.QUIT
			#if key pressed ...
			if event.type == pygame.KEYUP:
				#exit to previous menu
				if event.key == constants.keys['q']:
					return repint, self.action
				#pause
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
					self._hero.update(event.key, False)
			if event.type == pygame.KEYDOWN:
				self._hero.update(event.key, True)
		endpause=time.clock()
		if endpause-startpause>=1:
			self.pause_time=self.pause_time+endpause-startpause

		return repint, None

	#update hero and balls positions, also checks if any ball hitted the player path
	def updateObjects(self):
		"""
		Update the position of the balls and of the hero
		:return: returns if the players has lost or not the game
		"""
		self._hero.update(0, False)
		for b in self._ball:
			if b.update(self.grid) == constants.LOSE:
				return constants.LOSE
		return None

	#update new paintings!
	def updateGrid(self):
		"""
		After the hero moved, there is a possibility that he conquered more of the screen. This
		function updates the current game state.
		"""
		self.newBlocksConquered = 0
		
		#if a perimeter was closed ...
		if self.grid[self._hero.pos.Dx()][self._hero.pos.Dy()] == constants.CONQUERED:
			#if it happened when hero was conquering area ...
			if self.conquering:
				self.numberMovements += 1
				soundManager.play_music('conquered', 1.0, 0)
				self.conquering = False #end of conquering
				self.repint = True #screen need to be entirely updated
				
				#prepare grid
				for y in range(constants.GRID_SIZE[1]):
					for x in range(constants.GRID_SIZE[0]):
						if self.grid[x][y] == constants.NOTHING:
							self.grid[x][y] = constants.SHYPER #prepares area to be painted
						elif self.grid[x][y] == constants.PROCESS:
							self.grid[x][y] = constants.CONQUERED #paint perimeter
							self.newBlocksConquered += 1

				#counts the number of regions the screen is splitted
				self.numberRegions = 0
				for b in self._ball: 
					b.area = self.DFS(b.pos.Dx(), b.pos.Dy()) #changes SHYPER to HYPER
					if b.area > 4 and self.grid[b.pos.Dx()][b.pos.Dy()] == constants.HYPER:
						self.numberRegions += 1 #each HYPER count as a region

				#paint the regions smaller than PRISION_AREA
				done = False
				while not done:
					done = True
					for b in self._ball:
						if b.area < constants.PRISION_AREA and self.grid[b.pos.Dx()][b.pos.Dy()] != constants.NOTHING:
							self.numberRegions -= 1
							self.numberBalls -= 1
							self.ballsKilled += 1
							self.newBlocksConquered += self.DFS(b.pos.Dx(), b.pos.Dy(), True)
							self._ball.remove(b)
							done = False
							break
		
		else:
			#continues to conquer
			self.conquering = True
			if self.grid[self._hero.pos.Dx()][self._hero.pos.Dy()] == constants.NOTHING:
				soundManager.play_music('conquering', 1.0, 0)

			self.grid[self._hero.pos.Dx()][self._hero.pos.Dy()] = constants.PROCESS
			
	#paint the wall!
	def drawGrid(self, screen):
		"""
		draws the whole screen again
		:param screen: game screen, comes from pygame
		"""
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
		"""
		checks if the player won the game
		:return: true if the player won, false otherwise
		"""
		return self.cont <= self.minimum

	#draw hero and balls on screen
	def draw(self, screen):
		"""
		draws hero, balls and writes the time, score
		:param screen: game screen, comes from pygame
		"""
		self.objectErase.append(constants.SCR)
		
		#draw hero
		screen.blit(self._hero.sprite.img, [self._hero.pos.x, self._hero.pos.y])

		#draw ball
		for b in self._ball:
			screen.blit(b.sprite.img, [b.pos.x+3, b.pos.y+2])

		#Score
		font = pygame.font.SysFont('Calibri', 18, True, False)
		text = font.render("Left: {}  Minimum: {}  Score: {}".format(self.cont, self.minimum, self.score), True, theme.text_color)
		screen.blit(text, [0, 0])
		
		pygame.display.update(self.objectErase)

	def achievementsCondition(self):
		"""
		Checks if the player did something worth an achievement. If he did, then updates the data
		:return: a list of the achievements unlocked by the player
		"""
		new_achievement = []

		if not data.i['doubleKill'] == 1 and self.ballsKilled - self.oldBallsKilled > 1:
			data.i['doubleKill'] = 1
			new_achievement.append('doubleKill')
	
		if not data.i['yogaMaster'] == 1 and self.numberMovements == 1 and self.ballsKilled > 0:
			data.i['yogaMaster'] = 1
			new_achievement.append('yogaMaster')

		if not data.i['worldEmperor'] == 1 and self.cont + self.newBlocksConquered >= (constants.GRID_SIZE[0] - 2) * (constants.GRID_SIZE[1] - 2):
			data.i['worldEmperor'] = 1
			new_achievement.append('worldEmperor')

		self.oldBallsKilled = self.ballsKilled

		return new_achievement

	def createObjects(self):
		"""Instantiates the balls"""
		pass

	def stageDifferences(self, screen):
		"""
		Allows the stage to draw on the screen
		:param screen: game screen, comes from pygame
		"""
		pass

	def initialSettings(self):
		"""Sets initial values to variables"""
		pass

	def getInstructions(self):
		""":return: string with the info of what the player needs to do."""
		pass

	def timer(self, screen):
		"""
		Checks if there's still time left, and if there is updates the counter text
		:param screen: game screen, comes from pygame
		:return: returns if the player has lost the game
		"""
		if data.getActualTime() - self.timeStart > self.timerMax:
			return constants.LOSE

		font = pygame.font.SysFont('Calibri', 18, True, False)
		text = font.render("{}".format(int(self.timerMax - data.getActualTime() + self.timeStart+self.pause_time)), True, theme.text_color)
		screen.blit(text, [750, 0])

		return None

	def movesLeft(self, screen):
		"""
		Check if there's still movements left
		:param screen: game screen, comes from pygame
		:return: returns if the player has lost the game
		"""
		if self.numberMovements > self.numberMovementsMax:
			return constants.LOSE

		font = pygame.font.SysFont('Calibri', 18, True, False)
		text = font.render("Movements Left:{}".format(int(self.numberMovementsMax - self.numberMovements)), True, theme.text_color)
		screen.blit(text, [600, 0])

		return None

	#show achievements
	def achieve_advisor(self, screen, achieve):
		"""
		Prints a message on the screen if the player unlocked a new achievement
		:param screen: game screen, comes from pygame
		:param achieve: name of the achievement
		"""
		screen.fill(theme.conqColor, [200, 585, 400, 30])
		font = pygame.font.SysFont('Calibri', 18, True, False)
		text = font.render('New Achievement Unlocked! - ' + achieve, True, theme.text_color)
		screen.blit(text, [250, 584])

	def run(self, screen):
		"""
		Main loop of the game
		:param screen: game screen, comes from pygame
		:return: returns if the player won or lost the current stage
		"""
		self.conquering = False #true if there is any process block
		self.repint = True #true when the whole screen needs to be redrawn
		self.objectErase = [] #marks the position of everything that surrounds objects (balls or hero)
		self.minimum = -1
		self.score = 0
		data.new_score = 0
		achievements = []

		self.createObjects()
		self.initialSettings()
		self.initGrid()
		self.drawGrid(screen)

		doneRunning = False
		clock = pygame.time.Clock()

		#startMenu
		screen.fill(constants.WHITE)
		_menu = menu.StartMenu(self.action)
		action = _menu.update(screen, self.getInstructions())
		if action == self.action:
			return self.action

		self.timeStart = data.getActualTime()
		achieve_timer = self.timeStart
		while not doneRunning:
			self.objectErase = [] 
			pygame.draw.rect(screen, theme.conqColor, [0, 0, constants.SCREEN_SIZE[0], constants.SCALE[1]])
		
			#handle player input
			self.repint, check = self.checkInput(self.repint, screen)
			if check != None:
				return check
		
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

			#checks if any achievement is unlocked
			new_achievements = self.achievementsCondition()
			if len(new_achievements) > 0:
				achievements += new_achievements
				achieve_timer = data.getActualTime()

			#if able, show achievment on screen
			if len(achievements) > 0:
				if data.getActualTime() <= achieve_timer + constants.ACHIEVE_DURATION:
					self.achieve_advisor(screen, achievements[0])
				else:
					achievements.pop(0)
					screen.fill(theme.conqColor, [200, 585, 400, 30])
					if len(achievements) > 0:
						achieve_timer = data.getActualTime()

			#win condition
			if self.winCondition():
				return constants.WIN

			#update score
			if self.newBlocksConquered > 0:
				self.cont += self.newBlocksConquered
				self.score += self.newBlocksConquered//2
				data.new_score += self.newBlocksConquered//2

			#take time into account for score! <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
			self.draw(screen)
			clock.tick(100)

	#update data
	def __del__(self):
		data.i['ballsDestructed'] += self.ballsKilled
		data.i['blocksConquered'] += self.cont + self.newBlocksConquered

def set_environment():
	"""
	Responsible for setting game caption and title
	"""
	pygame.init()
	pygame.key.set_repeat(1, 200)  # turn on "repeat" functionality of keyboard
	pygame.display.set_caption('paintTheWall', 'The Game')  # game title

	dManager = dataManager.DataManager()  # recover data from last game
	data.startTime = data.getActualTime() - data.i['timePlayed']
	themeManager.changeTheme(data.i['theme'])  # loads theme

	return pygame.display.set_mode(constants.SCREEN_SIZE), dManager, menu.MainMenu(constants.QUIT)
