import pygame

from audiovisual import theme
from resources import constants, tools
from user_data import data

class Elements:	
	"""
	This is a generic class, has the common methods and atributs of elements, as buttons,
	and others.
	"""

	def __init__(self, x, y):
		"""
		Receive the position of the element on the screen

		:param x: horizontal value
		:param y: vertical value
		:param present_button: current sprite of the button
		:param presentColor: current color of the button
		:param text: the string with size, color and bold
		:param b_text: string of the button
		"""
		self.x = x
		self.y = y

	def turn_on(self):
		"""
		Change the colors of the element creating a visual effect of highlighted element
		"""
		self.present_button = self.on_button_sprite
		self.presentColor = self.onButtonColor
		self.text = self.fontButton.render(self.b_text, True, self.on_t_color)

	def turn_off(self):
		"""
		Change the colors of the element negating the highlighted
		"""
		self.present_button = self.off_button_sprite
		self.presentColor = self.offButtonColor
		self.text = self.fontButton.render(self.b_text, True, self.off_t_color)

	def centralize(self, rec):
		"""
		Receives an rec and the position of its center, so calculates the position of its left-upper
		corner
		:param rec: Rectangle with position of its center
		:return: Position of left-upper corner
		"""
		return [self.x + int((self.width - rec.width)/2), self.y + int((self.height - rec.height)/2)]

	def blit(self, screen):
		"""
		Virtual function, blits the element to the screen.
		"""
		pass

	def ishovering(self, mouse):
		"""
		Checks if the mouse is hovering the area of the current element
		:param mouse: mouse cursor position, comes from pygame
		:return: true if is hovering, and false if isn't
		"""
		return False

	def hover(self, mouse, done, action):
		"""
		Actions of the game if the mouse is hovering the element
		:param mouse: mouse cursor position, comes from pygame
		:param done: true while the player hasn't lost
		:param action: its an enum corresponding to the next action of the game
		:return: done, action
		"""
		return done, action

class Rectangle(Elements):
	"""
	Draws a rectangle on the screen
	"""
	def __init__(self, x, y, width, height, b_color = constants.BLACK, thickness = -1):
		"""
		:param x: horizontal position
		:param y: vertical position
		:param width: width of the rectangle
		:param height: height of the rectangle
		:param b_color: color of the rectangle
		:param thickness: if -1 is a solid rectangle, else is just the edge with the specified thickness
		"""
		self.width = width
		self.height = height
		self.shortcut = [constants.NOKEY]
		self.thickness = thickness

		Elements.__init__(self, x, y)

		self.b_color = b_color # inactive color

	def blit(self, screen):
		"""
		Blits the rectangle to the screen
		:param screen: game screen, comes from pygame
		"""
		if self.thickness > 0:
			pygame.draw.rect(screen, self.b_color, [self.x, self.y, self.width, self.height], self.thickness)
		else:
			pygame.draw.rect(screen, self.b_color, [self.x, self.y, self.width, self.height])

class Icon(Elements):
	"""
	Creates an Icon
	"""
	def __init__(self, x = None, y = None, action = constants.UNCLICKABLE, shortcut = [constants.NOKEY], callAction = None):
		"""
		:param x: horizontal position
		:param y: vertical position
		:param action: action that the game should have after clicking on this element
		:param shortcut: keys that when pressed should activate this element
		:param callAction: function that will be call when the user clicks this element
		"""
		self.set_button_sprites()

		self.width = self.present_button.rec.width
		self.height = self.present_button.rec.height

		Elements.__init__(self, x, y)
		self.body = [x, y, self.width, self.height] # rectangular area of the element
		self.pressed = False

		self.action = action # what will the button peform when clicked
		self.shortcut = shortcut
		self.callAction = callAction

		self.slide_1 = None
		self.slide_2 = None
		
		if theme.vol_max > 0.0 or theme.sfx_max > 0.0:
			self.is_on = True
		else:
			self.is_on = False

	def set_button_sprites(self):
		"""
		set button sprites
		"""
		self.off_button_sprite = theme.sound_off
		self.on_button_sprite = theme.sound_on
		if theme.vol_max > 0.0:
			self.present_button = self.on_button_sprite
		else:
			self.present_button = self.off_button_sprite

	def turn_on(self):
		"""
		change sprites to highlighted state
		"""
		self.present_button = self.on_button_sprite

	def turn_off(self):
		"""
		change sprites to not highlighted state
		"""
		self.present_button = self.off_button_sprite

	def centralize(self, rec):
		"""
		Receives an rec and the position of its center, so calculates the position of its left-upper
		corner
		:param rec: Rectangle with position of its center
		:return: Position of left-upper corner
		"""
		return [self.x + int((self.width - rec.width)/2), self.y + int((self.height - rec.height)/2)]

	def blit(self, screen):
		"""
		blits the icon to the screen
		:param screen: game screen, comes from pygame
		"""
		screen.blit(self.present_button.img, self.centralize(self.present_button.rec))

	def ishovering(self, mouse):
		"""
		true if the mouse is over the element
		:param mouse: mouse cursor position, comes from pygame
		:return: return true if the mouse is over the element
		"""
		return mouse[0]>=self.x and mouse[0]<=self.x + self.width and mouse[1]>=self.y and mouse[1]<=self.y + self.height

	# activate button if hovering, deactivate if not
	def hover(self, mouse, done, action):
		"""
		handles over and click events
		:param mouse: mouse cursor position, comes from pygame
		:param done: true while the player hasn't lost
		:param action: its an enum corresponding to the next action of the game
		:return: done, action
		"""
		if self.ishovering(mouse.get_pos()):
			if mouse.get_pressed()[0]: #on click
				self.pressed = True
			else:
				if self.pressed: #release
					action = self.action
					self.is_on = self.callAction(self, self.is_on)
					if not self.is_on:
						self.slide_1.old_value = self.slide_1.value
						self.slide_1.value = 0.0
						self.slide_2.old_value = self.slide_2.value
						self.slide_2.value = 0.0

				self.pressed = False

		return done, action

