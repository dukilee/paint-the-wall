import pygame

from main import engine, menu
from resources import constants
from stages import stage, stage_Survival
from user_data import data, dataManager
from visual import theme, themeManager

pygame.init()
pygame.display.set_caption('paintTheWall', 'The Game')
music = pygame.mixer.music
screen = pygame.display.set_mode(constants.SCREEN_SIZE)
dManager = dataManager.DataManager()
data.startTime = data.getActualTime() - data.i['timePlayed']
_menu = menu.MainMenu()
action = constants.UNDEFINED
lastAction = constants.UNDEFINED

themeManager.changeTheme(data.i['theme'])

while action != constants.QUIT:
	# music.load('resources/sounds/teste_1.mid')
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

	# music.load('resources/sounds/teste_2.mid')
	# music.play(0)

	if action == constants.PLAY:
		action = constants.RESTART
		while action == constants.RESTART:
			_engine = engine.Engine()
			action = _engine.run(screen)
	
	elif action == constants.STAGE_SURVIVAL:
		_engine = stage_Survival.Stage_Survival()
		action = _engine.run(screen)
	elif action in constants.STAGE_INDEX:
		selector = str(action - constants.STAGE_INDEX[0])
		_engine = eval("stage.Stage_" + selector)()
		action = _engine.run(screen)

	elif action in constants.MENU_INDEX:
		selector = str("menu." + constants.MENU_INDEX[action] + "Menu")
		_menu = eval(selector)()

	if action == constants.WIN:
		data.i['lastUnlockedStages'] = max(data.i['lastUnlockedStages'], 1 + lastAction - constants.STAGE_0)
		_menu = menu.WinMenu()

	elif action == constants.LOSE:
		_menu = menu.LoseMenu()

	_engine = None
	#music.stop()
	dManager.save()

data.i['timePlayed'] = data.getActualTime()
dManager.save()