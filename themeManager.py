import theme
import sprites
import constants
import data

def changeTheme(n):
    if n!= constants.RESET_THEME:
        changeTheme(constants.RESET_THEME)

    data.i['theme'] = n
    if n == constants.BASIC_THEME:
        #Basic Theme
        theme.backgroundColor = constants.WHITE

        #button
        theme.offButtonSprite = sprites.sprite('grey_off_button.png')
        theme.offButtonSpriteMini = sprites.sprite('small_grey_off_button.png')
        theme.offButtonTextColor = constants.DARK_GREEN
        theme.onButtonSprite = sprites.sprite('black_on_button.png')
        theme.onButtonSpriteMini = sprites.sprite('small_black_on_button.png')
        theme.onButtonTextColor = constants.MED_GREEN

        #label
        theme.labelBackColor = theme.backgroundColor
        theme.labelTextColor = constants.BLACK
        theme.labelTextLowColor = constants.GRAY
        theme.labelTextLLColor = (180, 180, 180)

        # engine
        theme.conqColor = constants.GREEN
        theme.procColor = constants.LIGHT_GREEN
        theme.freeColor = constants.WHITE
        theme.ballColor = constants.BLUE
        theme.heroColor = constants.RED
    elif n == constants.DARK_THEME:
        theme.backgroundColor = constants.BLACK

        # button
        theme.offButtonColor = (10, 10, 10)#DARK_GRAY
        theme.offButtonTextColor = (200, 200, 200)#LIGHT_GRAY
        theme.onButtonColor = constants.DARK_GREEN
        theme.onButtonTextColor = constants.WHITE


        # engine
        theme.conqColor = constants.DARK_GREEN
        theme.procColor = constants.GREEN
        theme.freeColor = constants.BLACK
        theme.ballColor = (90, 30, 0)
        theme.heroColor = (190, 190, 0)

        # label
        theme.labelBackColor = constants.WHITE#theme.backgroundColor
        theme.labelTextColor = (180, 180, 180)#GRAY
        theme.labelTextLowColor = (80, 80, 80)
        theme.labelTextLLColor = (30, 30, 30)

    elif n == constants.RESET_THEME:
        #Basic Theme
        theme.backgroundColor = constants.WHITE

        #button
        theme.offButtonSprite = None
        theme.offButtonSpriteMini = None
        theme.offButtonColor = None
        theme.offButtonTextColor = constants.DARK_GREEN
        theme.onButtonSprite = None
        theme.onButtonSpriteMini = None
        theme.onButtonColor = None
        theme.onButtonTextColor = constants.MED_GREEN

        #label
        theme.labelBackColor = theme.backgroundColor
        theme.labelTextColor = constants.BLACK
        theme.labelTextLowColor = constants.GRAY
        theme.labelTextLLColor = (220, 220, 220)

        # engine
        theme.conqColor = constants.GREEN
        theme.procColor = constants.LIGHT_GREEN
        theme.freeColor = constants.WHITE
        theme.ballColor = constants.BLUE
        theme.heroColor = constants.RED