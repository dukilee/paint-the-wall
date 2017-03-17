import constants
import pygame
import sprites
import sys

from pygame.locals import *

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
	def __init__(self, x = None, y = None, b_text = '', action = -1, text_size = 25, b_bold = True, off_t_color = constants.DARK_GREEN, on_t_color = constants.MED_GREEN):
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

		self.action = action # what will the button peform when clicked (see constants.py)

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
				done = True
				action = self.action
			else: #pass over
				self.turn_on()
		else: #away from button 
			self.turn_off()

		return done, action

class miniButton(Button):
	def set_button_sprites(self):
		self.off_button = sprites.sprite('small_grey_off_button.png')
		self.on_button = sprites.sprite('small_black_on_button.png')
		self.present_button = self.off_button

class Label(Elements):	
	def __init__(self, x = None, y = None, b_text = '', text_size = 50, b_bold = True, b_color = constants.WHITE, t_color = constants.BLACK):
		self.b_text = b_text # text to be shown
		self.fontButton = pygame.font.SysFont('Calibri', text_size, b_bold, False) # to create text objects
		self.text = self.fontButton.render(b_text, True, t_color) # text object

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
	
		#actors
		mouse = pygame.mouse
		self.initActors()		
		while not done:
			#player commands
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					#done = True
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == constants.KEY_q:
						return self.action

			#drawing background
			screen.fill(constants.WHITE)

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
		self.elements.append(Label(260, 30, 'About', 45))
		self.elements.append(Button(650, 500, 'BACK', constants.MAIN_MENU, 40, False))

class AchievementsMenu(Menu):
	def initActors(self):
		#where to go when quitting this menu
		self.action = constants.MAIN_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

		#actors
		self.elements = []
		self.elements.append(Label(260, 30, 'Achievements', 45))
		self.elements.append(Button(650, 500, 'BACK', constants.MAIN_MENU, 40, False))

class MainMenu(Menu):
	def initActors(self):
		#where to go when quitting this menu
		self.action = constants.QUIT

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

		#actors
		self.elements = []
		self.elements.append(Label(None, 100, 'Paint-The-Wall!'))
		self.elements.append(Button(None, 200, 'STAGES', constants.STAGE_MENU))
		self.elements.append(Button(None, 275, 'SURVIVAL', constants.SURVIVAL_MENU))
		self.elements.append(Button(None, 350, 'ACHIEVEMENTS', constants.ACHIEVEMENTS_MENU))
		self.elements.append(Button(None, 425, 'ABOUT', constants.ABOUT_MENU))
		self.elements.append(Button(None, 500, 'QUIT', constants.QUIT))

class PauseMenu(Menu):
	def initActors(self):
		#where to go when quitting this menu
		self.action = constants.MAIN_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 200, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1]-400)

		#actors
		self.elements = []
		self.elements.append(Button(100, 250, 'Restart', constants.RESTART, 40, False))
		self.elements.append(Button(275, 250, 'Resume', constants.UNDEFINED, 40, False))
		self.elements.append(Button(450, 250, 'Menu', constants.MAIN_MENU, 40, False))

class StageMenu(Menu):
	def initActors(self):
		#where to go when quitting this menu
		self.action = constants.MAIN_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

		#actors
		self.elements = [Button(260, 500, 'Back', constants.MAIN_MENU)]
		self.elements.append(Label(260, 30, 'Stages', 45))
		for i in range(10):
			self.elements.append(miniButton(80 + (i % 5) * 145, 150 + int(i / 5) * 225, '{}'.format(i + 1), constants.STAGE1 + i))

class StatsMenu(Menu):
	def initActors(self):		
		#where to go when quitting this menu
		self.action = constants.MAIN_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

		#actors
		self.elements = []
		self.elements.append(Label(260, 30, 'Stats', 45))
		self.elements.append(Button(450, 250, 'BACK', constants.MAIN_MENU, 40, False))

class SurvivalMenu(Menu):
	def initActors(self):
		#where to go when quitting this menu
		self.action = constants.MAIN_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

		#actors
		self.elements = []
		self.elements.append(Label(260, 30, 'Survival', 45))
		self.elements.append(Button(50, 500, 'PLAY', constants.STAGE_SURVIVAL, 40, False))
		self.elements.append(Button(275, 500, 'RANK', constants.RANK_MENU, 40, False))
		self.elements.append(Button(450, 500, 'BACK', constants.MAIN_MENU, 40, False))

class RankMenu(Menu):
	def initActors(self):		
		#where to go when quitting this menu
		self.action = constants.SURVIVAL_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

		#actors
		self.elements = []
		self.elements.append(Label(260, 30, 'Ranking', 45))
		self.elements.append(Button(450, 250, 'BACK', constants.SURVIVAL_MENU, 40, False))
