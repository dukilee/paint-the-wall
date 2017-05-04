import binascii

from user_data import data

class DataManager:
	def __init__(self):
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
		file = open('user_data\\user_data.bin', 'wb')
		self.updateData()
		for name, val in data.i.items():
			s = name + ": " + str(val) + "\n"
			self.write_data(file, s)
		file.close()

	def write_data(self, file, s):
		for k in s:
			file.write(bytes([255 - ord(k)])) #encript
			file.flush()

	def read_data(self, file):
		s = ''
		x = file.read(1)
		while x != b'':
			s += chr(255 - int(binascii.hexlify(x), 16)) #decript
			x = file.read(1)
		return s

# class DataManager:
# 	def __init__(self):
# 		try:
# 			file = open('data.txt', 'r')
#
# 			content = file.readlines()
# 			for x in content:
# 				lines = x.strip().split(": ")
#
# 				if len(lines) != 2 or lines[0] not in data.i.keys():
# 					print("Data file is corrupted :(")
# 				else:
# 					data.i[lines[0]] = int(float(lines[1]))
#
# 			file.close()
# 		except IOError:
# 			print("Creating a new data file...")
# 			self.save()
#
# 	def updateData(self):
# 		if data.i['lastUnlockedStages'] > 20:
# 			data.i['hacker'] = 1
# 		else:
# 			data.i['hacker'] = 0
#
# 		if data.i['lastUnlockedStages'] > 10:
# 			data.i['pilgrim'] = 1
# 		else:
# 			data.i['pilgrim'] = 0
#
# 		if data.i['ballsDestructed'] > 42:  # universe age
# 			data.i['serialKiller'] = 1
# 		else:
# 			data.i['serialKiller'] = 0
#
# 		if data.i['hacker'] == 1 and data.i['pilgrim'] == 1 and data.i['serialKiller'] == 1 and \
# 						data.i['worldEmperor'] == 1 and data.i['immortal'] == 1 and data.i['pacifist'] == 1 and \
# 						data.i['yogaMaster'] == 1 and data.i['doubleKill'] == 1:
# 			data.i['jedi'] = 1
# 		else:
# 			data.i['jedi'] = 0
#
# 	def save(self):
# 		file = open('data.txt', 'w')
# 		for name, val in data.i.items():
# 			s = name + ": " + str(val) + "\n"
# 			file.write(s)
# 		file.close()
#