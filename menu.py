import constants
import pygame
import sprites
import themeManager
import theme
import data
import animation

from pygame.locals import *

# Falta o tutorial!

class Elements:	
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def turn_on(self):
		self.present_button = self.on_button_sprite
		self.presentColor = self.onButtonColor
		self.text = self.fontButton.render(self.b_text, True, self.on_t_color)

	def turn_off(self):
		#self.b_color = self.off_b_color
		self.present_button = self.off_button_sprite
		self.presentColor = self.offButtonColor
		self.text = self.fontButton.render(self.b_text, True, self.off_t_color)

	def centralize(self, rec):
		return [self.x + int((self.width - rec.width)/2), self.y + int((self.height - rec.height)/2)]

	# update button on screen
	def blit(self, screen):
		pass

	# checks if mouse is hovering this area
	def ishovering(self, mouse):
		return False

	# activate button if hovering, deactivate if not
	def hover(self, mouse, done, action):
		return done, action

class Button(Elements):
	def __init__(self, x = None, y = None, b_text = '', action = constants.UNCLICKABLE, shortcut = [constants.NOKEY], callAction = None, text_size = constants.BUTTON_FONT_SIZE, b_bold = True, off_t_color = None, on_t_color = None):
		if off_t_color is None:
			off_t_color = theme.offButtonTextColor
		if on_t_color is None:
			on_t_color = theme.onButtonTextColor


		self.off_t_color = off_t_color # inactive text color
		self.on_t_color = on_t_color # active text color
		self.presentColor = theme.offButtonColor

		self.b_text = b_text # text to be shown on button
		self.fontButton = pygame.font.SysFont('Calibri', text_size, b_bold, False) # to create text objects
		self.text = self.fontButton.render(b_text, True, off_t_color) # text object

		self.set_button_sprites()
		if self.on_button_sprite == None:
			self.width = constants.BUTTON_WIDTH
			self.height = constants.BUTTON_HEIGHT
			self.set_button_sprites()
		else:
			self.width = self.off_button_sprite.rec.width
			self.height = self.off_button_sprite.rec.height

		if x == None: # centralize x on screen
			x = int((constants.SCREEN_SIZE[0] - self.width)/2)
		if y == None: # centralize y on screen
			y = int((constants.SCREEN_SIZE[1] - self.height)/2)

		Elements.__init__(self, x, y)
		self.body = [x, y, self.width, self.height] # rectangular area of the element
		self.pressed = False

		self.action = action # what will the button peform when clicked (see constants.py)
		self.shortcut = shortcut
		self.callAction = callAction
		self.set_button_sprites()
		self.update = False

	def set_button_sprites(self):
		self.off_button_sprite = theme.offButtonSprite
		self.on_button_sprite = theme.onButtonSprite
		self.onButtonColor = theme.onButtonColor
		self.offButtonColor = theme.offButtonColor
		self.present_button = self.off_button_sprite


	def blit(self, screen):
		text_rect = self.text.get_rect()
		if self.present_button != None:
			screen.blit(self.present_button.img, self.centralize(self.present_button.rec))
		else:
			pygame.draw.rect(screen, self.presentColor, [self.x, self.y, self.width, self.height])
		screen.blit(self.text, self.centralize(text_rect))

	def ishovering(self, mouse):
		return mouse[0]>=self.x and mouse[0]<=self.x + self.width and mouse[1]>=self.y and mouse[1]<=self.y + self.height

	# activate button if hovering, deactivate if not
	def hover(self, mouse, done, action):
		if self.action != constants.UNCLICKABLE and self.ishovering(mouse.get_pos()):
			if mouse.get_pressed()[0]: #on click
				self.pressed = True
			else:
				if self.pressed: #release
					done = True
					action = self.action
					if self.callAction != None:
						self.callAction()
				else: #pass over
					self.turn_on()
				self.pressed = False
		else: #away from button
			self.turn_off()

		return done, action

class ButtonOver(Button):
	# activate button if hovering, deactivate if not
	def hover(self, mouse, done, action):
		if self.ishovering(mouse.get_pos()):
			self.callAction()
		return done, action

