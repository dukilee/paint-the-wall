import constants

def round_coord(c, t): # t = 0 or 1 (x or y)
	return int(round(c/constants.SCALE[t]))

def discretize(pos):
	return [round_coord(pos.x, 0), round_coord(pos.y, 1)]