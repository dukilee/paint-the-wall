import constants
import pygame
from pygame.locals import *

class Button:	
	def __init__(self, x, y, w, h, b_text = '', action = -1, off_b_color = (0, 0, 255), off_t_color = (0, 150, 0), on_b_color = (100, 100, 255), on_t_color = (100, 255, 100)):
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
		self.fontButton = pygame.font.SysFont('Calibri', 80, True, False) # to create text objects
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
	def blit(self, screen, where = [0, 0]):
		screen.blit(self.text, where)

	def other_blit(self, screen):
		text_rect = self.text.get_rect()
		screen.blit(self.text, [self.x + self.width/2 - text_rect.width/2, self.y + self.height/2 - text_rect.height/2])

	# checks if mouse is hovering this area
	def ishovering(self, mouse):
		return mouse[0]>=self.x and mouse[0]<=self.x + self.width and mouse[1]>=self.y and mouse[1]<=self.y + self.height

	# activate button if hovering, deactivate if not
	def hover(self, mouse, done, action):
		if self.action >= 0 and self.ishovering(mouse.get_pos()):
			if mouse.get_pressed()[0]: #on click
				done = True
				action = self.action
			else: #pass over
				self.on_color()
		else: #away from button 
			self.off_color()

		return done, action

class Menu:
	def update(self, screen):
		#constants
		clock = pygame.time.Clock()
		done = False;
		action = constants.QUIT
		pygame.mouse.set_cursor(*pygame.cursors.tri_left)

		#actors
		mouse = pygame.mouse
		TITLE_button = Button(150, 100, 500, 100, 'THE GAME', constants.UNCLICKABLE, constants.WHITE, constants.BLACK)
		PLAY_button = Button(150, 200, 500, 100, 'PLAY', constants.STAGE_SELECT)
		QUIT_button = Button(150, 350, 500, 100, 'QUIT', constants.QUIT)
		
		while not done:
			#player commands
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True
				elif event.type == pygame.KEYDOWN:
					if event.key == 113:			
						done = True

			#drawing
			screen.fill(constants.WHITE)

			#button PLAY
			done, action = PLAY_button.hover(mouse, done, action)

			#button QUIT
			done, action = QUIT_button.hover(mouse, done, action)

			#draw buttons
			PLAY_button.draw(screen)
			QUIT_button.draw(screen)
				
			#TITLE_button.blit(screen, [220, 100])
			#PLAY_button.blit(screen, [325, 215])
			#QUIT_button.blit(screen, [320, 365])

			TITLE_button.other_blit(screen)
			PLAY_button.other_blit(screen)
			QUIT_button.other_blit(screen)

			pygame.display.flip()

			clock.tick(200)
		return action