#colors
NONE = (-1, -1, -1)
WHITE = (255, 255, 255)
MED_BLUE = (100, 100, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
LIGHT_GREEN = (200, 255, 200)
MED_GREEN = (100, 255, 100)
DARK_GREEN = (0, 150, 0)
GREEN = (0, 255, 0)

#screen
SCREEN_SIZE = (800, 600)

#hero
STOP = 0
RIGHT = 1
UP = 2
LEFT = 3
DOWN = 4
HERO_SPEED = 2
HERO_SIZE = (20, 20)

#ball
BALL_RADIUS = 7

#arrows
NOKEY = -1
KEY_RIGHT = 275
KEY_UP = 273
KEY_LEFT = 276
KEY_DOWN = 274
keys = { KEY_RIGHT: RIGHT, KEY_LEFT: LEFT, KEY_DOWN: DOWN, KEY_UP: UP, 'a':97, 'b':98,
			'c':99, 'd':100, 'e':101, 'f':102, 'g':103, 'h':104, 'i':105, 'j':106,
			'k':107, 'l':108, 'm':109, 'n':110, 'o':111, 'p':112, 'q':113, 'r':114,
			's':115, 't':116, 'u':117, 'v':118, 'w':119, 'x':120, 'y':121, 'z':122}
move_x = { RIGHT: HERO_SPEED, LEFT: -HERO_SPEED }
move_y = { UP: -HERO_SPEED, DOWN: HERO_SPEED }



#grid
NOTHING = 3
PROCESS = 2
CONQUERED = 1
HYPER = NOTHING + 1
SHYPER = HYPER + 1
GRID_SIZE = (40, 40)
SCALE = (int(SCREEN_SIZE[0]/GRID_SIZE[0]), int(SCREEN_SIZE[1]/GRID_SIZE[1]))

#states
LOSE = -99
WIN = -100
PRISION_AREA = 500 #1445

#menu
BUTTON_FONT_SIZE = 25
LABEL_FONT_SIZE = 50
POS = { 'RIGHT': int(0.7 * SCREEN_SIZE[0]), 'LEFT': int(0.05 * SCREEN_SIZE[0]), 'UP': int(0.15 * SCREEN_SIZE[1]), 'DOWN': int(0.85 * SCREEN_SIZE[1]) }
UNDEFINED = -1000 # for flags
RESTART = -3
UNCLICKABLE = -1
QUIT = 0

ABOUT_MENU = 1
ACHIEVEMENTS_MENU = 2
MAIN_MENU = 3
RANK_MENU = 4
STAGE_MENU = 5
STATS_MENU = 6
SURVIVAL_MENU = 7

PLAY = 9
STAGE = 10
STAGE_SURVIVAL = 99
STAGE0 = 100
STAGE1 = STAGE0 + 1
STAGE2 = STAGE1 + 1
STAGE3 = STAGE2 + 1
STAGE4 = STAGE3 + 1
STAGE5 = STAGE4 + 1
STAGE6 = STAGE5 + 1
STAGE7 = STAGE6 + 1
STAGE8 = STAGE7 + 1
STAGE9 = STAGE8 + 1
STAGE10 = STAGE9 + 1