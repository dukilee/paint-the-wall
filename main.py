import constants
import engine
import menu
import pygame
import stage_10

from pygame.locals import *

pygame.init()
pygame.display.set_caption('THE GAME', 'The Game')
music = pygame.mixer.music
screen = pygame.display.set_mode(constants.SCREEN_SIZE)

_menu = menu.MainMenu()
action = constants.UNDEFINED

while action != constants.QUIT:
	pygame.mixer.music.load('sounds/teste_1.mid')
	music.play(0)
	
	action = _menu.update(screen)
	music.stop()

	music.load('sounds/teste_2.mid')
	music.play(0)
	if action == constants.PLAY:
		_engine = engine.Engine(12)
		action = _engine.run(screen)

	elif action == constants.STAGE:
		_menu = menu.StageMenu()

	elif action == constants.MAIN_MENU:
		_menu = menu.MainMenu()

	elif action == constants.STAGE10:
		_engine = stage_10.Stage_10(5)
		action = _engine.run(screen)
		
	music.stop()