import pygame
import random

from resources import constants

#bidimentional vector class
class Vector2:
	def __init__(self, X, Y):
		self.x = X
		self.y = Y

	def _print(self):
		print("(", self.x, ", ", self.y, ")")

#for creating sprites
class sprite(pygame.sprite.Sprite):
	def __init__(self, path, scale = 1.0):
		# pygame.sprite.Sprite.__init__(self) # not sure if needed. leave it commented for now
		self.img = pygame.image.load('resources/sprites/' + path)
		self.rec = self.img.get_rect()
		self.img = pygame.transform.scale(self.img, (int(self.rec.width * scale), int(self.rec.height * scale)))

# - - - - -

#for ball generation
def random_pos():
	return Vector2(random.randint(1 + int(0.1 * constants.SCREEN_SIZE[0]), int(0.9 * constants.SCREEN_SIZE[0])), random.randint(int(1 + 0.1 * constants.SCREEN_SIZE[1]), int(0.9 * constants.SCREEN_SIZE[1])))

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
