'''
Created on Apr 18, 2019

@author: bryan
'''
from enum import Enum


class GameStates(Enum):
    PLAYERS_TURN = 1
    ENEMY_TURN = 2
    PLAYER_DEAD = 3
    LEVEL_UP = 4
    END_GAME = 5
    
