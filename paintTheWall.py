import constants
import dataManager
import engine
import menu
import pygame
import stage_Survival
import stage
import data
import themeManager
import theme

pygame.init()
pygame.display.set_caption('THE GAME', 'The Game')
music = pygame.mixer.music
screen = pygame.display.set_mode(constants.SCREEN_SIZE)
dManager = dataManager.DataManager()
data.startTime = data.getActualTime() - data.i['timePlayed']
_menu = menu.MainMenu()
action = constants.UNDEFINED
lastAction = constants.UNDEFINED

themeManager.changeTheme(data.i['theme'])

while action != constants.QUIT:
	# pygame.mixer.music.load('sounds/teste_1.mid')
	# music.play(0)
	# print("Lets go man action = ", action, " and lastaction = ", lastAction)
	screen.fill(theme.backgroundColor)
	if action != constants.MAIN_MENU or lastAction == constants.MAIN_MENU:
		if action != constants.RESTART:
			action = _menu.update(screen)
			if action == constants.NEXT:
				action = lastAction + 1
			elif action == constants.RESTART:
				action = lastAction
		else:
			action = lastAction
	lastAction = action
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
	elif action == constants.STAGE9:
		_engine = stage.Stage_9()
		action = _engine.run(screen)
	elif action == constants.STAGE10:
		_engine = stage.Stage_10()
		action = _engine.run(screen)
	elif action == constants.STAGE11:
		_engine = stage.Stage_11()
		action = _engine.run(screen)
	elif action == constants.STAGE12:
		_engine = stage.Stage_12()
		action = _engine.run(screen)
	elif action == constants.STAGE13:
		_engine = stage.Stage_13()
		action = _engine.run(screen)
	elif action == constants.STAGE14:
		_engine = stage.Stage_14()
		action = _engine.run(screen)
	elif action == constants.STAGE15:
		_engine = stage.Stage_15()
		action = _engine.run(screen)
	elif action == constants.STAGE16:
		_engine = stage.Stage_16()
		action = _engine.run(screen)
	elif action == constants.STAGE17:
		_engine = stage.Stage_17()
		action = _engine.run(screen)
	elif action == constants.STAGE18:
		_engine = stage.Stage_18()
		action = _engine.run(screen)
	elif action == constants.STAGE19:
		_engine = stage.Stage_19()
		action = _engine.run(screen)
	elif action == constants.STAGE20:
		_engine = stage.Stage_20()
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

	elif action == constants.STAGE_MENU_2:
		_menu = menu.StageMenu2()
	
	elif action == constants.STATS_MENU:
		_menu = menu.StatsMenu()

	elif action == constants.SURVIVAL_MENU:
		_menu = menu.SurvivalMenu()


	elif action == constants.SETTINGS_MENU:
		_menu = menu.SettingsMenu()

	if action == constants.WIN:
		data.i['lastUnlockedStages'] = max(data.i['lastUnlockedStages'], 1 + lastAction - constants.STAGE0)
		_menu = menu.WinMenu()

	elif action == constants.LOSE:
		_menu = menu.LoseMenu()

	_engine = None
	#music.stop()
	dManager.save()

data.i['timePlayed'] = data.getActualTime()
dManager.save()