'''
Created on Apr 18, 2019

@author: bryan
'''
from src.constants import RED_DARK



def deadPlayer(player):
    player.clrForeground = RED_DARK
    

def deadEnemy(enemy, map):
    enemy.clrForeground = RED_DARK
    map.aTcodMaps[map.intPlayerZ].walkable[enemy.y][enemy.x] = True