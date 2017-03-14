import engine
import constants
import menu
import pygame
from pygame.locals import *

pygame.init()
pygame.display.set_caption('THE GAME', 'The Game')
music = pygame.mixer.music
screen = pygame.display.set_mode(constants.SCREEN_SIZE)

_menu = menu.Menu()
action = constants.UNDEFINED

while action != constants.QUIT:
#	music.load('sounds/teste_1.mid')
#	music.play(0)
	
	# action = _menu.update(screen)
#	music.stop()

#	music.load('sounds/teste_2.mid')
#	music.play(0)
	# if action == constants.STAGE_SELECT:
		_engine = engine.Engine()
		_engine.numberBalls = 12
		_engine.run(screen)
		action = constants.UNDEFINED
	# elif action == constants.LEVEL_0:
		# pass

	# music.stop()