import constants
import vector2

class Hero:
	def __init__(self):
		self.pos = vector2.Vector2(0, 0)
		#constants.HERO_SPEED = constants.HERO_SPEED
		self.direction = constants.STOP
	
	def update(self, key, press):
		if press:
			if key == constants.KEY_RIGHT:
				self.direction = constants.RIGHT
			if key == constants.KEY_UP:
				self.direction = constants.UP
			if key == constants.KEY_LEFT:
				self.direction = constants.LEFT
			if key == constants.KEY_DOWN:
				self.direction = constants.DOWN
		else:
			if key == constants.KEY_RIGHT:
				if self.direction == constants.RIGHT:
					self.direction = constants.STOP
			if key == constants.KEY_UP:
				if self.direction == constants.UP:
					self.direction = constants.STOP
			if key == constants.KEY_LEFT:
				if self.direction == constants.LEFT:
					self.direction = constants.STOP
			if key == constants.KEY_DOWN:
				if self.direction == constants.DOWN:
					self.direction = constants.STOP

		if self.direction == constants.RIGHT:
			if self.pos.x < constants.SCREEN_SIZE[0] - constants.HERO_SIZE[0]:
				self.pos.x += constants.HERO_SPEED
		
		elif self.direction == constants.UP:
			if self.pos.y > 0:
				self.pos.y -= constants.HERO_SPEED
		
		elif self.direction == constants.LEFT:
			if self.pos.x > 0:
				self.pos.x -= constants.HERO_SPEED
		
		elif self.direction == constants.DOWN:
			if self.pos.y < constants.SCREEN_SIZE[1] - constants.HERO_SIZE[1]:
				self.pos.y += constants.HERO_SPEED
		
		
		
