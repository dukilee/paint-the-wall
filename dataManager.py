from user_data import data, soundManager

class DataManager:
	"""
	Responsible for loading/saving data from/to user's computer. If there's no data creates a new  one.
	All information is stored on data.py
	"""
	def __init__(self):
		# soundManager.setMusicVolume(data.i['musicVolume'])

		"""
		Load data from user's computer. If there's no data or is corrupted created a new one
		"""
		self.rank_tam = 10
		self.ranking = [('-', 0) for k in range(self.rank_tam)]
		if not data.already:
			data.already = True
			try:
				file = open('data.txt', 'r')

				content = file.readlines()
				for x in content:
					lines = x.strip().split(": ")

					if len(lines) != 2 or lines[0] not in data.i.keys():
						print("Data file is corrupted :(")
					else:
						data.i[lines[0]] = int(float(lines[1]))

				file.close()
			except IOError:
				self.reset();
				print("Creating a new data file...")
				self.save()
		print("setting sound music to ", data.i['musicVolume'])
		soundManager.setMusicVolume(data.i['musicVolume'])


	@staticmethod
	def updateData():
		"""
		checks if the player unlocked a new achievement
		"""

		if data.i['lastUnlockedStages']>20:
			data.i['hacker'] = 1
		else:
			data.i['hacker'] = 0

		if data.i['lastUnlockedStages']>10:
			data.i['pilgrim'] = 1
		else:
			data.i['pilgrim'] = 0

		if data.i['ballsDestructed'] > 42: #universe age
			data.i['serialKiller'] = 1
		else:
			data.i['serialKiller'] = 0

		if data.i['hacker']==1 and data.i['pilgrim']==1 and data.i['serialKiller']==1 and \
			data.i['worldEmperor']==1 and data.i['immortal']==1 and data.i['pacifist']==1 and \
			data.i['yogaMaster']==1 and data.i['doubleKill']==1:
			data.i['jedi'] = 1
		else:
			data.i['jedi'] = 0
	@staticmethod
	def save():
		"""
		Save the data to the user's computer
		"""
		file = open('data.txt', 'w')
		for name, val in data.i.items():
			s = name + ": " + str(val) + "\n"
			file.write(s)
		file.close()

def reset():
	"""
	Reset all data.
	"""
	data.startTime = 0
	data.startTime = data.getActualTime()
	data.new_score, data.new_player = 0, '-'

	data.i = {'timePlayed': 0, 'blocksConquered': 0, 'deaths': 0, 'ballsDestructed': 0,
		 'lastUnlockedStages': 1, 'theme': 0,
		 # achievements
		 'doubleKill': 0, 'worldEmperor': 0, 'yogaMaster': 0, 'immortal': 0, 'jedi': 0,
		 'pilgrim': 0, 'hacker': 0, 'pacifist': 0, 'serialKiller': 0,
		 # settings
		 'musicVolume': 0, 'effectsVolume': 0, 'rank': [('-', 0) for k in range(10)]}
	data.i['timePlayed'] = 0
	bd = data.i['ballsDestructed']

def full():
	"""
	Unlocks everything that is possible.
	"""
	tp = data.i['timePlayed']
	bd = data.i['ballsDestructed']
	if(bd<42):
		bd = 42
	rk = data.i['rank']
	data.i = {'timePlayed': tp, 'blocksConquered': 0, 'deaths': 0, 'ballsDestructed': bd,
		 'lastUnlockedStages': 21, 'theme': 0,
		 # achievements
		 'doubleKill': 1, 'worldEmperor': 1, 'yogaMaster': 1, 'immortal': 1, 'jedi': 1,
		 'pilgrim': 1, 'hacker': 1, 'pacifist': 1, 'serialKiller': 1,
		 # settings
		 'musicVolume': 100, 'effectsVolume': 100, 'rank': rk}