import pygame
import random

from audiovisual import theme
from resources import constants

#bidimensional vector class
class Vector2:
	def __init__(self, X, Y):
		self.x = X
		self.y = Y

	def _print(self):
		print("(", self.x, ", ", self.y, ")")

	def Dx(self): #discretize 'x' coordinate
		return conv(self.x, 0)

	def Dy(self): #discretize 'y' coordinate
		return conv(self.y, 1)
	
# - - - - -

#checks if 'x' coordinate is valid
def valid_x(x, grid):
	return x >= 0 and x < len(grid)

#checks if 'y' coordinate is valid
def valid_y(y, grid):
	if len(grid) > 0:
		return y >= 0 and y < len(grid[0])
	return False

#checks if (x, y) position is valid
def valid(x, y, grid):
	return valid_x(x, grid) and valid_y(y, grid)

#scale converter
def conv(c, t): # t = 0 (x) or 1 (y)
	return int(round(c/constants.SCALE[t]))

#convert coordinates
def discretize(pos):
	return [conv(pos.x, 0), conv(pos.y, 1)]

#signal function
def sign(x):
	if x > 0:
		return 1
	return -1