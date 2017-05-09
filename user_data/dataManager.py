import binascii

from user_data import data

class DataManager:
	"""
	Responsible for saving/loading data information, and stores on data.py
	"""
	def __init__(self):
		"""
		Reads the data from the user computer. If there's no data, creates a new one.
		"""
		try:
			file = open('user_data\\user_data.bin', 'rb')
			
			content = (self.read_data(file)).split('\n')
			file.close()			

			for x in content:
				if x == '':
					break

				lines = x.strip().split(": ")
				
				if len(lines) != 2 or lines[0] not in data.i.keys():
					print("Data file is corrupted :(")
				else:
					if lines[0] != 'rank':
						data.i[lines[0]] = int(float(lines[1]))
					else:
						data.i[lines[0]] = eval(lines[1])

		except IOError:
			print("Creating a new data file...")
			self.save()

	def updateData(self):
		"""
		checks if the player unlocked a new achievement
		"""
		if data.i['lastUnlockedStages'] > 20:
			data.i['hacker'] = 1
		else:
			data.i['hacker'] = 0

		if data.i['lastUnlockedStages'] > 10:
			data.i['pilgrim'] = 1
		else:
			data.i['pilgrim'] = 0

		if data.i['ballsDestructed'] >= 42:  # universe age
			data.i['serialKiller'] = 1
		else:
			data.i['serialKiller'] = 0

		if data.i['hacker'] == 1 and data.i['pilgrim'] == 1 and data.i['serialKiller'] == 1 and \
						data.i['worldEmperor'] == 1 and data.i['immortal'] == 1 and data.i['pacifist'] == 1 and \
						data.i['yogaMaster'] == 1 and data.i['doubleKill'] == 1:
			data.i['jedi'] = 1
		else:
			data.i['jedi'] = 0

	def save(self):
		"""
		Save the data to the user's computer
		"""
		file = open('user_data\\user_data.bin', 'wb')
		self.updateData()
		for name, val in data.i.items():
			s = name + ": " + str(val) + "\n"
			self.write_data(file, s)
		file.close()

	def write_data(self, file, s):
		"""
		encrypts the data
		:param file: file that will store data information
		:param s: data that will be encrypted
		"""
		for k in s:
			file.write(bytes([255 - ord(k)])) #encript
			file.flush()

	def read_data(self, file):
		"""
		decrypts the data
		:param file: file that stores data information
		:return: data already decrypted
		"""
		s = ''
		x = file.read(1)
		while x != b'':
			s += chr(255 - int(binascii.hexlify(x), 16)) #decript
			x = file.read(1)
		return s
