import sprites
import time
import pygame

i = {'timePlayed': 0, 'blocksConquered': 0, 'deaths': 0, 'ballsDestructed': 0,
		'lastUnlockedStages': 10, 'theme':0,
		#achievements
		'doubleKill': 0, 'worldEmperor': 0, 'yogaMaster': 0, 'immortal': 0, 'jedi':0,
	 	'pilgrim': 0, 'hacker': 0, 'pacifist': 0, 'serialKiller':0,
		#settings
		'musicVolume': 100, 'effectsVolume':100}

print("inicioa")
leftWingSprite = [sprites.sprite('wing1Mini.png'), sprites.sprite('wing2Mini.png'),
				  	sprites.sprite('wing3Mini.png'), sprites.sprite('fullWingMini.png')]

startTime = 0
def getActualTime():
	return int(time.mktime(time.localtime( )) - startTime)
