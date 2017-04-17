import pygame

from main import engine, menu
from resources import constants
from stages import stage, stage_Survival
from user_data import data, dataManager
from visual import theme, themeManager

#enviroment init
pygame.init()
pygame.key.set_repeat(1, 100) # turn on "repeat" functionality
pygame.display.set_caption('paintTheWall', 'The Game')
screen = pygame.display.set_mode(constants.SCREEN_SIZE)

#data init
dManager = dataManager.DataManager()
data.startTime = data.getActualTime() - data.i['timePlayed']
score = 0

#elements init
_menu = menu.MainMenu(constants.QUIT)
action = constants.MAIN_MENU
lastAction = constants.UNDEFINED

#sound and visual init
music = pygame.mixer.music
themeManager.changeTheme(data.i['theme'])

while action != constants.QUIT:
	# music.load('resources/sounds/teste_1.mid')
	# music.play(0)
	# print("Lets go man action = ", action, " and lastaction = ", lastAction)
	screen.fill(theme.backgroundColor)

	if action != constants.MAIN_MENU or lastAction == constants.MAIN_MENU:
		if action != constants.RESTART:
			if action == constants.RANK_INSERT:
				action = _menu.update(screen)
				dManager.insert_rank((_menu.player_name, score))
			else:
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
	
	if action == constants.STAGE_SURVIVAL:
		_engine = stage_Survival.Stage_Survival()
		action = _engine.run(screen)
		if action == constants.LOSE:
			score = _engine.score
			_menu = menu.InsertRankMenu(constants.MAIN_MENU, dManager)
			action = constants.RANK_INSERT
	
	elif action in constants.STAGE_INDEX:
		selector = str(action - constants.STAGE_INDEX[0])
		_engine = eval("stage.Stage_" + selector)()
		action = _engine.run(screen)
		if action == constants.LOSE:
			_menu = menu.LoseMenu(constants.STAGE_MENU)
	
	elif action in constants.MENU_INDEX:
		selector = str("menu." + constants.MENU_INDEX[action] + "Menu")
		if action != constants.SURVIVAL_MENU:
			_menu = eval(selector)()
		else:
			_menu = eval(selector)(constants.MAIN_MENU, dManager)

	if action == constants.WIN:
		data.i['lastUnlockedStages'] = max(data.i['lastUnlockedStages'], 1 + lastAction - constants.STAGE_0)
		_menu = menu.WinMenu()
	
	_engine = None
	#music.stop()
	dManager.save()

data.i['timePlayed'] = data.getActualTime()
dManager.save()