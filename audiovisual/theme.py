import pygame

from resources import constants

"""
Keeps the value of each color/sprite for the current theme
"""

pygame.init()

class sprite(pygame.sprite.Sprite):
	"""
	Keeps the sprite image and its size
	"""
	def __init__(self, path, scale = 1.0):
		"""
		:param path: Name of the archive in the computer
		:param scale: Diminishes the image
		"""
		self.img = pygame.image.load('resources/sprites/' + path)
		self.rec = self.img.get_rect()
		self.img = pygame.transform.scale(self.img, (int(self.rec.width * scale), int(self.rec.height * scale)))


#Basic Theme
backgroundColor = (245, 245, 255)

#button
offButtonSprite = sprite('Basic/grey_off_button.png')
offButtonSpriteMini = sprite('Basic/small_grey_off_button.png')
offButtonColor = None
offButtonTextColor = constants.DARK_GREEN
onButtonSprite = sprite('Basic/black_on_button.png')
onButtonSpriteMini = sprite('Basic/small_black_on_button.png')
onButtonColor = None
onButtonTextColor = constants.MED_GREEN
onButtonActualStage = constants.BLUE
offButtonActualStage = (120, 120, 255)

#label
labelBackColor = backgroundColor
labelTextColor = constants.BLACK
labelTextLowColor = constants.GRAY
labelTextLLColor = (220, 220, 220) #Super low
titleBackColor = (240, 240, 255)

#Slider Bar
sliderPointerSpriteOff = offButtonSpriteMini
sliderPointerSpriteOn = onButtonSpriteMini
sliderBackColor = constants.BLACK
sliderPointerColorOn = constants.BLACK
sliderPointerColorOff = constants.BLACK

#engine
text_color = constants.BLACK
conqColor = constants.GREEN
procColor = constants.LIGHT_GREEN
freeColor = constants.WHITE
ballColor = constants.BLUE
heroColor = constants.RED

#icons
sound_on = sprite('sound_on.png')
sound_off = sprite('sound_off.png')

#sounds
menu_song = 'resources/sounds/menu.mid'
game_song = 'resources/sounds/game.mid'
rank_song = 'resources/sounds/rank.mid'
lose_song = 'resources/sounds/lose.mid'
win_song = 'resources/sounds/win.mid'
conquering_song = 'resources/sounds/conquering.wav'
conquered_song = 'resources/sounds/conquered.wav'
