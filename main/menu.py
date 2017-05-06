import dataManager
import pygame

from audiovisual import animation, theme, themeManager
from pygame.locals import *
from resources import constants, elements, tools
from user_data import data

class Menu:
	def __init__(self, parent = constants.MAIN_MENU):
		self.elements = []
		self.animations = []
		self.parent_menu = parent #where to go when quitting this menu

	def initActors(self, ):
		pass

	def update(self, screen, anotherElement = None):
		clock = pygame.time.Clock()
		done = False
		action = self.parent_menu
		pygame.mouse.set_cursor(*pygame.cursors.tri_left)
		listShortcut = {}
		
		mouse = pygame.mouse
		self.initActors()

		if anotherElement != None:
			self.elements.append(elements.Label(None, 200, anotherElement, 40, False, constants.BLACK))

		count = 0

		for e in self.elements:
			for s in e.shortcut:
				listShortcut[s] = e
		if constants.NOKEY in listShortcut:
			del listShortcut[constants.NOKEY]

		while not done:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return constants.QUIT
				elif event.type == pygame.KEYDOWN:
					if event.key == constants.keys['q']:
						return self.parent_menu
					if event.key in listShortcut:
						done = True
						action = listShortcut[event.key].action
						if action == constants.SPECIAL:
							listShortcut[event.key].callAction()

			#button PLAY
			screen.fill(theme.backgroundColor)
			for b in self.elements:
				done, action = b.hover(mouse, done, action)
				b.blit(screen)
			count += 1
			for a in self.animations:
				a.update(screen, count)

			pygame.display.update(self.updateRect)
			clock.tick(200)

		return action

class AboutMenu(Menu):
	def initActors(self):
		#part of the screen that this menu uses
		self.updateRect = constants.SCR

		#actors
		self.elements = []
		self.elements.append(Label(None, constants.POS['UP'], 'About'))
		self.elements.append(Button(constants.POS['RIGHT'], constants.POS['DOWN'], 'BACK', constants.MAIN_MENU, [constants.keys['b'], constants.keys['backspace']]))

