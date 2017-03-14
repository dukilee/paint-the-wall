import constants
import pygame
import hero
import ball
import grid
import vector2
import sys
from pygame.locals import *

class Engine:
	def __init__(self):
		self._hero = hero.Hero() 
		self._ball = []
		self.cont = 500
		self.numberBalls = 1
		self.dx = (1, -1, 0, 0)
		self.dy = (0, 0, 1, -1)
		self.grid = [[0 for i in range(constants.GRID_SIZE[0])] for j in range (constants.GRID_SIZE[1])]

	def DFS(self, startx, starty):
		stack = []
		aux = [startx, starty]
		stack.append(aux)
		while not stack == []:
			aux = stack.pop()
			for i in range(4):
				nx = aux[0] + self.dx[i]
				ny = aux[1] + self.dy[i]
				if self.grid[nx][ny] == constants.HYPER:
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

	def run(self, screen):
		self._ball = []
		conquering = False #true if there is any process block
		repint = True#true when the hole screen needs to be redrawn
		objectErase = []#marks the position of everything that surrounds objects(balls or hero)
		for i in range(self.numberBalls):
			self._ball.append(ball.Ball(i))

		for i in range(self.numberBalls):
			self._ball[i].pos.print()

		pygame.init()
		doneRunning = False
		clock = pygame.time.Clock()

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
						doneRunning = True
					else:
						self._hero.update(event.key, True)
				if event.type == pygame.KEYUP:
					self._hero.update(event.key, False)

			#update game physics
			self._hero.update(0, False)
			for i in range(self.numberBalls):
				if self._ball[i].update(self.grid) == constants.LOSE:
					return constants.LOSE

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
					conquering = False
					repint = True
					for y in range(constants.GRID_SIZE[1]):
						for x in range(constants.GRID_SIZE[0]):
							if self.grid[x][y] == constants.NOTHING:
								self.grid[x][y] = constants.HYPER
							elif self.grid[x][y] == constants.PROCESS:
								self.grid[x][y] = constants.CONQUERED
					for i in range(self.numberBalls):
						self.DFS(int(round(self._ball[i].pos.x/constants.SCALE[0])), int(round(self._ball[i].pos.y/constants.SCALE[1])))
			else:
				conquering = True
				self.grid[_heroPos.x][_heroPos.y] = constants.PROCESS
			
			contador = int(3*constants.GRID_SIZE[0]*constants.GRID_SIZE[1]/4)			

			#draw grid
			if repint:
				repint = False
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
						pygame.draw.rect(screen, _color, [x*constants.SCALE[0], y*constants.SCALE[1], constants.SCALE[0], constants.SCALE[1]])
				pygame.display.flip()
			#win condition
			if contador <= 0:
				print("YOU WON :)")
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