import constants
import dataManager
import engine
import menu
import pygame
import stage_Survival
import stage
import stage_10
import time
import data

from pygame.locals import *


pygame.init()
pygame.display.set_caption('THE GAME', 'The Game')
music = pygame.mixer.music
screen = pygame.display.set_mode(constants.SCREEN_SIZE)
startTime = time.clock()
print("Acho que eh ", constants.GRID_SIZE[0]*constants.GRID_SIZE[1] - 2*constants.GRID_SIZE[0] - 2*constants.GRID_SIZE[1] + 4)
dManager = dataManager.DataManager()
data.startTime = startTime - data.i['timePlayed']
data.actualTime = time.clock() - data.startTime

_menu = menu.MainMenu()
action = constants.UNDEFINED

while action != constants.QUIT:
	# pygame.mixer.music.load('sounds/teste_1.mid')
	# music.play(0)
	screen.fill(constants.WHITE)
	if action != constants.RESTART:
		action = _menu.update(screen)
		lastAction = action
	else:
		action = lastAction
	# music.stop()

	# music.load('sounds/teste_2.mid')
	# music.play(0)

	if action == constants.PLAY:
		action = constants.RESTART
		while action == constants.RESTART:
			_engine = engine.Engine()
			action = _engine.run(screen)
	
	elif action == constants.STAGE_SURVIVAL:
		_engine = stage_Survival.Stage_Survival()
		action = _engine.run(screen)

	elif action == constants.STAGE1:
		_engine = stage.Stage_1()
		action = _engine.run(screen)
	elif action == constants.STAGE2:
		_engine = stage.Stage_2()
		action = _engine.run(screen)
	elif action == constants.STAGE3:
		_engine = stage.Stage_3()
		action = _engine.run(screen)
	elif action == constants.STAGE4:
		_engine = stage.Stage_4()
		action = _engine.run(screen)
	elif action == constants.STAGE5:
		_engine = stage.Stage_5()
		action = _engine.run(screen)
	elif action == constants.STAGE6:
		_engine = stage.Stage_6()
		action = _engine.run(screen)
	elif action == constants.STAGE7:
		_engine = stage.Stage_7()
		action = _engine.run(screen)
	elif action == constants.STAGE8:
		_engine = stage.Stage_8()
		action = _engine.run(screen)

	elif action == constants.STAGE10:
		action = constants.RESTART
		while action == constants.RESTART:
			_engine = stage_10.Stage_10()
			action = _engine.run(screen)

	#menus
	elif action == constants.ABOUT_MENU:
		_menu = menu.AboutMenu()
	
	elif action == constants.ACHIEVEMENTS_MENU:
		_menu = menu.AchievementsMenu()
	
	elif action == constants.MAIN_MENU:
		_menu = menu.MainMenu()
	
	elif action == constants.RANK_MENU:
		_menu = menu.RankMenu()
	
	elif action == constants.STAGE_MENU:
		_menu = menu.StageMenu()
	
	elif action == constants.STATS_MENU:
		_menu = menu.StatsMenu()
	
	elif action == constants.SURVIVAL_MENU:
		_menu = menu.SurvivalMenu()
	

	if action == constants.WIN:
		data.i['lastUnlockedStages'] = max(data.i['lastUnlockedStages'], 1 + lastAction - constants.STAGE0)
		print("You won, can play ", data.i['lastUnlockedStages'])
	elif action == constants.LOSE:
		print("SADNESS :(")
	_engine = None
	#music.stop()
	dManager.save()


data.i['timePlayed'] += time.clock() - startTime
dManager.save()