class AchievementsMenu(Menu):
	def toDK(self):#double kill
		self.overString = 'Kill two balls at same time.'

	def toYM(self):#Yoga master
		self.overString = 'Kill a ball with only the first move.'

	def toWE(self): #World Emperor
		self.overString = 'Conquer the hole screen.'

	def toIM(self):#Immortal
		self.overString = 'Do 666 points in survival mode.'

	def toJE(self):#Jedi
		self.overString = 'Conquer all achievements.'

	def toPI(self):#Pilgrim
		self.overString = 'Complete stage 10.'

	def toHA(self):#hacker
		self.overString = 'Complete all stages. :D'

	def toPA(self):#Pacifist
		self.overString = 'Complete stage 9 without killing balls'

	def toSK(self):#Serial Killer
		self.overString = 'Kill 42 balls.'

	def instructionsText(self):
		copy = self.overString
		self.overString = '<Pass mouse over achievements to get info>'
		return copy

	def initActors(self):
		#part of the screen that this menu uses
		self.updateRect = constants.SCR
		self.overString = '<Pass mouse over achievements>'

		#actors
		self.elements = []
		self.elements.append(elements.Title(None, constants.POS['UP'], 'Achievements'))
		self.elements.append(elements.Rectangle(10, constants.POS['DOWN'], 460, 50, theme.labelTextLLColor))
		self.elements.append(elements.Label(130, constants.POS['DOWN']+15, 'Instructions a lot of it', 30, False, None, None, self.instructionsText))
		# self.elements.append(elements.Label(constants.POS['RIGHT'], 300, '00:00:00'             ,    30, False, None, None, self.timeText))
		self.elements.append(elements.Button(constants.POS['RIGHT'], constants.POS['DOWN'], 'BACK', constants.MAIN_MENU, [constants.keys['b'], constants.keys['backspace']]))

		if data.i['doubleKill'] == 1:
			self.elements.append(elements.Label(50, 210, 'Double Kill', 30, False, None, None))
			self.elements.append(elements.ButtonOver(50, 150, self.toDK, 'doubleKillMini.png'))
		else:
			self.elements.append(
				elements.Label(50, 210, 'Double Kill', 30, False, theme.labelBackColor, theme.labelTextLowColor))
			self.elements.append(elements.ButtonOver(50, 150, self.toDK, 'unknown.png'))
		self.elements.append(elements.Rectangle(50, 150, 197, 57, theme.titleBackColor, 5))

		if data.i['worldEmperor'] == 1:
			self.elements.append(
				elements.Label(300, 210, 'World Emperor', 30, False, theme.labelBackColor, theme.labelTextColor))
			self.elements.append(elements.ButtonOver(300, 150, self.toWE, 'worldEmperorMini.png'))
		else:
			self.elements.append(
				elements.Label(300, 210, 'World Emperor', 30, False, theme.labelBackColor, theme.labelTextLowColor))
			self.elements.append(elements.ButtonOver(300, 150, self.toWE, 'unknown.png'))
		self.elements.append(elements.Rectangle(300, 150, 197, 57, theme.titleBackColor, 5))

		if data.i['yogaMaster'] == 1:
			self.elements.append(elements.Label(550, 210, 'Yoga Master', 30, False, theme.labelBackColor, theme.labelTextColor))
			self.elements.append(elements.ButtonOver(550, 150, self.toYM, 'yogaMasterMini.png'))
		else:
			self.elements.append(
				elements.Label(550, 210, 'Yoga Master', 30, False, theme.labelBackColor, theme.labelTextLowColor))
			self.elements.append(elements.ButtonOver(550, 150, self.toYM, 'unknown.png'))
		self.elements.append(elements.Rectangle(550, 150, 197, 57, theme.titleBackColor, 5))

		if data.i['pacifist'] == 1:
			self.elements.append(elements.Label(50, 310, 'Pacifist', 30, False, None, None))
			self.elements.append(elements.ButtonOver(50, 250, self.toPA, 'pacifistMini.png'))
		else:
			self.elements.append(
				elements.Label(50, 310, 'Pacifist', 30, False, theme.labelBackColor, theme.labelTextLowColor))
			self.elements.append(elements.ButtonOver(50, 250, self.toPA, 'unknown.png'))
		self.elements.append(elements.Rectangle(50, 250, 197, 57, theme.titleBackColor, 5))

		if data.i['serialKiller'] == 1:
			self.elements.append(elements.Label(550, 310, 'Serial Killer', 30, False, theme.labelBackColor, theme.labelTextColor))
			self.elements.append(elements.ButtonOver(550, 250, self.toSK, 'serialKillerMini.png'))
		else:
			self.elements.append(
				elements.Label(550, 310, 'Serial Killer', 30, False, theme.labelBackColor, theme.labelTextLowColor))
			self.elements.append(elements.ButtonOver(550, 250, self.toSK, 'unknown.png'))
		self.elements.append(elements.Rectangle(550, 250, 197, 57, theme.titleBackColor, 5))

		if data.i['immortal'] == 1:
			self.elements.append(elements.Label(50, 410, 'Immortal', 30, False, None, None))
			self.elements.append(elements.ButtonOver(50, 350, self.toIM, 'jedi.png'))
		else:
			self.elements.append(
				elements.Label(50, 410, 'Immortal', 30, False, theme.labelBackColor, theme.labelTextLowColor))
			self.elements.append(elements.ButtonOver(50, 350, self.toIM, 'unknown.png'))
		self.elements.append(elements.Rectangle(50, 350, 197, 57, theme.titleBackColor, 5))

		if data.i['pilgrim'] == 1:
			self.elements.append(
				elements.Label(300, 410, 'Pilgrim', 30, False, theme.labelBackColor, theme.labelTextColor))
			self.elements.append(elements.ButtonOver(300, 350, self.toPI, 'jedi.png'))
		else:
			self.elements.append(
				elements.Label(300, 410, 'Pilgrim', 30, False, theme.labelBackColor, theme.labelTextLowColor))
			self.elements.append(elements.ButtonOver(300, 350, self.toPI, 'unknown.png'))
		self.elements.append(elements.Rectangle(300, 350, 197, 57, theme.titleBackColor, 5))

		if data.i['hacker'] == 1:
			self.elements.append(elements.Label(550, 410, 'Hacker', 30, False, theme.labelBackColor, theme.labelTextColor))
			self.elements.append(elements.ButtonOver(550, 350, self.toHA, 'jedi.png'))
		else:
			self.elements.append(
				elements.Label(550, 410, 'Hacker', 30, False, theme.labelBackColor, theme.labelTextLowColor))
			self.elements.append(elements.ButtonOver(550, 350, self.toHA, 'unknown.png'))
		self.elements.append(elements.Rectangle(550, 350, 197, 57, theme.titleBackColor, 5))

		if data.i['jedi'] == 1:
			self.elements.append(
				elements.Label(300, 310, 'Jedi', 30, False, theme.labelBackColor, theme.labelTextColor))
			self.elements.append(elements.ButtonOver(300, 250, self.toJE, 'jedi.png'))
		else:
			self.elements.append(
				elements.Label(300, 310, 'Jedi', 30, False, theme.labelBackColor, theme.labelTextLowColor))
			self.elements.append(elements.ButtonOver(300, 250, self.toJE, 'unknown.png'))
		self.elements.append(elements.Rectangle(300, 250, 197, 57, theme.titleBackColor, 5))

