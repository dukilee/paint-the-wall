import data

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
					data.i[lines[0]] = int(lines[1])

			file.close()
		except IOError:
			print("Creating a new data file...")
			self.save()


	def load(self, file):
		return val

	def save(self):
		file = open('data.txt', 'w')
		for name, val in data.i.items():
			s = name + ": " + str(val) + "\n"
			file.write(s)
		file.close()

	def __del__(self):
		self.save()
		print("Data successfully saved!! :)");
		