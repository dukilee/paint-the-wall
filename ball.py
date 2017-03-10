import constants
import sys
class Ball:
	pos = [100, 100]
	speed = [3, 3]
	def update(self, grid):
		nextPos = [self.pos[0] + constants.BALL_RADIUS*(self.speed[0]/abs(self.speed[0])), self.pos[1] + constants.BALL_RADIUS*self.speed[1]/abs(self.speed[1])]
		actualGrid = [int(round(self.pos[0]/constants.SCALE[0])), int(round(self.pos[1]/constants.SCALE[1]))]		
		nextGrid = [int(round(nextPos[0]/constants.SCALE[0])), int(round(nextPos[1]/constants.SCALE[1]))]
		if grid[nextGrid[0]][actualGrid[1]] == constants.CONQUERED:
			self.speed[0] *= -1
			nextPos[0] = self.pos[0] + self.speed[0]
			nextGrid[0] = int(round(nextPos[0]/constants.SCALE[0]))
		if grid[actualGrid[0]][nextGrid[1]] == constants.CONQUERED:
			self.speed[1] *= -1
			nextPos[1] = self.pos[1] + self.speed[1]
			nextGrid[1] = int(round(nextPos[1]/constants.SCALE[1]))

		if grid[nextGrid[0]][nextGrid[1]] == constants.PROCESS:
			print("YOU LOST :(");
			sys.exit()
		self.pos = [self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]]