class MainMenu(Menu):
	def initActors(self):
		#where to go when quitting this menu
		self.parent_menu = constants.QUIT

		#part of the screen that this menu uses
		self.updateRect = constants.SCR

		#actors
		self.elements = []
		# self.elements.append(Label(None, constants.POS['UP'], 'Paint-The-Wall!'))
		self.elements.append(elements.Title(None, constants.POS['UP'], 'Paint the Wall!'))
		self.elements.append(elements.Button(None, 150, 'STAGES', constants.STAGE_MENU, [constants.keys['s']]))
		self.elements.append(elements.Button(None, 219, 'SURVIVAL', constants.SURVIVAL_MENU, [constants.keys['v']]))
		self.elements.append(elements.Button(None, 288, 'ACHIEVEMENTS', constants.ACHIEVEMENTS_MENU, [constants.keys['a']]))
		self.elements.append(elements.Button(None, 357, 'STATS', constants.STATS_MENU, [constants.keys['t']]))
		self.elements.append(elements.Button(None, 426, 'SETTINGS', constants.SETTINGS_MENU, [constants.keys['g']]))
		self.elements.append(elements.Button(None, 495, 'QUIT', constants.QUIT))

		#animations
		# self.animations.append(animation.MainMenuAnimation())

class PauseMenu(Menu):
	def initActors(self):
		#part of the screen that this menu uses
		self.updateRect = Rect(0, 100, constants.SCREEN_SIZE[0], 300)

		#actors
		self.elements = []
		self.elements.append(elements.Label(None, 350, 'Press \'p\' to resume.', 30, False, constants.BLACK))
		self.elements.append(elements.Button(constants.POS['LEFT'], None, 'Menu', self.parent_menu, [constants.keys['m']]))
		self.elements.append(elements.Button(None, None, 'Restart', constants.RESTART, [constants.keys['r']]))
		self.elements.append(elements.Button(constants.POS['RIGHT'], None, 'Resume', constants.UNDEFINED, [constants.keys['p'], constants.keys['enter']]))

