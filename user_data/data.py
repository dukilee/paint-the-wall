import pygame
import time

from resources import tools

rank_tam = 10
ranking = [('-', 0) for k in range(rank_tam)]
new_score, new_player = 0, '-'

i = {'timePlayed': 0, 'blocksConquered': 0, 'deaths': 0, 'ballsDestructed': 0,
		'lastUnlockedStages': 10, 'theme':0,
		#achievements
		'doubleKill': 0, 'worldEmperor': 0, 'yogaMaster': 0, 'immortal': 0, 'jedi':0,
	 	'pilgrim': 0, 'hacker': 0, 'pacifist': 0, 'serialKiller':0,
		#settings
		'musicVolume': 100, 'effectsVolume':100}

#print("inicio")
leftWingSprite = [tools.sprite('wing1Mini.png'), tools.sprite('wing2Mini.png'),
				  	tools.sprite('wing3Mini.png'), tools.sprite('fullWingMini.png')]

startTime = 0
def getActualTime():
	return int(time.mktime(time.localtime( )) - startTime)

def insert_rank():
	global ranking, new_score, new_player
	ranking.append((new_player, new_score))
	ranking = sorted(ranking, key = lambda x: x[1])[::-1]
	ranking.pop(-1)