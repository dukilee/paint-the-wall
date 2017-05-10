import pygame

from user_data import data
from audiovisual import theme


pygame.init()


music = pygame.mixer.music
sfx = pygame.mixer
currentMusic = None
sfx_arq = { 'conquering': 'resources/sounds/conquering.wav', 'conquered': 'resources/sounds/conquered.wav' }
sfx_list = { k: pygame.mixer.Sound(sfx_arq[k]) for k in sfx_arq }

def setMusicVolume(val = -1, icon = None):
    """
    Change music volume to val
    :param val: new value to volume
    :param icon: sprite to mute/unmute
    """
    if val == -1:
        val = data.i['musicVolume']
    else:
        data.i['musicVolume'] = val
    data.vol_max = val / 100.0
    data.old_music = val / 100.0
    music.set_volume(val / 100.0)
    if icon != None:
        if data.vol_max == 0.0 and data.sfx_max == 0.0:
            icon.turn_off()
            icon.is_on = False
        else:
            icon.turn_on()
            icon.is_on = True




def setEffectsVolume(val = -1, icon = None):
    """
    Change sound effects volume to val
    :param val: new value to volume
    :param icon: sprite to mute/unmute
    """
    if val == -1:
        val = data.i['effectsVolume']
    else:
        data.i['effectsVolume'] = val
    data.sfx_max = val / 100.0
    data.old_sfx = val / 100.0
    for k in sfx_list:
        # play_music(sfx, 1.0, 0)
        sfx_list[k].set_volume(data.i['effectsVolume']/100.0)
    sfx_list['conquering'].play()
    if icon != None:
        if data.vol_max < 0.05 and data.sfx_max < 0.05:
            icon.turn_off()
            icon.is_on = False
        else:
            icon.turn_on()
            icon.is_on = True

def mute(icon, is_on):
    """
    Change music volume to 0
    :param icon: sprite to mute/unmute
    :param is_on: bool representing if the soun was already mute
    """
    if not is_on:
        icon.turn_on()
        data.i['musicVolume'] = data.old_music
        data.vol_max = data.old_music
        data.sfx_max = data.old_sfx
        music.set_volume(data.i['musicVolume'])
        for k in theme.sfx_list:
            theme.sfx_list[k].set_volume(data.sfx_max)
    else:
        icon.turn_off()
        data.vol_max = 0.0
        data.sfx_max = 0.0
        data.i['musicVolume'] = 0
        music.set_volume(0)
        for k in theme.sfx_list:
            theme.sfx_list[k].set_volume(0)
    return not is_on


def play_music(path, vol = 1.0, rep = -1):
    """
    starts the music
    :param path: name of the archive in the computer
    :param vol: volume of the music
    :param rep: number of repetitions
    """
    global music, vol_max
    if path == 'conquering' or path == 'conquered':
        sfx_list[path].play()
    else:
        global currentMusic
        if currentMusic != path:
            currentMusic = path
            music.stop()
            music.load(path)
            setMusicVolume()
            music.play(rep)