class miniButton(Button):
	def set_button_sprites(self):
		self.off_button_sprite = theme.offButtonSpriteMini
		self.on_button_sprite = theme.offButtonSpriteMini
		self.offButtonColor = theme.offButtonColor
		self.onButtonColor = theme.onButtonColor
		self.present_button = self.off_button_sprite
		self.presentColor = self.offButtonColor
		self.width = constants.BUTTON_MINI_WIDTH
		self.height = constants.BUTTON_MINI_HEIGHT

class Label(Elements):	
	def __init__(self, x = None, y = None, b_text = '', text_size = constants.LABEL_FONT_SIZE, b_bold = True, b_color = None, t_color = None, update = None):
		if t_color is None:
			t_color = theme.labelTextColor
		if b_color is None:
			b_color = theme.labelBackColor

		self.b_text = b_text # text to be shown
		self.fontButton = pygame.font.SysFont('Calibri', text_size, b_bold, False) # to create text objects
		self.text = self.fontButton.render(b_text, True, t_color) # text object
		self.shortcut = [constants.NOKEY]
		rec = self.text.get_rect()
		self.width = rec.width
		self.height = rec.height

		if x == None: # centralize x on screen
			x = int((constants.SCREEN_SIZE[0] - rec.width)/2)
		if y == None: # centralize y on screen
			y = int((constants.SCREEN_SIZE[1] - rec.height)/2)

		Elements.__init__(self, x, y)

		self.b_color = b_color # inactive color
		self.t_color = t_color # inactive text color
		self.update = update #if need to change while the software is running

	def blit(self, screen):
		if self.update != None:
			self.text = self.fontButton.render(self.update(), True, self.t_color)  # text object

		text_rect = self.text.get_rect()
		screen.blit(self.text, self.centralize(text_rect))	

class Rectangle(Elements):
	def __init__(self, x, y, width, height, b_color = constants.BLACK):
		self.width = width
		self.height = height
		self.shortcut = [constants.NOKEY]

		Elements.__init__(self, x, y)

		self.b_color = b_color # inactive color

	def blit(self, screen):
		pygame.draw.rect(screen, self.b_color, [self.x, self.y, self.width, self.height])
		# text_rect = self.text.get_rect()
		# screen.blit(self.text, self.centralize(text_rect))

