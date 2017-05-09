import pygame
import random

from audiovisual import theme
from resources import constants

#bidimensional vector class
class Vector2:
	"""
	A pair of numbers to represent position in a cartesian plan
	"""
	def __init__(self, X, Y):
		"""
		:param X: horizontal coordinate
		:param Y: vertical coordinate
		"""
		self.x = X
		self.y = Y

	def _print(self):
		"""
		Prints the content of the class
		"""
		print("(", self.x, ", ", self.y, ")")

	def Dx(self):
		"""discretize 'x' coordinate"""
		return conv(self.x, 0)

	def Dy(self):
		"""discretize 'y' coordinate"""
		return conv(self.y, 1)
	
# - - - - -

def valid_x(x, grid):
	"""
	checks if 'x' coordinate is valid
	:param x: 'x' coordinate
	:param grid: current game state
	:return: true if is valid
	"""
	return x >= 0 and x < len(grid)

def valid_y(y, grid):
	"""
	checks if 'y' coordinate is valid
	:param y: 'y' coordinate
	:param grid: current game state
	:return: true if is valid
	"""
	if len(grid) > 0:
		return y >= 0 and y < len(grid[0])
	return False

def valid(x, y, grid):
	"""
	Checks if 'x' and 'y' coordinates are valid
	:param x: 'x' coordinate
	:param y: 'y' coordinate
	:param grid: current game state
	:return: true if both are valid
	"""
	return valid_x(x, grid) and valid_y(y, grid)

def conv(c, t): # t = 0 (x) or 1 (y)
	"""scale converter"""
	return int(round(c/constants.SCALE[t]))

def discretize(pos):
	"""
	Convert coordinates
	:param pos: Current coordinate
	:return: Coordinate after conversion
	"""
	return [conv(pos.x, 0), conv(pos.y, 1)]

def sign(x):
	"""
	Returns the signal of x
	:param x: real value
	:return: 1 if x is positive, -1 otherwise
	"""
	if x > 0:
		return 1
	return -1