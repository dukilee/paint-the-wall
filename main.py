import engine
import constants
import menu
import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode(constants.SCREEN_SIZE)

_engine = engine.Engine()
_menu = menu.Menu()

action = constants.QUIT + 1 #just to enter the while 
while action != constants.QUIT:
	action = _menu.update(screen)

	if action == constants.STAGE_SELECT:
		_engine.numberBalls = 4
		_engine.run(screen)



