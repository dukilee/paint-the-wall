import pygame

from audiovisual import theme, themeManager
from main import engine, menu
from resources import constants, tools
from stages import stage, stage_Survival
from user_data import data, dataManager

screen, dManager, _menu = engine.set_environment()

action = constants.MAIN_MENU 	#flag game state
lastAction = constants.UNDEFINED

theme.play_music(theme.menu_song, theme.menu_vol)

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
		theme.play_music(theme.game_song, theme.game_vol)
		_engine = stage_Survival.Stage_Survival()
		action = _engine.run(screen)
		if action == constants.LOSE:
			theme.play_music(theme.rank_song, 1.0, 0)
			_menu = menu.InsertRankMenu()
			action = constants.RANK_INSERT

	elif action in constants.STAGE_INDEX:
		theme.play_music(theme.game_song, theme.game_vol)
		selector = str(action - constants.STAGE_INDEX[0])
		_engine = eval("stage.Stage_" + selector)()
		action = _engine.run(screen)

	elif action in constants.MENU_INDEX:
		theme.play_music(theme.menu_song, theme.menu_vol)
		selector = str("menu." + constants.MENU_INDEX[action] + "Menu")
		_menu = eval(selector)()

	if action == constants.WIN:
		data.i['lastUnlockedStages'] = max(data.i['lastUnlockedStages'], 1 + lastAction - constants.STAGE_0)
		theme.play_music(theme.win_song, 1.0, 0)
		_menu = menu.WinMenu()
	
	elif action == constants.LOSE:
		theme.play_music(theme.lose_song, 1.0, 0)
		_menu = menu.LoseMenu(constants.STAGE_MENU)
	
	_engine = None
	dManager.save()

data.i['timePlayed'] = data.getActualTime()
dManager.save()