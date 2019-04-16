'''
Created on Apr 8, 2019

@author: bryan
'''
from src.constants import INVENTORY
def useBlaster(enemy, item):
    
    
    if item.ammo > 0:
        enemy.hp -= item.damage
        item.ammo -= 1
    else:
        print("weapon is empty")
        

def getBlaster(item):
    
    for equip in INVENTORY:
        if equip.strName == "Blaster":
            equip.ammo += item.ammo
            if equip.ammo > equip.maxAmmo:
                equip.ammo = equip.maxAmmo
                break
    else:
        INVENTORY.append(item)
        

def getFistoKit(item, myPlayer):
    
    for equip in INVENTORY:
        if equip.strName == "Fisto Kit":
            equip.charges += item.charges
            if equip.charges > equip.maxCharges:
                equip.charges = equip.maxCharges
                break
    else:
        myPlayer.damage = item.damage
        INVENTORY.append(item)
            

def getSheild(item, myPlayer):
    
    for equip in INVENTORY:
        if equip.strName == "Shield":
            myPlayer.hp += item.charges
            if myPlayer.hp-1 > equip.maxCharges:
                myPlayer.hp = equip.maxCharges+1
                break
    else:
        myPlayer.hp += item.charges
        INVENTORY.append(item)        