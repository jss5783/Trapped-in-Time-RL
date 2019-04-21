'''

2019/04/18		(JSS5783)
				Modified getShield to work with new Map methods. (Also some story.)

Created on Apr 8, 2019

@author: bryan
'''
from src.constants import INVENTORY
from src.Entity import *
from src.Map import *
from src.Status import *

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


# def getShield(inShield, inPlayer):
def getShield(inMap, inLog, inStatus):
	#i in len(INVENTORY) for index, but doesn't work if empty...
	#i in INVENTORY for "has ANY contents?", but no index
	entPlayer = inMap.getTopEntity(inMap.getPlayerX(), inMap.getPlayerY() )
	entTarget = inMap.getEntityAt(inMap.getEntityIndexAt(Shield, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY() )
	
	print(len(INVENTORY) )
	if len(INVENTORY) > 0:
		for i in range(len(INVENTORY) ):
			print("entering equip check")
			if isinstance(INVENTORY[i], Shield):
# 				inMap.getTopEntity(inMap.getPlayerX(), inMap.getPlayerY()).hp += inMap.getEntityAt(inMap.getEntityIndexAt(Shield, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY()).charges
# 				if inMap.getTopEntity(inMap.getPlayerX(), inMap.getPlayerY()).hp - 1 > INVENTORY[i].maxCharges:
# 					inMap.getTopEntity(inMap.getPlayerX(), inMap.getPlayerY()).hp = INVENTORY[i].maxCharges + 1
# 					inMap.removeEntityAtIndex(inMap.getEntityIndexAt(Shield, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY())
# 					inLog.addMessage("You recharge your Shield.")
# 					break
# 	else:
# 		inMap.getTopEntity(inMap.getPlayerX(), inMap.getPlayerY()).hp += inMap.getEntityAt(inMap.getEntityIndexAt(Shield, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY()).charges
# 		INVENTORY.append(inMap.getEntityAt(inMap.getEntityIndexAt(Shield, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY()) )
# 		inMap.removeEntityAtIndex(inMap.getEntityIndexAt(Shield, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY())
# 		inLog.addMessage("You pick up a Shield.")
# 		inLog.addMessage("\"This... will protect me, I think.\"")
# 		HAS_SHIELD = True
				entPlayer.hp += entTarget.charges
				if entPlayer.hp - 1 > INVENTORY[i].maxCharges:
					entPlayer.hp = INVENTORY[i].maxCharges + 1
					inMap.removeEntityAtIndex(inMap.getEntityIndexAt(Shield, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY())
					inLog.addMessage("You recharge your Shield. It shines faintly.")
					inStatus.setShieldCurrent(entPlayer.hp)
					break
	else:
		entPlayer.hp += entTarget.charges
		INVENTORY.append(inMap.getEntityAt(inMap.getEntityIndexAt(Shield, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY()) )
		inMap.removeEntityAtIndex(inMap.getEntityIndexAt(Shield, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY())
		inLog.addMessage("You pick up a Shield module, slotting it into your device easily.")
		inLog.addMessage("\"This... will protect me, I think.\"")
		inStatus.setShieldCurrent(entTarget.charges)
		inStatus.setShieldMax(entTarget.maxCharges)
			
# 	for equip in INVENTORY:
# 		if equip.strName == "Shield":
# 			inPlayer.hp += inShield.charges
# 			if inPlayer.hp-1 > equip.maxCharges:
# 				inPlayer.hp = equip.maxCharges+1
# 				break
# 	else:
# 		inPlayer.hp += inShield.charges
# 		INVENTORY.append(inShield)		