class Menu:
	def __init__(self):
		self.elements = []
		self.animations = []

	# virtual method
	def initActors(self):
		pass

	def update(self, screen, anotherElement = None):
		#constants
		clock = pygame.time.Clock()
		done = False
		action = constants.QUIT
		pygame.mouse.set_cursor(*pygame.cursors.tri_left)
		listShortcut = {}
		#actors
		mouse = pygame.mouse
		self.initActors()		

		if anotherElement != None:
			self.elements.append(Label(None, 200, anotherElement, 40, False, constants.BLACK))

		count = 0

		for e in self.elements:
			for s in e.shortcut:
				listShortcut[s] = e
		if constants.NOKEY in listShortcut:
			del listShortcut[constants.NOKEY]

		while not done:
			for b in self.elements:
				pass
			#player commands
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return constants.QUIT
				elif event.type == pygame.KEYDOWN:
					if event.key == constants.keys['q']:
						return self.action
					if event.key in listShortcut:
						done = True
						action = listShortcut[event.key].action

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
		#where to go when quitting this menu
		self.action = constants.MAIN_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

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
		self.overString = 'Conquer the hole screen'

	def instructionsText(self):
		copy = self.overString
		self.overString = '<Pass mouse over achievements to get info>'
		return copy

	def initActors(self):
		#where to go when quitting this menu
		self.action = constants.MAIN_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])
		self.overString = '<Pass mouse over achievements>'

		#actors
		self.elements = []
		self.elements.append(Label(None, constants.POS['UP'], 'Achievements'))
		self.elements.append(Rectangle(10, constants.POS['DOWN'], 460, 50, theme.labelTextLLColor))
		self.elements.append(Label(130, constants.POS['DOWN']+15, 'Instructions a lot of it', 30, False, None, None, self.instructionsText))
		# self.elements.append(Label(constants.POS['RIGHT'], 300, '00:00:00'             ,    30, False, None, None, self.timeText))
		self.elements.append(Button(constants.POS['RIGHT'], constants.POS['DOWN'], 'BACK', constants.MAIN_MENU, [constants.keys['b'], constants.keys['backspace']]))

		if data.i['doubleKill'] == 1:
			self.elements.append(Label(50, 225, 'Double Kill', 30, False, None, None))
			self.elements.append(ButtonOver(50, 150, 'DK', constants.UNCLICKABLE, [constants.NOKEY], self.toDK, constants.BUTTON_FONT_SIZE, True, constants.DARK_GREEN, constants.DARK_GREEN))
		else:
			self.elements.append(Label(50, 225, 'Double Kill', 30, False, theme.labelBackColor, theme.labelTextLowColor))
			self.elements.append(ButtonOver(50, 150, 'DK', constants.UNCLICKABLE, [constants.NOKEY], self.toDK, constants.BUTTON_FONT_SIZE, True, constants.RED, constants.RED))

		if data.i['worldEmperor'] == 1:
			self.elements.append(Label(300, 225, 'World Emperor', 30, False, theme.labelBackColor, theme.labelTextColor))
			self.elements.append(ButtonOver(300, 150, 'WE', constants.UNCLICKABLE, [constants.NOKEY], self.toWE, constants.BUTTON_FONT_SIZE, True, constants.DARK_GREEN, constants.DARK_GREEN))
		else:
			self.elements.append(Label(300, 225, 'World Emperor', 30, False, theme.labelBackColor, theme.labelTextLowColor))
			self.elements.append(ButtonOver(300, 150, 'WE', constants.UNCLICKABLE, [constants.NOKEY], self.toWE, constants.BUTTON_FONT_SIZE, True, constants.RED, constants.RED))

		if data.i['yogaMaster'] == 1:
			self.elements.append(Label(550, 225, 'Yoga Master', 30, False, theme.labelBackColor, theme.labelTextColor))
			self.elements.append(ButtonOver(550, 150, 'YM', constants.UNCLICKABLE, [constants.NOKEY], self.toYM, constants.BUTTON_FONT_SIZE, True, constants.DARK_GREEN, constants.DARK_GREEN))
		else:
			self.elements.append(Label(550, 225, 'Yoga Master', 30, False, theme.labelBackColor, theme.labelTextLowColor))
			self.elements.append(ButtonOver(550, 150, 'YM', constants.UNCLICKABLE, [constants.NOKEY], self.toYM, constants.BUTTON_FONT_SIZE, True, constants.RED, constants.RED))
		
class MainMenu(Menu):
	def initActors(self):
		#where to go when quitting this menu
		self.action = constants.QUIT

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

		#actors
		self.elements = []
		self.elements.append(Label(None, constants.POS['UP'], 'Paint-The-Wall!'))
		self.elements.append(Button(None, 150, 'STAGES', constants.STAGE_MENU))
		self.elements.append(Button(None, 219, 'SURVIVAL', constants.SURVIVAL_MENU))
		self.elements.append(Button(None, 288, 'ACHIEVEMENTS', constants.ACHIEVEMENTS_MENU))
		self.elements.append(Button(None, 357, 'STATS', constants.STATS_MENU))
		self.elements.append(Button(None, 426, 'SETTINGS', constants.SETTINGS_MENU))
		self.elements.append(Button(None, 495, 'QUIT', constants.QUIT))

		#animations
		self.animations.append(animation.MainMenuAnimation())

class PauseMenu(Menu):
	def initActors(self):
		#where to go when quitting this menu
		self.action = constants.MAIN_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 100, constants.SCREEN_SIZE[0], 300)

		#actors
		self.elements = []
		self.elements.append(Label(None, 350, 'Press \'p\' to resume.', 30, False, constants.BLACK))
		self.elements.append(Button(constants.POS['LEFT'], None, 'Menu', constants.MAIN_MENU, [constants.keys['m']]))
		self.elements.append(Button(None, None, 'Restart', constants.RESTART, [constants.keys['r']]))
		self.elements.append(Button(constants.POS['RIGHT'], None, 'Resume', constants.UNDEFINED, [constants.keys['p'], constants.keys['Enter']]))

