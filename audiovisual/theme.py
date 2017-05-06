import pygame

from resources import constants

class sprite(pygame.sprite.Sprite):
	def __init__(self, path, scale = 1.0):
		self.img = pygame.image.load('resources/sprites/' + path)
		self.rec = self.img.get_rect()
		self.img = pygame.transform.scale(self.img, (int(self.rec.width * scale), int(self.rec.height * scale)))

def play_music(path, vol = 1.0, rep = -1):
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

#engine
text_color = constants.BLACK

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
conqColor = constants.GREEN
procColor = constants.LIGHT_GREEN
freeColor = constants.WHITE
ballColor = constants.BLUE
heroColor = constants.RED

#sounds
music = pygame.mixer.music
vol_max = 1.0
menu_song = 'resources/sounds/menu.mid'
menu_vol = 1.0
game_song = 'resources/sounds/game.mid'
game_vol = 1.0
rank_song = 'resources/sounds/rank.mid'
lose_song = 'resources/sounds/lose.mid'
win_song = 'resources/sounds/win.mid'
conquering_sfx = 'resources/sounds/conquering.wav'
conquered_sfx = 'resources/sounds/conquered.wav'
