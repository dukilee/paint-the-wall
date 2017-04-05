import time
x = 0

while True:
	y = int(time.clock())
	if y != x:
		print(y)
		x = y