class StartMenu(Menu):
	def initActors(self):
		#where to go when quitting this menu
		self.action = constants.MAIN_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 100, constants.SCREEN_SIZE[0], 300)

		#actors
		self.elements = []
		self.elements.append(Label(None, 350, 'Press \'Enter\' to start.', 30, False, constants.BLACK))
		self.elements.append(Button(None, None, 'Start', constants.UNDEFINED, [constants.keys['s'], constants.keys['Enter']]))
		self.elements.append(Button(constants.POS['LEFT'], None, 'Menu', constants.MAIN_MENU, [constants.keys['m']]))

class StageMenu(Menu):
	def initActors(self):
		#where to go when quitting this menu
		self.action = constants.MAIN_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

		#actors
		self.elements = [Button(constants.POS['RIGHT'], constants.POS['DOWN'], 'Back', constants.MAIN_MENU, [constants.keys['b'], constants.keys['backspace']])]
		self.elements.append(miniButton(constants.POS['RIGHT']+130, 240, '>', constants.STAGE_MENU_2, [constants.KEY_RIGHT]))
		self.elements.append(Label(None, constants.POS['UP'], 'Stages'))
		for i in range(10):
			if i >= data.i['lastUnlockedStages']:
				self.elements.append(Label(170 + (i % 5) * 110, 190 + int(i / 5) * 150,'{}'.format(i + 1), 30, False, constants.BLACK, theme.labelTextLLColor))
			else:
				self.elements.append(miniButton(150 + (i % 5) * 110, 170 + int(i / 5) * 150, '{}'.format(i + 1), constants.STAGE1 + i))

class StageMenu2(Menu):
	def initActors(self):
		#where to go when quitting this menu
		self.action = constants.MAIN_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

		#actors
		self.elements = [Button(constants.POS['RIGHT'], constants.POS['DOWN'], 'Back', constants.MAIN_MENU, [constants.keys['b'], constants.keys['backspace']])]
		self.elements.append(
			miniButton(constants.POS['LEFT']+10, 240, '<', constants.STAGE_MENU, [constants.KEY_LEFT]))

		self.elements.append(Label(None, constants.POS['UP'], 'Stages'))
		for i in range(10, 20):
			if i >= data.i['lastUnlockedStages']:
				self.elements.append(Label(170 + (i % 5) * 110, 190 + int((i-10) / 5) * 150,'{}'.format(i + 1), 30, False, constants.BLACK, theme.labelTextLLColor))
			else:
				self.elements.append(miniButton(150 + (i % 5) * 110, 170 + int((i-10) / 5) * 150, '{}'.format(i + 1), constants.STAGE1 + i))


class StatsMenu(Menu):
	def timeText(self):
		actualTime = data.getActualTime()
		return '{0:0=2d}:{1:0=2d}:{2:0=2d}'.format(int(actualTime / 3600), (int(actualTime / 60)) % 60,
											   (actualTime) % 60)

	def initActors(self):
		#where to go when quitting this menu
		self.action = constants.MAIN_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

		#actors
		self.elements = []
		self.elements.append(Label(None, constants.POS['UP'], 'Stats'))
		self.elements.append(Button(constants.POS['RIGHT'], constants.POS['DOWN'], 'BACK', constants.MAIN_MENU, [constants.keys['b'], constants.keys['backspace']]))
		self.elements.append(Label(constants.POS['LEFT'], 300, 'Time Played:', 30, False))
		self.elements.append(Label(constants.POS['LEFT'], 350, 'Blocks Destructed:', 30, False))
		self.elements.append(Label(constants.POS['LEFT'], 400, 'Balls Killed:', 30, False))
		self.elements.append(Label(constants.POS['LEFT'], 450, 'Deaths:', 30, False))
		self.elements.append(Label(constants.POS['RIGHT'], 300, '00:00:00', 30, False, None, None, self.timeText))
		self.elements.append(Label(constants.POS['RIGHT'], 350, '{}'.format(data.i['blocksConquered']), 30, False))
		self.elements.append(Label(constants.POS['RIGHT'], 400, '{}'.format(data.i['ballsDestructed']), 30, False))
		self.elements.append(Label(constants.POS['RIGHT'], 450, '{}'.format(data.i['deaths']), 30, False))


