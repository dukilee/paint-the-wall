import pygame
import time

from audiovisual import theme

"""
	stores every information about the game, as the achievements, time played, achievements
	and rank information of suvival mode.
"""

new_score, new_player = 0, '-'

startTime = 0
already = False
def getActualTime():
	return int(time.mktime(time.localtime( )) - startTime)

i = {'timePlayed': 0, 'blocksConquered': 0, 'deaths': 0, 'ballsDestructed': 0,
		'lastUnlockedStages': 1, 'theme':0,
		#achievements
		'doubleKill': 0, 'worldEmperor': 0, 'yogaMaster': 0, 'immortal': 0, 'jedi':0,
	 	'pilgrim': 0, 'hacker': 0, 'pacifist': 0, 'serialKiller':0,
		#settings
		'musicVolume': 100, 'effectsVolume':100, 'rank': [('-', 0) for k in range(10)]}

leftWingSprite = [theme.sprite('wing1Mini.png'), theme.sprite('wing2Mini.png'),
				  	theme.sprite('wing3Mini.png'), theme.sprite('fullWingMini.png')]

def insert_rank():
	i['rank'].append((new_player, new_score))
	i['rank'] = sorted(i['rank'], key = lambda x: x[1])[::-1]
	i['rank'].pop(-1)

menu_vol, game_vol = 1.0, 1.0
old_music, old_sfx = 1.0, 1.0
vol_max, sfx_max = 1.0, 1.0