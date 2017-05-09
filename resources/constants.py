import pygame

#colors
NONE = (-1, -1, -1)
WHITE = (255, 255, 255)
MED_BLUE = (100, 100, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
LIGHT_GREEN = (200, 255, 200)
MED_GREEN = (100, 255, 100)
DARK_GREEN = (0, 120, 0)
GREEN = (0, 255, 0)
GRAY = (120, 120, 120)

#screen
SCREEN_SIZE = (800, 600)

#grid
NOTHING = 3
PROCESS = 2
CONQUERED = 1
HYPER = NOTHING + 1
SHYPER = HYPER + 1
GRID_SIZE = (40, 40)
SCALE = (int(SCREEN_SIZE[0]/GRID_SIZE[0]), int(SCREEN_SIZE[1]/GRID_SIZE[1]))
SCR = pygame.Rect(0, 0, SCREEN_SIZE[0],  SCREEN_SIZE[1])
dx = (1, -1, 0, 0)
dy = (0, 0, 1, -1)

#hero
STOP = 0
RIGHT = 1
UP = 2
LEFT = 3
DOWN = 4
HERO_SPEED = 2
HERO_SIZE = (20, 20)
DEF_Px = 0 #default initial 'x' position
DEF_Py = 0 #default initial 'y' position
move_x = { RIGHT: HERO_SPEED, LEFT: -HERO_SPEED }
move_y = { UP: -HERO_SPEED, DOWN: HERO_SPEED }

#ball
BALL_RADIUS = 7
DEF_Vx = 3 #default horizontal velocity
DEF_Vy = 3 #default vertical velocity

#arrows
NOKEY = -1
KEY_RIGHT = 275
KEY_UP = 273
KEY_LEFT = 276
KEY_DOWN = 274

keys = { KEY_RIGHT: RIGHT, KEY_LEFT: LEFT, KEY_DOWN: DOWN, KEY_UP: UP,
		 'enter': 13, 'backspace': 8, 'space': 32, 'shift_in': 15, 'shift_out': 14}
		 
for k in range(ord('a'), ord('z') + 1): # adding letters to keys
	keys[chr(k)] = k

for k in range(ord('0'), ord('9') + 1): # adding numbers to keys
	keys[chr(k)] = k

#states
LOSE = -99
WIN = -100
PRISION_AREA = 500 #1445

#menu
BUTTON_FONT_SIZE = 25
BUTTON_HEIGHT = 57
BUTTON_WIDTH = 198
BUTTON_MINI_HEIGHT = 57
BUTTON_MINI_WIDTH = 57
LABEL_FONT_SIZE = 50
POS = { 'RIGHT': int(0.7 * SCREEN_SIZE[0]),
        'LEFT': int(0.05 * SCREEN_SIZE[0]),
        'UP': int(0.08 * SCREEN_SIZE[1]),
        'DOWN': int(0.85 * SCREEN_SIZE[1]) }

UNDEFINED = -1000 # for flags
NEXT = -999
RESTART = -3
SPECIAL = -2
UNCLICKABLE = -1
QUIT = 0

ABOUT_MENU = 1
ACHIEVEMENTS_MENU = 2
MAIN_MENU = 3
STAGE_MENU = 5
STATS_MENU = 6
SURVIVAL_MENU = 7
SETTINGS_MENU = 8
TUTORIAL_MENU=10
STAGE_MENU_2 = 121
MENU_INDEX = { ABOUT_MENU: "About", ACHIEVEMENTS_MENU: "Achievements",
               MAIN_MENU: "Main", STAGE_MENU: "Stage", STAGE_MENU_2: "Stage2",
               STATS_MENU: "Stats", SURVIVAL_MENU: "Survival", SETTINGS_MENU: "Settings", TUTORIAL_MENU:"Tutorial"}

#stages
PLAY = 9
RANK_INSERT = 98
STAGE_SURVIVAL = 99
STAGE_0 = 100
N_OF_STAGES = 20
STAGE_INDEX = [STAGE_0 + k for k in range(N_OF_STAGES + 1)]
ACHIEVE_DURATION = 3

#themes
RESET_THEME = -1
BASIC_THEME = 0
DARK_THEME = 1
MARIO_THEME = 2