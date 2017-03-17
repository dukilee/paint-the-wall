import pygame

class sprite(pygame.sprite.Sprite):
	def __init__(self, path):
		# pygame.sprite.Sprite.__init__(self) # not sure if needed. leave it commented for now
		self.img = pygame.image.load('sprites/' + path)
		self.rec = self.img.get_rect()