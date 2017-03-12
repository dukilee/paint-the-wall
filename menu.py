import constants
import pygame
from pygame.locals import *

def hovering(xarea, yarea, width, height, mouse):
	return mouse[0]>=xarea and mouse[0]<=xarea + width and mouse[1]>=yarea and mouse[1]<=yarea + height

class Menu:
	

	def update(self, screen):
		#constants
		clock = pygame.time.Clock()
		done = False;
		action = constants.QUIT
		pygame.mouse.set_cursor(*pygame.cursors.tri_left)
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
			fontButton = pygame.font.SysFont('Calibri', 80, True, False)

			#button PLAY
			if hovering(100, 200, 500, 100, pygame.mouse.get_pos()):
				if pygame.mouse.get_pressed()[0]: #on click
					done = True
					action = constants.STAGE_SELECT
				else: #pass over
					textPlayColor = (100, 255, 100)
					buttonPlayColor = (100, 100, 255)
			else:#away from button 
				textPlayColor = (0, 150, 0)
				buttonPlayColor = (0, 0, 255)
			textPlay = fontButton.render('PLAY', True, textPlayColor)

			#button QUIT
			if hovering(100, 350, 500, 100, pygame.mouse.get_pos()):
				if pygame.mouse.get_pressed()[0]: #on click
					done = True
					action = constants.QUIT
				else: #pass over
					textQuitColor = (100, 255, 100)
					buttonQuitColor = (100, 100, 255)
			else:#away from button 
				textQuitColor = (0, 150, 0)
				buttonQuitColor = (0, 0, 255)
			textQuit = fontButton.render('QUIT', True, textPlayColor)

			#draw buttons
			pygame.draw.rect(screen, buttonPlayColor, [100, 200, 500, 100])
			pygame.draw.rect(screen, buttonQuitColor, [100, 350, 500, 100])
			
			textTitle = fontButton.render('THE GAME', True, (0, 0, 0))
			screen.blit(textTitle, [220, 100])
			screen.blit(textPlay, [300, 230])
			screen.blit(textQuit, [300, 380])
			pygame.display.flip()

			clock.tick(200)
		return action