class SlideBar(Elements):
	"""
	Draws an slider bar and calls functions for each event
	"""
	def __init__(self, x, y, width, maxValue, action, value = 0, share = None):
		"""
		:param x: horizontal position
		:param y: vertical position
		:param width: width of the slider
		:param maxValue: maximum value of the slider
		:param action: function that will be called when the user clicks the slider
		:param value: current value of the slider
		"""
		self.action = action
		self.width = width
		self.height = 50
		self.maxValue = maxValue
		self.value = value
		self.old_value = value
		self.shortcut = [constants.NOKEY]

		Elements.__init__(self, x, y)

		self.pointerPos = tools.Vector2(self.x + int(self.value*self.width/self.maxValue), self.y)
		self.backgroundColor = theme.sliderBackColor
		self.icon = share
		self.turn_off()

	def turn_on(self):
		"""
		changes color and sprite to highlighted state
		"""
		self.presentSprite = theme.sliderPointerSpriteOn
		self.presentColor = theme.sliderPointerColorOn

	def turn_off(self):
		"""
		changes color and sprite to not hightlighted state
		"""
		self.presentSprite = theme.sliderPointerSpriteOff
		self.presentColor = theme.sliderPointerColorOff

	def blit(self, screen):
		"""
		blits the slider to the screen
		:param screen: game screen, comes from pygame
		"""
		text_rect = [self.x, self.y, self.width, self.height]
		pygame.draw.rect(screen, self.backgroundColor, [self.x, self.y +int(9*self.height/20), self.width, self.height/10])
		if self.presentSprite != None:
			screen.blit(self.presentSprite.img, [self.pointerPos.x - int(self.presentSprite.rec.width/2), self.y, 20, self.height])
		else:
			pygame.draw.rect(screen, self.presentColor, [self.pointerPos.x-10, self.y, 20, self.height])

	def ishovering(self, mouse):
		"""
		checks if the mouse is over the sliderBar
		:param mouse: mouse cursor position, comes from pygame
		:return: true if the move is over the sliderBar
		"""
		return mouse[0]>=self.x and mouse[0]<=self.x + self.width and mouse[1]>=self.y and mouse[1]<=self.y + self.height

	# activate button if hovering, deactivate if not
	def hover(self, mouse, done, action):
		"""
		handles over and click events
		:param mouse: mouse cursor position, comes from pygame
		:param done: true while the player hasn't lost
		:param action: its an enum corresponding to the next action of the game
		:return: done, action
		"""
		self.turn_off()
		if self.action != constants.UNCLICKABLE and self.ishovering(mouse.get_pos()):
			if mouse.get_pressed()[0]: #on click
				self.turn_on()
				self.pointerPos.x = mouse.get_pos()[0]
				self.value = (self.pointerPos.x - self.x)*self.maxValue/self.width
				self.action(self.value, self.icon)

		return done, action

class Label(Elements):
	"""
	Can be static or dynamic but doesn't interacts with the user.
	"""
	def __init__(self, x = None, y = None, b_text = '', text_size = constants.LABEL_FONT_SIZE, b_bold = True, b_color = None, t_color = None, update = None):
		"""
		:param x: horizontal position
		:param y: vertical position
		:param b_text: string with the text of the label
		:param text_size: font size of the label
		:param b_bold: if true then the text is bold
		:param b_color: color of the background
		:param t_color: color of the text
		:param update: true if is dynamic text, false if its static
		"""
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
		"""
		blits the label to the screen
		:param screen: game screen, comes from pygame
		"""
		if self.update != None:
			self.text = self.fontButton.render(self.update(), True, self.t_color)  # text object

		text_rect = self.text.get_rect()
		screen.blit(self.text, self.centralize(text_rect))

