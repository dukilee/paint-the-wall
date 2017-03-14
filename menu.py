import constants
import pygame
from pygame.locals import *

class Button:	
	def __init__(self, x, y, w, h, b_text = '', action = -1, b_text_size = 60, b_bold = True, off_b_color = constants.BLUE, off_t_color = constants.DARK_GREEN, on_b_color = constants.MED_BLUE, on_t_color = constants.MED_GREEN):
		self.x = x
		self.y = y
		self.width = w
		self.height = h
		self.body = [x, y, w, h] # rectangular area of the button

		self.off_b_color = off_b_color # inactive button color
		self.off_t_color = off_t_color # inactive text color

		if action == constants.UNCLICKABLE:
			self.on_b_color = off_b_color # color remains unchanged
			self.on_t_color = off_t_color # color remains unchanged
		else:
			self.on_b_color = on_b_color # active button color
			self.on_t_color = on_t_color # active text color

		self.b_color = off_b_color # present button color
		self.b_text = b_text # text to be shown on button
		self.fontButton = pygame.font.SysFont('Calibri', b_text_size, b_bold, False) # to create text objects
		self.text = self.fontButton.render(b_text, True, off_t_color) # text object

		self.action = action # what will the button peform when clicked (see constants.py)

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
		if self.action != constants.UNCLICKABLE and self.ishovering(mouse.get_pos()):
			if mouse.get_pressed()[0]: #on click
				done = True
				action = self.action
			else: #pass over
				self.on_color()
		else: #away from button 
			self.off_color()

		return done, action

class Menu:
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
					done = True
				elif event.type == pygame.KEYDOWN:
					if event.key == 113:			
						done = True

			#drawing background
			screen.fill(constants.WHITE)

			#button PLAY
			for b in self.buttons:
				done, action = b.hover(mouse, done, action)
				b.draw(screen)
				b.blit(screen)

			pygame.display.update(self.updateRect)

			clock.tick(200)
		return action


class MainMenu(Menu):
	def initActors(self):
		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

		#actors
		self.buttons = []
		self.buttons.append(Button(260, 100, 250, 70, 'Paint-The-Wall!', constants.UNCLICKABLE, 60, True, constants.WHITE, constants.BLACK))
		self.buttons.append(Button(260, 200, 250, 70, 'PLAY', constants.STAGE_SELECT))
		self.buttons.append(Button(260, 300, 250, 70, 'STAGES', constants.LEVEL_0))
		self.buttons.append(Button(260, 400, 250, 70, 'QUIT', constants.QUIT))
		

class StageMenu(Menu):
	def initActors(self):
		#part of the screen that this menu uses
		self.updateRect = Rect(0, 0, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1])

		#actors
		self.buttons = [Button(260, 500, 250, 70, 'Back', constants.MAIN_MENU)]
		for i in range(10):
			self.buttons.append(Button(50 + (i%5)*145, 75 + int(i/5)*225, 120, 150, '{}'.format(i+1), constants.STAGE1 + i))
				

class PauseMenu(Menu):
	def initActors(self):
		#part of the screen that this menu uses
		self.updateRect = Rect(0, 200, constants.SCREEN_SIZE[0], constants.SCREEN_SIZE[1]-400)

		#actors
		self.buttons = []
		self.buttons.append(Button(100, 250, 150, 100, 'Restart', constants.RESTART, 40, False))
		self.buttons.append(Button(275, 250, 150, 100, 'Resume', constants.UNDEFINED, 40, False))
		self.buttons.append(Button(450, 250, 150, 100, 'Menu', constants.MAIN_MENU, 40, False))
		

