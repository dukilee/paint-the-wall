import sprites
import constants
import pygame

#Basic Theme
backgroundColor = constants.WHITE

#button
offButtonSprite = sprites.sprite('grey_off_button.png')
offButtonSpriteMini = sprites.sprite('small_grey_off_button.png')
offButtonColor = None
offButtonTextColor = constants.DARK_GREEN
onButtonSprite = sprites.sprite('black_on_button.png')
onButtonSpriteMini = sprites.sprite('small_black_on_button.png')
onButtonColor = None
onButtonTextColor = constants.MED_GREEN

#label
labelBackColor = backgroundColor
labelTextColor = constants.BLACK
labelTextLowColor = constants.GRAY
labelTextLLColor = (220, 220, 220) #Super low

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