class SurvivalMenu(Menu):
	def initActors(self):
		#where to go when quitting this menu
		self.action = constants.MAIN_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

		#actors
		self.elements = []
		self.elements = []
		self.elements.append(Label(None, constants.POS['UP'], 'Survival'))
		self.elements.append(Button(constants.POS['LEFT'], constants.POS['DOWN'], 'PLAY', constants.STAGE_SURVIVAL, [constants.keys['p'], constants.keys['Enter']]))
		self.elements.append(Button(None, constants.POS['DOWN'], 'RANK', constants.RANK_MENU, [constants.keys['r']]))
		self.elements.append(Button(constants.POS['RIGHT'], constants.POS['DOWN'], 'BACK', constants.MAIN_MENU, [constants.keys['b']]))

class SettingsMenu(Menu):

	def toBasic(self):
		themeManager.changeTheme(constants.BASIC_THEME)

	def toDark(self):
		themeManager.changeTheme(constants.DARK_THEME)

	def initActors(self):
		#where to go when quitting this menu
		self.action = constants.MAIN_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

		#actors
		self.elements = []
		self.elements.append(Label(None, constants.POS['UP'], 'Settings'))
		self.elements.append(Label(constants.POS['LEFT'], 415, 'Theme:', 40, False))
		self.elements.append(Button(None, 400, 'BASIC', constants.RESTART, [constants.keys['p'], constants.keys['Enter']], self.toBasic))
		self.elements.append(Button(constants.POS['RIGHT'], 400, 'DARK', constants.RESTART, [constants.keys['p'], constants.keys['Enter']], self.toDark))
		self.elements.append(Button(constants.POS['RIGHT'], constants.POS['DOWN'], 'BACK', constants.MAIN_MENU, [constants.keys['b']]))

class RankMenu(Menu):
	def initActors(self):		
		#where to go when quitting this menu
		self.action = constants.SURVIVAL_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

		#actors
		self.elements = []
		self.elements.append(Label(None, constants.POS['UP'], 'Ranking'))
		self.elements.append(Button(450, 250, 'BACK', constants.SURVIVAL_MENU, [constants.keys['b']]))

class LoseMenu(Menu):
	def initActors(self):
		#where to go when quitting this menu
		self.action = constants.MAIN_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 100, constants.SCREEN_SIZE[0], 300)

		#actors
		self.elements = []
		self.elements.append(Label(None, 150, 'You\'ve LOST :(', 80, False, constants.BLACK))
		self.elements.append(Label(None, 350, 'Press \'Enter\' to restart.', 30, False, constants.BLACK))
		self.elements.append(Button(constants.POS['LEFT'], None, 'Menu', constants.MAIN_MENU, [constants.keys['m']]))
		self.elements.append(Button(None, None, 'Restart', constants.RESTART, [constants.keys['r'], constants.keys['Enter']]))

class WinMenu(Menu):
	def initActors(self):
		#where to go when quitting this menu
		self.action = constants.MAIN_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 100, constants.SCREEN_SIZE[0], 300)

		#actors
		self.elements = []
		self.elements.append(Label(None, 150, 'You\'ve WON :)', 80, False, constants.BLACK))
		self.elements.append(Label(None, 350, 'Press \'Enter\' to start next stage.', 30, False, constants.BLACK))
		self.elements.append(Button(constants.POS['LEFT'], None, 'Menu', constants.MAIN_MENU, [constants.keys['m']]))
		self.elements.append(Button(None, None, 'Restart', constants.RESTART, [constants.keys['r']]))
		self.elements.append(Button(constants.POS['RIGHT'], None, 'Next', constants.NEXT, [constants.keys['Enter']]))
