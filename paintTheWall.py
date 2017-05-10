import pygame
from user_data import soundManager

from audiovisual import theme, themeManager
from main import engine, menu
from resources import constants, tools
from stages import stage, stage_Survival
from user_data import data, dataManager

"""
Main class of the game Paint The Wall
"""

screen, dManager, _menu = engine.set_environment()

action = constants.MAIN_MENU 	#flag game state
lastAction = constants.UNDEFINED

soundManager.play_music(theme.menu_song, data.menu_vol)

# Game Loop
while action != constants.QUIT:
	screen.fill(theme.backgroundColor)

	if action != constants.MAIN_MENU or lastAction == constants.MAIN_MENU:
		if action != constants.RESTART:
			action = _menu.update(screen)
			if action == constants.NEXT:
				action = lastAction + 1
				_menu = menu.StageMenu()
			elif action == constants.RESTART:
				action = lastAction
				_menu = menu.StageMenu()
		else:
			action = lastAction
	lastAction = action

	if action == constants.STAGE_SURVIVAL:
		soundManager.play_music(theme.game_song, data.game_vol)
		_engine = stage_Survival.Stage_Survival()
		action = _engine.run(screen)
		soundManager.play_music(theme.menu_song, data.game_vol)
		if action == constants.LOSE:
			soundManager.play_music(theme.rank_song, 1.0, 0)
			_menu = menu.InsertRankMenu()
			action = constants.RANK_INSERT
	elif action in constants.STAGE_INDEX:
		soundManager.play_music(theme.game_song, data.game_vol)
		selector = str(action - constants.STAGE_INDEX[0])
		_engine = eval("stage.Stage_" + selector)()
		action = _engine.run(screen)
		soundManager.play_music(theme.menu_song, data.game_vol)
		print("out this hell: ", action)

	elif action in constants.MENU_INDEX:
		print("play menu song")
		soundManager.play_music(theme.menu_song, data.menu_vol)
		selector = str("menu." + constants.MENU_INDEX[action] + "Menu")
		_menu = eval(selector)()

	if action == constants.WIN:
		soundManager.play_music(theme.win_song, 1.0, 0)
		data.i['lastUnlockedStages'] = max(data.i['lastUnlockedStages'], 1 + lastAction - constants.STAGE_0)
		_menu = menu.WinMenu()
	
	elif action == constants.LOSE:
		soundManager.play_music(theme.lose_song, 1.0, 0)
		_menu = menu.LoseMenu(constants.STAGE_MENU)
	
	_engine = None
	dManager.save()

data.i['timePlayed'] = data.getActualTime()
dManager.save()