import constants
import pygame
import sys

from pygame.locals import *

class Elements:	
	#virtual constructor
	def __init__():
		pass

	# update color: on
	def on_color(self):
		self.b_color = self.on_b_color
		self.text = self.fontButton.render(self.b_text, True, self.on_t_color)

	# update color: off
	def off_color(self):
		self.b_color = self.off_b_color
		self.text = self.fontButton.render(self.b_text, True, self.off_t_color)

	# draw button on screen
	def draw(self, screen):
		if self.b_color != constants.NONE:
			pygame.draw.rect(screen, self.b_color, self.body)

	# update button on screen
	def blit(self, screen):
		text_rect = self.text.get_rect()
		screen.blit(self.text, [self.x + self.width/2 - text_rect.width/2, self.y + self.height/2 - text_rect.height/2])


	# checks if mouse is hovering this area
	def ishovering(self, mouse):
		return mouse[0]>=self.x and mouse[0]<=self.x + self.width and mouse[1]>=self.y and mouse[1]<=self.y + self.height

	# activate button if hovering, deactivate if not
	def hover(self, mouse, done, action):
		return done, action

class Button(Elements):	
	def __init__(self, x, y, w, h, b_text = '', action = -1, b_text_size = 60, b_bold = True, off_b_color = constants.BLUE, off_t_color = constants.DARK_GREEN, on_b_color = constants.MED_BLUE, on_t_color = constants.MED_GREEN):
		self.x = x
		self.y = y
		self.width = w
		self.height = h
		self.body = [x, y, w, h] # rectangular area of the button

		self.off_b_color = off_b_color # inactive button color
		self.off_t_color = off_t_color # inactive text color
		self.on_b_color = on_b_color # active button color
		self.on_t_color = on_t_color # active text color

		self.b_color = off_b_color # present button color
		self.b_text = b_text # text to be shown on button
		self.fontButton = pygame.font.SysFont('Calibri', b_text_size, b_bold, False) # to create text objects
		self.text = self.fontButton.render(b_text, True, off_t_color) # text object

		self.action = action # what will the button peform when clicked (see constants.py)

	# checks if mouse is hovering this area
	def ishovering(self, mouse):
		return mouse[0]>=self.x and mouse[0]<=self.x + self.width and mouse[1]>=self.y and mouse[1]<=self.y + self.height

	# activate button if hovering, deactivate if not
	def hover(self, mouse, done, action):
		if self.action != constants.UNCLICKABLE and self.ishovering(mouse.get_pos()):
			if mouse.get_pressed()[0]: #on click
				done = True
				action = self.action
			else: #pass over
				self.on_color()
		else: #away from button 
			self.off_color()

		return done, action

class Label(Elements):	
	def __init__(self, x, y, w, h, b_text = '', b_text_size = 60, b_bold = True, off_b_color = constants.NONE, off_t_color = constants.BLACK, on_b_color = constants.MED_BLUE, on_t_color = constants.MED_GREEN):
		self.x = x
		self.y = y
		self.width = w
		self.height = h
		self.body = [x, y, w, h] # rectangular area of the button

		self.off_b_color = off_b_color # inactive color
		self.off_t_color = off_t_color # inactive text color

		self.b_color = off_b_color # present color
		self.b_text = b_text # text to be shown
		self.fontButton = pygame.font.SysFont('Calibri', b_text_size, b_bold, False) # to create text objects
		self.text = self.fontButton.render(b_text, True, off_t_color) # text object

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
				b.draw(screen)
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
		self.elements.append(Label(260, 30, 250, 70, 'About', 45))
		self.elements.append(Button(650, 500, 150, 100, 'BACK', constants.MAIN_MENU, 40, False))

class AchievementsMenu(Menu):
	def initActors(self):
		#where to go when quitting this menu
		self.action = constants.MAIN_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

		#actors
		self.elements = []
		self.elements.append(Label(260, 30, 250, 70, 'Achievements', 45))
		self.elements.append(Button(650, 500, 150, 100, 'BACK', constants.MAIN_MENU, 40, False))

class MainMenu(Menu):
	def initActors(self):
		#where to go when quitting this menu
		self.action = constants.QUIT

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

		#actors
		self.elements = []
		self.elements.append(Label(260, 100, 250, 70, 'Paint-The-Wall!'))
		self.elements.append(Button(50, 200, 400, 50, 'STAGES', constants.STAGE_MENU))
		self.elements.append(Button(50, 275, 400, 50, 'SURVIVAL', constants.SURVIVAL_MENU))
		self.elements.append(Button(50, 350, 400, 50, 'ACHIEVEMENTS', constants.ACHIEVEMENTS_MENU))
		self.elements.append(Button(50, 425, 400, 50, 'ABOUT', constants.ABOUT_MENU))
		self.elements.append(Button(50, 500, 400, 50, 'QUIT', constants.QUIT))

class PauseMenu(Menu):
	def initActors(self):
		#where to go when quitting this menu
		self.action = constants.MAIN_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 200, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1]-400)

		#actors
		self.elements = []
		self.elements.append(Button(100, 250, 150, 100, 'Restart', constants.RESTART, 40, False))
		self.elements.append(Button(275, 250, 150, 100, 'Resume', constants.UNDEFINED, 40, False))
		self.elements.append(Button(450, 250, 150, 100, 'Menu', constants.MAIN_MENU, 40, False))

class StageMenu(Menu):
	def initActors(self):
		#where to go when quitting this menu
		self.action = constants.MAIN_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

		#actors
		self.elements = [Button(260, 500, 250, 70, 'Back', constants.MAIN_MENU)]
		self.elements.append(Label(260, 30, 250, 70, 'Stages', 45))
		for i in range(10):
			self.elements.append(Button(50 + (i%5)*145, 75 + int(i/5)*225, 120, 150, '{}'.format(i+1), constants.STAGE1 + i))

class StatsMenu(Menu):
	def initActors(self):		
		#where to go when quitting this menu
		self.action = constants.MAIN_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

		#actors
		self.elements = []
		self.elements.append(Label(260, 30, 250, 70, 'Stats', 45))
		self.elements.append(Button(450, 250, 150, 100, 'BACK', constants.MAIN_MENU, 40, False))

class SurvivalMenu(Menu):
	def initActors(self):
		#where to go when quitting this menu
		self.action = constants.MAIN_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

		#actors
		self.elements = []
		self.elements.append(Label(260, 30, 250, 70, 'Survival', 45))
		self.elements.append(Button(50, 500, 150, 100, 'PLAY', constants.STAGE_SURVIVAL, 40, False))
		self.elements.append(Button(275, 500, 150, 100, 'RANK', constants.RANK_MENU, 40, False))
		self.elements.append(Button(450, 500, 150, 100, 'BACK', constants.MAIN_MENU, 40, False))


class RankMenu(Menu):
	def initActors(self):		
		#where to go when quitting this menu
		self.action = constants.SURVIVAL_MENU

		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

		#actors
		self.elements = []
		self.elements.append(Label(260, 30, 250, 70, 'Ranking', 45))
		self.elements.append(Button(450, 250, 150, 100, 'BACK', constants.SURVIVAL_MENU, 40, False))
