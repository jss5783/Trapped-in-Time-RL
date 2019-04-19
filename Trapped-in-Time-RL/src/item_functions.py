'''
Created on Apr 8, 2019

@author: bryan

---CHANGELOG---
2019/04/19        (Bryan)
                Finished item use functions
                Added pick up item function
                Items have ammo/charge counters and max ammo/charge equippable
'''
from src.constants import INVENTORY, ITEMS
def useBlaster(enemy, item):
    
    
    if item.ammo > 0:
        enemy.hp -= item.damage
        item.ammo -= 1
    else:
        print("weapon is empty")
        
def meleeAttack(player, enemy):
    for equip in INVENTORY:
        if equip.strName == "Fisto Kit" and equip.charges > 0:
            enemy.hp -= player.damage
            equip.charges -= 1
            print(enemy.hp)
            print(equip.charges)
    
def getBlaster(item, inMap):
    
    for equip in INVENTORY:
        if equip.strName == "Blaster":
            equip.ammo += item.ammo
            if equip.ammo > equip.maxAmmo:
                equip.ammo = equip.maxAmmo
            break
    else:
        INVENTORY.append(item)
    
    inMap.aLstEntities[inMap.getPlayerX()][inMap.getPlayerY()][inMap.getPlayerZ()].remove(item)
        

def getFistoKit(item, myPlayer, inMap):
    
    for equip in INVENTORY:
        if equip.strName == "Fisto Kit":
            equip.charges += item.charges
            if equip.charges > equip.maxCharges:
                equip.charges = equip.maxCharges
            break
    else:
        myPlayer.damage = item.damage
        INVENTORY.append(item)
    
    inMap.aLstEntities[inMap.getPlayerX()][inMap.getPlayerY()][inMap.getPlayerZ()].remove(item)        

def getSheild(item, myPlayer, inMap):
    
    for equip in INVENTORY:
        if equip.strName == "Shield":
            myPlayer.hp += item.charges
            if myPlayer.hp-1 > equip.maxCharges:
                myPlayer.hp = equip.maxCharges+1
            break
    else:
        myPlayer.hp += item.charges
        INVENTORY.append(item)
    
    inMap.aLstEntities[inMap.getPlayerX()][inMap.getPlayerY()][inMap.getPlayerZ()].remove(item)        