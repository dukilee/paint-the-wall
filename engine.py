import constants
import pygame
import hero
import ball
import sys
from pygame.locals import *
class Engine:
	_hero = hero.Hero() 
	_ball = ball.Ball()
	cont = 500
	dx = (1, -1, 0, 0)
	dy = (0, 0, 1, -1)
	screen = pygame.display.set_mode(constants.SCREEN_SIZE) 
	screen.fill(constants.WHITE)	
	grid = [[0 for i in range(constants.GRID_SIZE[0])] for j in range (constants.GRID_SIZE[1])]

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


	def run(self):
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
				if event.type == pygame.KEYDOWN:
					if event.key == constants.KEY_q:
						doneRunning = True
					else:
						self._hero.update(event.key, True)
				if event.type == pygame.KEYUP:
					print("A tecla ", event.key, " foi solta")
					self._hero.update(event.key, False)
			self._hero.update(0, False)
			self._ball.update(self.grid)
			#update grid 
			_heroPos = [int(round(self._hero.pos[0]/constants.SCALE[0])), int(round(self._hero.pos[1]/constants.SCALE[1]))] 
			if self.grid[_heroPos[0]][_heroPos[1]] == constants.CONQUERED:
				for y in range(constants.GRID_SIZE[1]):
					for x in range(constants.GRID_SIZE[0]):
						if self.grid[x][y] == constants.NOTHING:
							self.grid[x][y] = constants.HYPER
						elif self.grid[x][y] == constants.PROCESS:
							self.grid[x][y] = constants.CONQUERED
			else:
				self.grid[_heroPos[0]][_heroPos[1]] = constants.PROCESS
			self.DFS(int(round(self._ball.pos[0]/constants.SCALE[0])), int(round(self._ball.pos[1]/constants.SCALE[1])))
			contador = -int(constants.GRID_SIZE[0]*constants.GRID_SIZE[1]/2)
			#draw grid
			for x in range(constants.GRID_SIZE[0]):
				for y in range(constants.GRID_SIZE[1]):
					_color = constants.WHITE
					if self.grid[x][y] == constants.PROCESS:
						_color = constants.LIGHT_GREEN
					elif self.grid[x][y] == constants.CONQUERED:
						_color = constants.GREEN
					elif self.grid[x][y] == constants.HYPER:
						_color = constants.GREEN
						self.grid[x][y] = constants.CONQUERED
					else:
						contador += 1
					pygame.draw.rect(self.screen, _color, [x*constants.SCALE[0], y*constants.SCALE[1], constants.SCALE[0], constants.SCALE[1]])




			if contador <= 0:
				print("YOU WON :)")
				sys.exit()
			#draw hero
			pygame.draw.rect(self.screen, constants.RED, [self._hero.pos[0], self._hero.pos[1], constants.HERO_SIZE[0], constants.HERO_SIZE[1]])

			#draw ball
			pygame.draw.circle(self.screen, constants.BLUE, [self._ball.pos[0], self._ball.pos[1]], constants.BALL_RADIUS)

		
			font = pygame.font.SysFont('Calibri', 25, True, False)
			text = font.render("Left: {}".format(contador), True, constants.BLACK)
			self.screen.blit(text, [0, 0])


			pygame.display.flip()
			clock.tick(100)
