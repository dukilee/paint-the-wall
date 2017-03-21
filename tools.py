import constants
import random
import vector2

# for balls
def random_pos():
	return vector2.Vector2(random.randint(1 + int(0.1 * constants.SCREEN_SIZE[0]), int(0.9 * constants.SCREEN_SIZE[0])), random.randint(int(1 + 0.1 * constants.SCREEN_SIZE[1]), int(0.9 * constants.SCREEN_SIZE[1])))

def conv(c, t): # t = 0 or 1 (x or y)
	return int(round(c/constants.SCALE[t]))

def discretize(pos):
	return [conv(pos.x, 0), conv(pos.y, 1)]

def sign(x):
	if x>0:
		return 1
	return -1