from audiovisual import theme
from resources import constants, tools
from user_data import data

def changeTheme(n):
    if n!= constants.RESET_THEME:
        changeTheme(constants.RESET_THEME)

    data.i['theme'] = n
    if n == constants.BASIC_THEME:
        #Basic Theme
        theme.backgroundColor = (245, 245, 255)

        #button
        theme.offButtonSprite = theme.sprite('Basic/grey_off_button.png')
        theme.offButtonSpriteMini = theme.sprite('Basic/small_grey_off_button.png')
        theme.offButtonTextColor = constants.DARK_GREEN
        theme.onButtonSprite = theme.sprite('Basic/black_on_button.png')
        theme.onButtonSpriteMini = theme.sprite('Basic/small_black_on_button.png')
        theme.onButtonTextColor = constants.MED_GREEN
        theme.onButtonActualStage = constants.BLUE
        theme.offButtonActualStage = (120, 120, 255)

        #label
        theme.labelBackColor = theme.backgroundColor
        theme.labelTextColor = constants.BLACK
        theme.labelTextLowColor = constants.GRAY
        theme.labelTextLLColor = (180, 180, 180)
        theme.titleBackColor = (205, 255, 205)

        #slider Bar
        theme.sliderPointerSpriteOff =  theme.sprite('Basic/small_grey_off_button.png')
        theme.sliderPointerSpriteOn = theme.sprite('Basic/small_black_on_button.png')

        # engine
        theme.conqColor = constants.GREEN
        theme.procColor = constants.LIGHT_GREEN
        theme.freeColor = constants.WHITE
        theme.ballColor = constants.BLUE
    
    elif n == constants.DARK_THEME:
        theme.backgroundColor = (5, 5, 5)

        # button
        theme.offButtonColor = (10, 10, 10)#DARK_GRAY
        theme.offButtonTextColor = (200, 200, 200)#LIGHT_GRAY
        theme.onButtonColor = constants.DARK_GREEN
        theme.onButtonTextColor = constants.WHITE
        theme.onButtonActualStage = (120, 120, 250)
        theme.offButtonActualStage = (50, 50, 150)

        # engine
        theme.conqColor = constants.DARK_GREEN
        theme.procColor = constants.GREEN
        theme.freeColor = constants.BLACK
        theme.ballColor = (90, 30, 0)
        theme.titleBackColor = (7,35,7)

        # label
        theme.labelBackColor = constants.WHITE#theme.backgroundColor
        theme.labelTextColor = (180, 180, 180)#GRAY
        theme.labelTextLowColor = (80, 80, 80)
        theme.labelTextLLColor = (30, 30, 30)

        #slider Bar
        theme.sliderBackColor = (180, 180, 180)
        theme.sliderPointerColorOn = (80, 80, 80)
        theme.sliderPointerColorOff = (150, 150, 150)

    elif n == constants.MARIO_THEME:
        theme.backgroundColor = (255, 255, 255)

        #button
        theme.offButtonSprite = theme.sprite('SMB/off_button.png')
        theme.offButtonSpriteMini = theme.sprite('SMB/mini_off_button.png')
        theme.offButtonColor = None
        theme.offButtonTextColor = constants.BLACK
        theme.offButtonActualStage = constants.MED_BLUE

        theme.onButtonSprite = theme.sprite('SMB/on_button.png')
        theme.onButtonSpriteMini = theme.sprite('SMB/mini_on_button.png')
        theme.onButtonColor = None
        theme.onButtonTextColor = constants.WHITE
        theme.onButtonActualStage = constants.WHITE
        
		#label
        theme.labelTextColor = constants.BLACK
        theme.labelTextLowColor = constants.GRAY
        theme.labelTextLLColor = (220, 220, 220) #Super low
        theme.titleBackColor = (240, 240, 255)

		#Slider Bar
        theme.sliderPointerSpriteOff = theme.sprite('SMB/mini_off_button.png')
        theme.sliderPointerSpriteOn = theme.sprite('SMB/mini_on_button.png')
        theme.sliderBackColor = constants.BLACK
        theme.sliderPointerColorOn = constants.BLACK
        theme.sliderPointerColorOff = constants.BLACK

		#engine
        theme.text_color = constants.WHITE
        theme.conqColor = constants.BLACK
        theme.procColor = constants.GRAY
        theme.freeColor = constants.WHITE

    elif n == constants.RESET_THEME:
        #Basic Theme
        theme.backgroundColor = (245, 245, 255)

        #button
        theme.offButtonSprite = None
        theme.offButtonSpriteMini = None
        theme.offButtonColor = None
        theme.offButtonTextColor = constants.DARK_GREEN
        theme.onButtonSprite = None
        theme.onButtonSpriteMini = None
        theme.onButtonColor = None
        theme.onButtonTextColor = constants.MED_GREEN
        theme.onButtonActualStage = constants.BLUE
        theme.offButtonActualStage = (120, 120, 255)

        #label
        theme.labelBackColor = theme.backgroundColor
        theme.labelTextColor = constants.BLACK
        theme.labelTextLowColor = constants.GRAY
        theme.labelTextLLColor = (220, 220, 220)
        theme.titleBackColor = (249, 249, 255)

        #slider Bar
        theme.sliderPointerSpriteOff = None
        theme.sliderPointerSpriteOn = None
        theme.sliderBackColor = constants.BLACK
        theme.sliderPointerColorOn = constants.BLACK
        theme.sliderPointerColorOff = constants.BLACK

        # engine
        theme.conqColor = constants.GREEN
        theme.procColor = constants.LIGHT_GREEN
        theme.freeColor = constants.WHITE
        theme.ballColor = constants.BLUE
        theme.heroColor = (220, 0, 0)

        #sounds
        theme.vol_max = 1.0
        theme.menu_song = 'resources/sounds/SMW/menu.mid'
        theme.menu_vol = 1.0
        theme.game_song = 'resources/sounds/SMW/game.mid'
        theme.game_vol = 0.3
        theme.rank_song = 'resources/sounds/rank.mid'
        theme.lose_song = 'resources/sounds/lose.mid'
        theme.win_song = 'resources/sounds/win.mid'
        theme.conquering_sfx = 'resources/sounds/SMW/conquering.wav'
        theme.conquered_sfx = 'resources/sounds/SMW/conquered.wav'
