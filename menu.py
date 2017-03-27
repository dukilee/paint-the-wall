import constants
import pygame
import sprites
import data
import sys
import time

from pygame.locals import *

# Falta o tutorial!

class Elements:	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def turn_on(self):
		self.present_button = self.on_button
		self.text = self.fontButton.render(self.b_text, True, self.on_t_color)

	def turn_off(self):
		#self.b_color = self.off_b_color
		self.present_button = self.off_button
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
	def __init__(self, x = None, y = None, b_text = '', action = constants.UNCLICKABLE, shortcut = [constants.NOKEY], text_size = constants.BUTTON_FONT_SIZE, b_bold = True, off_t_color = constants.DARK_GREEN, on_t_color = constants.MED_GREEN):
		self.off_t_color = off_t_color # inactive text color
		self.on_t_color = on_t_color # active text color

		self.b_text = b_text # text to be shown on button
		self.fontButton = pygame.font.SysFont('Calibri', text_size, b_bold, False) # to create text objects
		self.text = self.fontButton.render(b_text, True, off_t_color) # text object

		self.set_button_sprites()

		self.width = self.off_button.rec.width
		self.height = self.off_button.rec.height

		if x == None: # centralize x on screen
			x = int((constants.SCREEN_SIZE[0] - self.width)/2)
		if y == None: # centralize y on screen
			y = int((constants.SCREEN_SIZE[1] - self.height)/2)

		Elements.__init__(self, x, y)
		self.body = [x, y, self.width, self.height] # rectangular area of the element
		self.pressed = False

		self.action = action # what will the button peform when clicked (see constants.py)
		self.shortcut = shortcut

	def set_button_sprites(self):
		self.off_button = sprites.sprite('grey_off_button.png')
		self.on_button = sprites.sprite('black_on_button.png')
		self.present_button = self.off_button

	def blit(self, screen):
		text_rect = self.text.get_rect()
		screen.blit(self.present_button.img, self.centralize(self.present_button.rec))
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
				else: #pass over
					self.turn_on()
				self.pressed = False
		else: #away from button
			self.turn_off()

		return done, action

class miniButton(Button):
	def set_button_sprites(self):
		self.off_button = sprites.sprite('small_grey_off_button.png')
		self.on_button = sprites.sprite('small_black_on_button.png')
		self.present_button = self.off_button

class Label(Elements):	
	def __init__(self, x = None, y = None, b_text = '', text_size = constants.LABEL_FONT_SIZE, b_bold = True, b_color = constants.WHITE, t_color = constants.BLACK):
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

	def blit(self, screen):
		text_rect = self.text.get_rect()
		screen.blit(self.text, self.centralize(text_rect))	

class Menu:
	# virtual method
	def initActors(self):
		pass

	def update(self, screen):
		#constants
		clock = pygame.time.Clock()
		done = False;
		action = constants.QUIT
		pygame.mouse.set_cursor(*pygame.cursors.tri_left)
		listShortcut = {}
		#actors
		mouse = pygame.mouse
		self.initActors()		

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
			for b in self.elements:
				done, action = b.hover(mouse, done, action)
				b.blit(screen)

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
	def initActors(self):
		#where to go when quitting this menu
		self.action = constants.MAIN_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

		#actors
		self.elements = []
		self.elements.append(Label(None, constants.POS['UP'], 'Achievements'))
		self.elements.append(Button(constants.POS['RIGHT'], constants.POS['DOWN'], 'BACK', constants.MAIN_MENU, [constants.keys['b'], constants.keys['backspace']]))

		if data.i['doubleKill'] == 1:
			self.elements.append(Label(50, 225, 'Double Kill', 30, False, constants.WHITE, constants.BLACK))
			self.elements.append(Button(50, 150, 'DK', constants.UNCLICKABLE, [constants.NOKEY], constants.BUTTON_FONT_SIZE, True, constants.DARK_GREEN, constants.DARK_GREEN))
		else:
			self.elements.append(Label(50, 225, 'Double Kill', 30, False, constants.WHITE, constants.GRAY))
			self.elements.append(Button(50, 150, 'DK', constants.UNCLICKABLE, [constants.NOKEY], constants.BUTTON_FONT_SIZE, True, constants.RED, constants.RED))

		if data.i['worldEmperor'] == 1:
			self.elements.append(Label(300, 225, 'World Emperor', 30, False, constants.WHITE, constants.BLACK))
			self.elements.append(Button(300, 150, 'WE', constants.UNCLICKABLE, [constants.NOKEY], constants.BUTTON_FONT_SIZE, True, constants.DARK_GREEN, constants.DARK_GREEN))
		else:
			self.elements.append(Label(300, 225, 'World Emperor', 30, False, constants.WHITE, constants.GRAY))
			self.elements.append(Button(300, 150, 'WE', constants.UNCLICKABLE, [constants.NOKEY], constants.BUTTON_FONT_SIZE, True, constants.RED, constants.RED))

		if data.i['yogaMaster'] == 1:
			self.elements.append(Label(550, 225, 'Yoga Master', 30, False, constants.WHITE, constants.BLACK))
			self.elements.append(Button(550, 150, 'YM', constants.UNCLICKABLE, [constants.NOKEY], constants.BUTTON_FONT_SIZE, True, constants.DARK_GREEN, constants.DARK_GREEN))
		else:
			self.elements.append(Label(550, 225, 'Yoga Master', 30, False, constants.WHITE, constants.GRAY))
			self.elements.append(Button(550, 150, 'YM', constants.UNCLICKABLE, [constants.NOKEY], constants.BUTTON_FONT_SIZE, True, constants.RED, constants.RED))
		
class MainMenu(Menu):
	def initActors(self):
		#where to go when quitting this menu
		self.action = constants.QUIT

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

		#actors
		self.elements = []
		self.elements.append(Label(None, constants.POS['UP'], 'Paint-The-Wall!'))
		self.elements.append(Button(None, 200, 'STAGES', constants.STAGE_MENU))
		self.elements.append(Button(None, 275, 'SURVIVAL', constants.SURVIVAL_MENU))
		self.elements.append(Button(None, 350, 'ACHIEVEMENTS', constants.ACHIEVEMENTS_MENU))
		self.elements.append(Button(None, 425, 'STATS', constants.STATS_MENU))
		self.elements.append(Button(None, 500, 'QUIT', constants.QUIT))

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
		self.elements.append(Label(None, constants.POS['UP'], 'Stages'))
		for i in range(10):
			if i >= data.i['lastUnlockedStages']:
				self.elements.append(Label(80 + (i % 5) * 145, 170 + int(i / 5) * 150,'{}'.format(i + 1), 30, False))
			else:
				self.elements.append(miniButton(80 + (i % 5) * 145, 170 + int(i / 5) * 150, '{}'.format(i + 1), constants.STAGE1 + i))

class StatsMenu(Menu):
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

		data.actualTime = int(time.clock() - data.startTime)
		self.elements.append(Label(constants.POS['RIGHT'], 300, '{0:0=2d}:{1:0=2d}:{2:0=2d}'.format(int(data.actualTime/3600), (int(data.actualTime/60))%60, (data.actualTime)%60), 30, False))
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
