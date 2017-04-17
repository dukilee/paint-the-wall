import pygame

from resources import constants, tools
from user_data import data
from visual import theme

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

class Rectangle(Elements):
	def __init__(self, x, y, width, height, b_color = constants.BLACK, thickness = -1):
		self.width = width
		self.height = height
		self.shortcut = [constants.NOKEY]
		self.thickness = thickness

		Elements.__init__(self, x, y)

		self.b_color = b_color # inactive color

	def blit(self, screen):
		if self.thickness > 0:
			pygame.draw.rect(screen, self.b_color, [self.x, self.y, self.width, self.height], self.thickness)
		else:
			pygame.draw.rect(screen, self.b_color, [self.x, self.y, self.width, self.height])

class SlideBar(Elements):
	def __init__(self, x, y, width, maxValue, action, value = 0):
		self.action = action
		self.width = width
		self.height = 50
		self.maxValue = maxValue
		self.value = value
		self.shortcut = [constants.NOKEY]


		Elements.__init__(self, x, y)

		self.pointerPos = tools.Vector2(self.x + int(self.value*self.width/self.maxValue), self.y)
		self.backgroundColor = theme.sliderBackColor
		self.turn_off()

	def turn_on(self):
		self.presentSprite = theme.sliderPointerSpriteOn
		self.presentColor = theme.sliderPointerColorOn

	def turn_off(self):
		self.presentSprite = theme.sliderPointerSpriteOff
		self.presentColor = theme.sliderPointerColorOff

	def blit(self, screen):
		text_rect = [self.x, self.y, self.width, self.height]
		pygame.draw.rect(screen, self.backgroundColor, [self.x, self.y +int(9*self.height/20), self.width, self.height/10])
		if self.presentSprite != None:
			screen.blit(self.presentSprite.img, [self.pointerPos.x - int(self.presentSprite.rec.width/2), self.y, 20, self.height])
		else:
			pygame.draw.rect(screen, self.presentColor, [self.pointerPos.x-10, self.y, 20, self.height])

	def ishovering(self, mouse):
		return mouse[0]>=self.x and mouse[0]<=self.x + self.width and mouse[1]>=self.y and mouse[1]<=self.y + self.height

	# activate button if hovering, deactivate if not
	def hover(self, mouse, done, action):
		self.turn_off()
		if self.action != constants.UNCLICKABLE and self.ishovering(mouse.get_pos()):
			if mouse.get_pressed()[0]: #on click
				self.turn_on()
				self.pointerPos.x = mouse.get_pos()[0]
				self.value = (self.pointerPos.x - self.x)*self.maxValue/self.width
				self.action(self.value)

		return done, action

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

class Title(Label):
	def __init__(self, x=None, y=None, b_text=''):
		Label.__init__(self, x, y, b_text, 70)

	def blit(self, screen):
		text_rect = self.text.get_rect()

		id = int((data.i['lastUnlockedStages']-1)/5)
		if id>0:
			screen.blit(data.leftWingSprite[id-1].img, [self.x + text_rect.x-110, self.y + text_rect.y - 15])
			screen.blit(pygame.transform.flip(data.leftWingSprite[id-1].img, True, False), [self.x + text_rect.width - 25, self.y + text_rect.y - 15])
		pygame.draw.rect(screen, theme.titleBackColor, [text_rect.x + self.x, text_rect.y + self.y, text_rect.width, text_rect.height])
		pygame.draw.rect(screen, theme.backgroundColor, [text_rect.x + self.x+4, 4+text_rect.y + self.y, text_rect.width-8, text_rect.height-14])

		text_rect = self.text.get_rect()
		screen.blit(self.text, self.centralize(text_rect))

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
	def __init__(self, x, y, callAction, imageName):
		Button.__init__(self, x, y, '', constants.UNCLICKABLE, [constants.NOKEY],
					 callAction, constants.BUTTON_FONT_SIZE, True, None, None)
		self.present_button = tools.sprite(imageName)

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

class TextBox(Elements):
	def __init__(self, x = None, y = None, b_text = '', text_size = constants.BUTTON_FONT_SIZE, t_color = constants.BLACK):
		Elements.__init__(self, x, y)
		
		self.t_color = t_color
		self.b_text = b_text # text to be shown on button
		self.fontButton = pygame.font.SysFont('Calibri', text_size, True, False) # to create text objects
		self.text = self.fontButton.render(b_text, True, t_color) # text object
		self.shift = False
		self.MAX_TAM = 15

		self.width = constants.BUTTON_WIDTH
		self.height = constants.BUTTON_HEIGHT

		if x == None:
			x = int((constants.SCREEN_SIZE[0] - self.width)/2)
		if y == None:
			y = int((constants.SCREEN_SIZE[1] - self.height)/2)

		self.body = [x, y, self.width, self.height]
		self.update = False

	#need to enable more "shiftted" keys
	def blit(self, screen, letter):
		if letter != None:
			if letter == constants.keys['backspace'] and len(self.b_text) > 0:
				self.b_text = self.b_text[0:-1]
			elif letter == constants.keys['shift_in']:
				self.shift = True
			elif letter == constants.keys['shift_out']:
				self.shift = False			
			elif letter >= 32 and letter <= 254 and len(self.b_text) < self.MAX_TAM: # (extended) ascii limits
				if self.shift:
					if letter >= ord('a') and letter <= ord('z'):
						self.b_text += chr(letter).upper()
					elif letter == ord('-'):
						self.b_text += '_'
				else:
					self.b_text += chr(letter)
			
			self.text = self.fontButton.render(self.b_text, True, self.t_color)
		text_rect = self.text.get_rect()
		pygame.draw.rect(screen, constants.WHITE, [self.x, self.y, self.width, self.height])
		screen.blit(self.text, self.centralize(text_rect))