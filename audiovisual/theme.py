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

def play_music(path, vol = 1.0, rep = -1):
	"""
	starts the music
	:param path: name of the archive in the computer
	:param vol: volume of the music
	:param rep: number of repetitions
	"""
	global music, vol_max
	music.stop()
	music.load(path)
	music.set_volume(vol * vol_max)
	music.play(rep)

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
music = pygame.mixer.music
sfx = pygame.mixer
old_music, old_sfx = 1.0, 1.0
vol_max, sfx_max = 1.0, 1.0
menu_song = 'resources/sounds/menu.mid'
menu_vol = 1.0
game_song = 'resources/sounds/game.mid'
game_vol = 0.4
rank_song = 'resources/sounds/rank.mid'
lose_song = 'resources/sounds/lose.mid'
win_song = 'resources/sounds/win.mid'
sfx_arq = { 'conquering': 'resources/sounds/conquering.wav', 'conquered': 'resources/sounds/conquered.wav' }
sfx_list = { k: pygame.mixer.Sound(sfx_arq[k]) for k in sfx_arq }