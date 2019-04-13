'''
Created on Apr 8, 2019

@author: bryan
'''
def useBlaster(enemy, item):
    
    
    if item.charges > 0:
        enemy.hp -= item.damage
        item.charges -= 1
    else:
        print("weapon is empty")