class StartMenu(Menu):
	def initActors(self):
		#part of the screen that this menu uses
		self.updateRect = Rect(0, 100, constants.SCREEN_SIZE[0], 300)

		#actors
		self.elements = []
		self.elements.append(elements.Label(None, 350, 'Press \'Enter\' to start.', 30, False, constants.BLACK))
		self.elements.append(elements.Button(None, None, 'Start', constants.UNDEFINED, [constants.keys['s'], constants.keys['enter']]))
		self.elements.append(elements.Button(constants.POS['LEFT'], None, 'Menu', self.parent_menu, [constants.keys['m']]))

class StageMenu(Menu):
	def initActors(self):
		#part of the screen that this menu uses
		self.updateRect = constants.SCR

		#actors
		self.elements = [elements.Button(constants.POS['RIGHT'], constants.POS['DOWN'], 'Back', constants.MAIN_MENU, [constants.keys['b'], constants.keys['backspace']])]
		self.elements.append(elements.Button(constants.POS['LEFT'], constants.POS['DOWN'], 'Tutorial', constants.UNDEFINED, [constants.keys['t']]))
		self.elements.append(elements.miniButton(constants.POS['RIGHT']+130, 240, '>', constants.STAGE_MENU_2, [constants.KEY_RIGHT]))
		self.elements.append(elements.Title(None, constants.POS['UP'], 'Stages'))
		# self.elements.append(Label(None, constants.POS['UP'], 'Stages'))
		for i in range(10):
			if i >= data.i['lastUnlockedStages']:
				self.elements.append(elements.Label(170 + (i % 5) * 110, 190 + int(i / 5) * 150,'{}'.format(i), 30, False, constants.BLACK, theme.labelTextLLColor))
			elif i == data.i['lastUnlockedStages']-1: #Button()
				self.elements.append(elements.miniButton(150 + (i % 5) * 110, 170 + int(i / 5) * 150, '{}'.format(i), constants.STAGE_INDEX[i + 1], [constants.keys[str(i)]], None, constants.BUTTON_FONT_SIZE, True, theme.offButtonActualStage, theme.onButtonActualStage))
			else:
				self.elements.append(elements.miniButton(150 + (i % 5) * 110, 170 + int(i / 5) * 150, '{}'.format(i), constants.STAGE_INDEX[i + 1], [constants.keys[str(i)]]))

class Stage2Menu(Menu):
	def initActors(self):
		#part of the screen that this menu uses
		self.updateRect = constants.SCR

		#actors
		self.elements = [elements.Button(constants.POS['RIGHT'], constants.POS['DOWN'], 'Back', constants.MAIN_MENU, [constants.keys['b'], constants.keys['backspace']])]
		self.elements.append(elements.Button(constants.POS['LEFT'], constants.POS['DOWN'], 'Tutorial', constants.UNDEFINED, [constants.keys['t']]))
		self.elements.append(
			elements.miniButton(constants.POS['LEFT']+10, 240, '<', constants.STAGE_MENU, [constants.KEY_LEFT]))

		self.elements.append(elements.Title(None, constants.POS['UP'], 'Stages'))
		for i in range(10, 20):
			if i >= data.i['lastUnlockedStages']:
				self.elements.append(elements.Label(170 + (i % 5) * 110, 190 + int((i-10) / 5) * 150,'{}'.format(i), 30, False, constants.BLACK, theme.labelTextLLColor))
			elif i==data.i['lastUnlockedStages']-1:																																			# Button()
				self.elements.append(elements.miniButton(150 + (i % 5) * 110, 170 + int((i-10) / 5) * 150, '{}'.format(i), constants.STAGE_INDEX[1] + i, [constants.keys[str(i - 10)]], None, constants.BUTTON_FONT_SIZE, True, theme.offButtonActualStage, theme.onButtonActualStage))
			else:
				self.elements.append(elements.miniButton(150 + (i % 5) * 110, 170 + int((i-10) / 5) * 150, '{}'.format(i), constants.STAGE_INDEX[1] + i, [constants.keys[str(i - 10)]]))

