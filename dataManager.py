from user_data import data

class DataManager:
	def __init__(self):
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
			print("Creating a new data file...")
			self.save()

	@staticmethod
	def updateData():
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
		file = open('data.txt', 'w')
		for name, val in data.i.items():
			s = name + ": " + str(val) + "\n"
			file.write(s)
		file.close()

