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
					data.i[lines[0]] = int(float(lines[1]))

		except IOError:
			print("Creating a new data file...")
			self.save()

	def load(self, file):
		return val

	def save(self):
		file = open('user_data\\user_data.bin', 'wb')
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