class StatsMenu(Menu):
	def timeText(self):
		actualTime = data.getActualTime()
		return '{0:0=2d}:{1:0=2d}:{2:0=2d}'.format(int(actualTime / 3600), (int(actualTime / 60)) % 60,
											   (actualTime) % 60)

	def initActors(self):
		#part of the screen that this menu uses
		self.updateRect = constants.SCR

		#actors
		self.elements = []
		self.elements.append(elements.Title(None, constants.POS['UP'], 'Stats'))
		self.elements.append(elements.Button(constants.POS['RIGHT'], constants.POS['DOWN'], 'BACK', constants.MAIN_MENU, [constants.keys['b'], constants.keys['backspace']]))
		self.elements.append(elements.Label(constants.POS['LEFT'], 300, 'Time Played:', 30, False))
		self.elements.append(elements.Label(constants.POS['LEFT'], 350, 'Blocks Destructed:', 30, False))
		self.elements.append(elements.Label(constants.POS['LEFT'], 400, 'Balls Killed:', 30, False))
		self.elements.append(elements.Label(constants.POS['LEFT'], 450, 'Deaths:', 30, False))
		self.elements.append(elements.Label(constants.POS['RIGHT'], 300, '00:00:00', 30, False, None, None, self.timeText))
		self.elements.append(elements.Label(constants.POS['RIGHT'], 350, '{}'.format(data.i['blocksConquered']), 30, False))
		self.elements.append(elements.Label(constants.POS['RIGHT'], 400, '{}'.format(data.i['ballsDestructed']), 30, False))
		self.elements.append(elements.Label(constants.POS['RIGHT'], 450, '{}'.format(data.i['deaths']), 30, False))

class SurvivalMenu(Menu):
	def initActors(self):
		#part of the screen that this menu uses
		self.updateRect = constants.SCR

		#actors
		self.elements = [elements.Title(None, constants.POS['UP'], 'Survival')]
		
		for k in range(len(data.i['rank'])):
			self.elements.append(elements.Label(300, 150 + 35 * k, data.i['rank'][k][0], 30, False))
			self.elements.append(elements.Label(500, 150 + 35 * k, str(data.i['rank'][k][1]), 30, False))

		self.elements.append(elements.Button(None, constants.POS['DOWN'], 'PLAY', constants.STAGE_SURVIVAL, [constants.keys['p'], constants.keys['enter']]))
		self.elements.append(elements.Button(constants.POS['RIGHT'], constants.POS['DOWN'], 'BACK', constants.MAIN_MENU, [constants.keys['b']]))

class SettingsMenu(Menu):
	def toBasic(self):
		themeManager.changeTheme(constants.BASIC_THEME)

	def toDark(self):
		themeManager.changeTheme(constants.DARK_THEME)

	def toSMW(self):
		themeManager.changeTheme(constants.MARIO_THEME)

	def setMusicVolume(self, val):
		data.i['musicVolume'] = val
		theme.vol_max = val / 100.0
		theme.music.set_volume(theme.vol_max * theme.menu_vol)

	def setEffectsVolume(self, val):
		data.i['effectsVolume'] = val

	def initActors(self):
		#part of the screen that this menu uses
		self.updateRect = constants.SCR

		#actors
		self.elements = []
		self.elements.append(elements.Title(None, constants.POS['UP'], 'Settings'))
		self.elements.append(elements.SlideBar(350, 120, 410, 100, self.setMusicVolume, data.i['musicVolume']))
		self.elements.append(elements.Label(constants.POS['LEFT'], 135, 'Music Volume:', 40, False))
		self.elements.append(elements.SlideBar(350, 200, 410, 100, self.setEffectsVolume, data.i['effectsVolume']))
		self.elements.append(elements.Label(constants.POS['LEFT'], 215, 'Effects Volume:', 40, False))

		self.elements.append(elements.Label(constants.POS['LEFT'], 295, 'Theme:', 40, False))
		self.elements.append(elements.Button(170, 295, 'BASIC', constants.SPECIAL, [constants.keys['a']], self.toBasic))
		self.elements.append(elements.Button(385, 295, 'DARK', constants.SPECIAL, [constants.keys['d']], self.toDark))
		self.elements.append(elements.Button(600, 295, 'SMW', constants.SPECIAL, [constants.keys['s']], self.toSMW))
		self.elements.append(elements.Button(constants.POS['RIGHT'], constants.POS['DOWN'], 'BACK', constants.MAIN_MENU, [constants.keys['b']]))

