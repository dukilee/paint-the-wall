import random

from audiovisual import theme
from resources import constants, tools

#The enemy
class Ball:
	"""
	Keeps the ball position and speed. Also updates the ball given the current field
	"""
	def __init__(self):
		"""
		Starts in a random position with a random direction, but fixed speed.
		"""
		self.pos = self.random_pos() #random position on screen
		self.speed = self.random_spd() #random speed
		self.sprite = theme.sprite('default/ball.png', 0.225)

	@staticmethod
	def random_pos():
		"""
		Calculates a valid random position for the ball
		:return: a valid random position
		"""
		return tools.Vector2(random.randint(1 + int(0.1 * constants.SCREEN_SIZE[0]), int(0.9 * constants.SCREEN_SIZE[0])), random.randint(int(1 + 0.1 * constants.SCREEN_SIZE[1]), int(0.9 * constants.SCREEN_SIZE[1])))

	@staticmethod
	def random_spd():
		"""
		Calculates a random direction for the ball
		:return: a random direction
		"""
		speed = tools.Vector2(constants.DEF_Vx, constants.DEF_Vy)
		if random.randint(-1, 1) < 0:
			speed.x *=-1
		if random.randint(-1, 1) < 0:
			speed.y *=-1
		return speed

	#update position on screen
	def update(self, grid):
		"""
		given the actual game state, calculates the next position of the ball and its next
		direction (if the ball collide with the wall). And checks if the ball killed the hero.
		:param grid: game state
		:return: returns if the ball killed or not the hero
		"""
		nextPos = tools.Vector2(self.pos.x + constants.BALL_RADIUS*tools.sign(self.speed.x), self.pos.y + constants.BALL_RADIUS*tools.sign(self.speed.y))
		actualGrid = tools.discretize(self.pos)
		nextGrid = tools.discretize(nextPos)
		
		#horizontal reflection on walls
		if tools.valid(nextGrid[0], actualGrid[1], grid) and grid[nextGrid[0]][actualGrid[1]] == constants.CONQUERED or not tools.valid_x(nextGrid[0], grid):
			self.speed.x *= -1
			nextPos.x = self.pos.x + self.speed.x
			nextGrid[0] = tools.conv(nextPos.x, 0)
		
		#vertical reflectio on walls
		if tools.valid(actualGrid[0], nextGrid[1], grid) and grid[actualGrid[0]][nextGrid[1]] == constants.CONQUERED or not tools.valid_y(nextGrid[1], grid):
			self.speed.y *= -1
			nextPos.y = self.pos.y + self.speed.y
			nextGrid[1] = tools.conv(nextPos.y, 1)
		
		#verify if player path was hit
		if tools.valid(nextGrid[0], nextGrid[1], grid) and grid[nextGrid[0]][nextGrid[1]] == constants.PROCESS:
			return constants.LOSE

		#new position
		self.pos = tools.Vector2(self.pos.x + self.speed.x, self.pos.y + self.speed.y)

		#may return 'LOSE' or 'UNDEFINED' states
		return constants.UNDEFINED