class Title(Label):
	"""
	It's the same as label, but bigger and can receive a background image
	"""
	def __init__(self, x=None, y=None, b_text=''):
		"""
		:param x: horizontal position
		:param y: vertical position
		:param b_text: string with the title text
		"""
		Label.__init__(self, x, y, b_text, 70)

	def blit(self, screen):
		"""
		blits the title to the screen with its background image
		:param screen: game screen, comes from pygame
		"""
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
	"""
	Draws a button and handles the press event
	"""
	def __init__(self, x = None, y = None, b_text = '', action = constants.UNCLICKABLE, shortcut = [constants.NOKEY], callAction = None, text_size = constants.BUTTON_FONT_SIZE, b_bold = True, off_t_color = None, on_t_color = None):
		"""
		:param x: horizontal position
		:param y: vertical position
		:param b_text: string with the text of the button
		:param action: its an enum corresponding to the next action of the game
		:param shortcut:  keys that when pressed the button should activate
		:param callAction: function that is called when the user clicks the button
		:param text_size: font size of the button text
		:param b_bold: if true then the text is bold
		:param off_t_color: color when not highlighted
		:param on_t_color: color when highlighted
		"""
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

		self.action = action # what will the button peform when clicked
		self.shortcut = shortcut
		self.callAction = callAction
		self.set_button_sprites()
		self.update = False

	def set_button_sprites(self):
		"""
		sets the sprites and color of the button
		"""
		self.off_button_sprite = theme.offButtonSprite
		self.on_button_sprite = theme.onButtonSprite
		self.onButtonColor = theme.onButtonColor
		self.offButtonColor = theme.offButtonColor
		self.present_button = self.off_button_sprite

	def blit(self, screen):
		"""
		blits the button to the screen
		:param screen: game screen, comes from pygame
		"""
		text_rect = self.text.get_rect()
		if self.present_button != None:
			screen.blit(self.present_button.img, self.centralize(self.present_button.rec))
		else:
			pygame.draw.rect(screen, self.presentColor, [self.x, self.y, self.width, self.height])
		screen.blit(self.text, self.centralize(text_rect))

	def ishovering(self, mouse):
		"""
		checks if the mouse is over the button
		:param mouse: mouse cursor position, comes from pygame
		"""
		return mouse[0]>=self.x and mouse[0]<=self.x + self.width and mouse[1]>=self.y and mouse[1]<=self.y + self.height

	# activate button if hovering, deactivate if not
	def hover(self, mouse, done, action):
		"""
		handles the over and click events
		:param mouse: mouse cursor position, comes from pygame
		:param done: true while the player hasn't lost
		:param action: its an enum corresponding to the next action of the game
		:return: done, action
		"""
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
	"""
	The same as button, but it activates when the mouse pass over it
	"""
	def __init__(self, x, y, callAction, imageName):
		"""
		:param x: horizontal position of the button
		:param y: vertical position of the button
		:param callAction: function that will be called when the mouse pass over it
		:param imageName: name of the sprite of the button
		"""
		Button.__init__(self, x, y, '', constants.UNCLICKABLE, [constants.NOKEY],
					 callAction, constants.BUTTON_FONT_SIZE, True, None, None)
		self.present_button = theme.sprite(imageName)

	# activate button if hovering, deactivate if not
	def hover(self, mouse, done, action):
		"""
		Call the function specified (i.e. callAction) when the mouse pass over the button
		:param mouse: mouse cursor position, comes from pygame
		:param done: true while the player hasn't lost
		:param action: its an enum corresponding to the next action of the game
		:return: done, action
		"""
		if self.ishovering(mouse.get_pos()):
			self.callAction()
		return done, action

class miniButton(Button):
	"""
	The same as class button, but its size is smaller
	"""
	def set_button_sprites(self):
		"""
		Sets the sprites, color, width and height of the button
		"""
		self.off_button_sprite = theme.offButtonSpriteMini
		self.on_button_sprite = theme.onButtonSpriteMini
		self.offButtonColor = theme.offButtonColor
		self.onButtonColor = theme.onButtonColor
		self.present_button = self.off_button_sprite
		self.presentColor = self.offButtonColor
		self.width = constants.BUTTON_MINI_WIDTH
		self.height = constants.BUTTON_MINI_HEIGHT

class TextBox(Elements):
	"""
	Creates an input box
	"""
	def __init__(self, x = None, y = None, b_text = '', text_size = constants.BUTTON_FONT_SIZE, t_color = constants.BLACK):
		"""
		:param x: horizontal position
		:param y: vertical position
		:param b_text: string with the current text
		:param text_size: font size of the text
		:param t_color: text color
		"""
		self.width = constants.BUTTON_WIDTH
		self.height = constants.BUTTON_HEIGHT
	
		if x == None:
			x = int((constants.SCREEN_SIZE[0] - self.width)/2)
		if y == None:
			y = int((constants.SCREEN_SIZE[1] - self.height)/2)
		Elements.__init__(self, x, y)
		
		self.t_color = t_color
		self.b_text = b_text # text to be shown on button
		self.fontButton = pygame.font.SysFont('Calibri', text_size, True, False) # to create text objects
		self.text = self.fontButton.render(b_text, True, t_color) # text object
		self.shift = False
		self.MAX_TAM = 15

		self.body = [x, y, self.width, self.height]
		self.update = False

	#need to enable more "shiftted" keys
	def blit(self, screen, letter):
		"""
		blits the text box to the screen
		:param screen: game screen, comes from pygame
		:param letter: receives the last pressed key and adds it to the text
		"""
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