class LoseMenu(Menu):
	def initActors(self):
		#part of the screen that this menu uses
		self.updateRect = Rect(0, 100, constants.SCREEN_SIZE[0], 300)

		#actors
		self.elements = []
		self.elements.append(elements.Label(None, 150, 'You\'ve LOST :(', 80, False, constants.BLACK))
		self.elements.append(elements.Label(None, 350, 'Press \'Enter\' to restart.', 30, False, constants.BLACK))
		self.elements.append(elements.Button(constants.POS['LEFT'], None, 'Menu', self.parent_menu, [constants.keys['m']]))
		self.elements.append(elements.Button(None, None, 'Restart', constants.RESTART, [constants.keys['r'], constants.keys['enter']]))

class WinMenu(Menu):
	def initActors(self):
		#where to go when quitting this menu
		self.parent_menu = constants.STAGE_MENU
		
		#part of the screen that this menu uses
		self.updateRect = Rect(0, 100, constants.SCREEN_SIZE[0], 300)

		#actors
		self.elements = []
		self.elements.append(elements.Label(None, 150, 'You\'ve WON :)', 80, False, constants.BLACK))
		self.elements.append(elements.Label(None, 350, 'Press \'Enter\' to start next stage.', 30, False, constants.BLACK))
		self.elements.append(elements.Button(constants.POS['LEFT'], None, 'Menu', constants.STAGE_MENU, [constants.keys['m']]))
		self.elements.append(elements.Button(None, None, 'Restart', constants.RESTART, [constants.keys['r']]))
		self.elements.append(elements.Button(constants.POS['RIGHT'], None, 'Next', constants.NEXT, [constants.keys['enter']]))

class InsertRankMenu(Menu):
	def initActors(self):
		#where to go when quitting this menu
		self.parent_menu = constants.SURVIVAL_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 200, constants.SCREEN_SIZE[0], 200)

		#actors
		self.elements = []
		self.elements.append(elements.Label(None, 350, 'Type in your name.', 30, False, constants.BLACK))
		
		self.text_box = elements.TextBox()

	def update(self, screen):
		done = False
		action = self.parent_menu
		clock = pygame.time.Clock()
		pygame.mouse.set_cursor(*pygame.cursors.tri_left)
		listShortcut = {}
		
		mouse = pygame.mouse
		self.initActors()

		count = 0

		for e in self.elements:
			for s in e.shortcut:
				listShortcut[s] = e
		if constants.NOKEY in listShortcut:
			del listShortcut[constants.NOKEY]

		while not done:
			letter = None
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return constants.QUIT
				elif event.type == pygame.KEYDOWN:
					if event.key != pygame.K_LSHIFT and event.key != pygame.K_RSHIFT and event.key != constants.keys['enter']:
						letter = event.key
					elif event.key == constants.keys['enter']:
						data.new_player = self.text_box.b_text
						data.insert_rank()
						return self.parent_menu
					else:
						letter = constants.keys['shift_in']
				elif event.type == pygame.KEYUP:
					if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
						letter = constants.keys['shift_out']
		
			#button PLAY
			screen.fill(theme.backgroundColor)
			for b in self.elements:
				done, action = b.hover(mouse, done, action)
				b.blit(screen)
			count += 1

			self.text_box.blit(screen, letter)

			pygame.display.update(self.updateRect)
			clock.tick(200)

		return action