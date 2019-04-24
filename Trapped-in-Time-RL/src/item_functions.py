'''
---CHANGELOG---
2019/04/23		(JSS5783)
				Updated code. Items are picked up, can kill enemies, etc.

2019/04/19		(Bryan)
				Finished item use functions
				Added pick up item function
				Items have ammo/charge counters and max ammo/charge equippable

2019/04/18		(JSS5783)
				Modified getShield to work with new Map methods. (Also some story.)

2019/04/08		(Bryan)
				Created.

@author: bryan
'''
from src.constants import *
from src.GameStates import *
from src.Entity import *
from src.Map import *
from src.Status import *

		

def getBlaster(inMap, inLog, inStatus):
# 	for equip in INVENTORY:
# 		if equip.strName == "Blaster":
# 			equip.ammo += item.ammo
# 			if equip.ammo > equip.maxAmmo:
# 				equip.ammo = equip.maxAmmo
# 			break
# 	else:
# 		INVENTORY.append(item)
# 	
# 	inMap.aLstEntities[inMap.getPlayerX()][inMap.getPlayerY()][inMap.getPlayerZ()].remove(item)
	
# 	entPlayer = inMap.getTopEntity(inMap.getPlayerX(), inMap.getPlayerY() )
# 	entTarget = inMap.getEntityAt(inMap.getEntityIndexAt(Shield, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY() )
# 	intPosition = 0
# 	
# 	if DEBUG_MODE: print(len(INVENTORY) )
# 	if len(INVENTORY) > 0:
# 		for i in range(len(INVENTORY) ):
# 			if DEBUG_MODE: print("entering equip check")
# 			if isinstance(INVENTORY[i], Blaster):
# # 				intPos = i
# 				INVENTORY[i].currentAmmo += entTarget.currentAmmo
# 				if INVENTORY[i].currentAmmo > INVENTORY[i].maxAmmo:
# 					INVENTORY[i].currentAmmo = INVENTORY[i].maxAmmo
# 					inMap.removeEntityAtIndex(inMap.getEntityIndexAt(Blaster, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY())
# 					inLog.addMessage("You recharge your Blaster. It hums ominously.")
# 					inStatus.setRangedCurrent(INVENTORY[i].ammo)
# 					break
# 	else:
# # 		INVENTORY[i].ammo += entTarget.charges
# 		INVENTORY.append(inMap.getEntityAt(inMap.getEntityIndexAt(Blaster, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY()) )
# 		inMap.removeEntityAtIndex(inMap.getEntityIndexAt(Blaster, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY())
# 		inLog.addMessage("You pick up a Blaster module, slotting it into your device easily.")
# 		inLog.addMessage("\"[Right-click] an enemy to... blast it to bits.\"")
# 		inStatus.setRangedCurrent(INVENTORY[0].maxAmmo)
# 		inStatus.setRangedMax(INVENTORY[0].maxAmmo)
	
	entItem = inMap.getEntityAt(inMap.getEntityIndexAt(Blaster, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY() )
	intPosition = -1
	
	if DEBUG_MODE: print(len(INVENTORY) )
	if len(INVENTORY) > 0:
		for i in range(len(INVENTORY) ):
			if DEBUG_MODE: print("entering equip check")
			if isinstance(INVENTORY[i], Blaster):
				intPosition = i
				break
	
	if intPosition > -1:	#if has Blaster
		if INVENTORY[intPosition].currentAmmo + entItem.currentAmmo > INVENTORY[intPosition].maxAmmo:	#if recharged Blaster ammo would exceed maximum capacity
			INVENTORY[intPosition].currentAmmo = INVENTORY[intPosition].maxAmmo		#max out Blaster ammo
			inLog.addMessage("You recharge your Blaster. It hums ominously.")
		else:	#refill Blaster ammo
			INVENTORY[intPosition].currentAmmo = INVENTORY[intPosition].currentAmmo + entItem.currentAmmo
			inLog.addMessage("You recharge your Blaster.")
		inMap.removeEntityAtIndex(inMap.getEntityIndexAt(Blaster, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY())	#remove Blaster from Map tile
		inStatus.setRangedCurrent(INVENTORY[intPosition].currentAmmo)	#update Status
		
	else:	#if NO Blaster
		INVENTORY.append(entItem)	#equip Blaster
		inStatus.setRangedCurrent(entItem.currentAmmo)	#update Status
		inStatus.setRangedMax(entItem.maxAmmo)
		inMap.removeEntityAtIndex(inMap.getEntityIndexAt(Blaster, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY())	#remove Blaster from Map tile
		inLog.addMessage("You pick up a Blaster module, slotting it into your device easily.")
		inLog.addMessage("\"[Right-click] an enemy to... blast it to bits.\"")


def getFistoKit(inMap, inLog, inStatus):
	entItem = inMap.getEntityAt(inMap.getEntityIndexAt(FistoKit, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY() )
	intPosition = -1
	
	if DEBUG_MODE: print(len(INVENTORY) )
	if len(INVENTORY) > 0:
		for i in range(len(INVENTORY) ):
			if DEBUG_MODE: print("entering equip check")
			if isinstance(INVENTORY[i], FistoKit):
				intPosition = i
				break
	
	if intPosition > -1:	#if has FistoKit
		if INVENTORY[intPosition].currentCharges + entItem.currentCharges > INVENTORY[intPosition].maxCharges:	#if recharged FistoKit charges would exceed maximum capacity
			INVENTORY[intPosition].currentCharges = INVENTORY[intPosition].maxCharges		#max out FistoKit charges
			inLog.addMessage("You recharge your Fist-o-Kit. It glows menacingly.")
		else:	#refill FistoKit charges
			INVENTORY[intPosition].currentCharges = INVENTORY[intPosition].currentCharges + entItem.currentCharges
			inLog.addMessage("You recharge your Fist-o-Kit.")
		inMap.removeEntityAtIndex(inMap.getEntityIndexAt(FistoKit, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY())	#remove FistoKit from Map tile
		inStatus.setMeleeCurrent(INVENTORY[intPosition].currentCharges)	#update Status
		
	else:	#if NO FistoKit
		INVENTORY.append(entItem)	#equip FistoKit
		inStatus.setMeleeCurrent(entItem.currentCharges)	#update Status
		inStatus.setMeleeMax(entItem.maxCharges)
		inMap.removeEntityAtIndex(inMap.getEntityIndexAt(FistoKit, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY())	#remove FistoKit from Map tile
		inLog.addMessage("You pick up a Fist-o-Kit module, slotting it into your device easily.")
		inLog.addMessage("\"[Move into] an enemy to... power-punch it?\"")
		
# 	for equip in INVENTORY:
# 		if equip.strName == "Fisto Kit":
# 			equip.charges += item.charges
# 			if equip.charges > equip.maxCharges:
# 				equip.charges = equip.maxCharges
# 				break
# 	else:
# 		myPlayer.damage = item.damage
# 		INVENTORY.append(item)
# 
# 	inMap.aLstEntities[inMap.getPlayerX()][inMap.getPlayerY()][inMap.getPlayerZ()].remove(item)		


def getShield(inMap, inLog, inStatus):
	'''
	if inv empty, then position = 0
	else iterate over inventory to check for blaster/etc.
	
	if Blaster found,
		operate on blaster in inventory slot[i]
	else
		get new equip
	'''
	#i in len(INVENTORY) for index, but doesn't work if empty...
	#i in INVENTORY for "has ANY contents?", but no index
	entPlayer = inMap.getTopEntity(inMap.getPlayerX(), inMap.getPlayerY() )
	entItem = inMap.getEntityAt(inMap.getEntityIndexAt(Shield, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY() )
	intPosition = -1
	
	if DEBUG_MODE: print(len(INVENTORY) )
	if len(INVENTORY) > 0:
		for i in range(len(INVENTORY) ):
			if DEBUG_MODE: print("entering equip check")
			if isinstance(INVENTORY[i], Shield):
				intPosition = i
				break
	
	if intPosition > -1:	#if has Shield
		if entPlayer.hp + entItem.currentCharges > INVENTORY[intPosition].maxCharges + 1:	#if Player TOTAL health (Shield charges + Player's lone hit-point) > if Shield was added to it
			entPlayer.hp = INVENTORY[intPosition].maxCharges + 1	#max out Player health
			inLog.addMessage("You recharge your Shield. It shines faintly.")
		else:	#refill Player health
			entPlayer.hp = entItem.currentCharges + 1
			inLog.addMessage("You recharge your Shield.")
		inMap.removeEntityAtIndex(inMap.getEntityIndexAt(Shield, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY())	#remove Shield from Map tile
		inStatus.setShieldCurrent(entPlayer.hp)	#update Status
	else:	#if NO Shield
		entPlayer.hp = entItem.currentCharges + 1	#add Shield charges to Player health
		INVENTORY.append(inMap.getEntityAt(inMap.getEntityIndexAt(Shield, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY()) )	#equip Shield
		inMap.removeEntityAtIndex(inMap.getEntityIndexAt(Shield, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY())	#remove Shield from Map tile
		inLog.addMessage("You pick up a Shield module, slotting it into your device easily.")
		inLog.addMessage("\"This will protect me from extra blows, I think.\"")
		inStatus.setShieldCurrent(entPlayer.hp)	#update Status
		inStatus.setShieldMax(entItem.maxCharges)
	
# 	if len(INVENTORY) > 0:
# 		for i in range(len(INVENTORY) ):
# 			print("entering equip check")
# 			if isinstance(INVENTORY[i], Shield):
# 				entPlayer.hp += entTarget.charges
# 				if entPlayer.hp - 1 > INVENTORY[i].maxCharges:
# 					entPlayer.hp = INVENTORY[i].maxCharges + 1
# 					inMap.removeEntityAtIndex(inMap.getEntityIndexAt(Shield, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY())
# 					inLog.addMessage("You recharge your Shield. It shines faintly.")
# 					inStatus.setShieldCurrent(entPlayer.hp)
# 					break
# 	else:
# 		entPlayer.hp += entTarget.charges
# 		INVENTORY.append(inMap.getEntityAt(inMap.getEntityIndexAt(Shield, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY()) )
# 		inMap.removeEntityAtIndex(inMap.getEntityIndexAt(Shield, inMap.getPlayerX(), inMap.getPlayerY()), inMap.getPlayerX(), inMap.getPlayerY())
# 		inLog.addMessage("You pick up a Shield module, slotting it into your device easily.")
# 		inLog.addMessage("\"This... will protect me, I think.\"")
# 		inStatus.setShieldCurrent(entTarget.charges)
# 		inStatus.setShieldMax(entTarget.maxCharges)
			
# 	for equip in INVENTORY:
# 		if equip.strName == "Shield":
# 			inPlayer.hp += inShield.charges
# 			if inPlayer.hp-1 > equip.maxCharges:
# 				inPlayer.hp = equip.maxCharges+1
# 				break
# 	else:
# 		inPlayer.hp += inShield.charges
# 		INVENTORY.append(inShield)

def meleeAttack(inMap, inLog, inStatus, intInTargetX, intInTargetY, intInTargetZ=-1):
	if intInTargetZ == -1:
		intInTargetZ = inMap.getPlayerZ()

	intPosition = -1
	
	if DEBUG_MODE: print(len(INVENTORY) )
	if len(INVENTORY) > 0:
		for i in range(len(INVENTORY) ):
			if DEBUG_MODE: print("entering equip check")
			if isinstance(INVENTORY[i], FistoKit):
				intPosition = i
				break
	
	if intPosition > -1:
		equip = INVENTORY[intPosition]
		target = inMap.getTopEntity(intInTargetX, intInTargetY, intInTargetZ)
		
		if equip.currentCharges > 0 and isinstance(target, Enemy):
			inLog.addMessage("You punch the "  + type(target).__name__ + "!")
			target.hp -= equip.damage
			equip.currentCharges -= 1
			inStatus.setMeleeCurrent(equip.currentCharges)
# 		if INVENTORY[intPosition].currentCharges > 0 and isinstance(inMap.getTopEntity(intInTargetX, intInTargetY, intInTargetZ), Enemy):
# 			inLog.addMessage("You punch the "  + type(inMap.getTopEntity(intInTargetX, intInTargetY, intInTargetZ) ).__name__ + "!")
# 			inMap.getTopEntity(intInTargetX, intInTargetY, intInTargetZ).hp -= INVENTORY[intPosition].damage
# 			INVENTORY[intPosition].currentCharges -= 1
# 			inStatus.setMeleeCurrent(INVENTORY[intPosition].currentCharges)
		else:	#if out of ammo
			inLog.addMessage("Lights dark, your Fist-o-Kit refuses to budge.")


def useBlaster(inMap, inLog, inStatus, intInTargetX, intInTargetY, intInTargetZ=-1):
	if intInTargetZ == -1:
		intInTargetZ = inMap.getPlayerZ()

	intPosition = -1
	
	if DEBUG_MODE: print(len(INVENTORY) )
	if len(INVENTORY) > 0:
		for i in range(len(INVENTORY) ):
			if DEBUG_MODE: print("entering equip check")
			if isinstance(INVENTORY[i], Blaster):
				intPosition = i
				break
	
	if intPosition > -1:	#if has Blaster
		equip = INVENTORY[intPosition]
		target = inMap.getTopEntity(intInTargetX, intInTargetY, intInTargetZ)
		
		if equip.currentAmmo > 0 and isinstance(target, Enemy):	#if has ammo
			inLog.addMessage("You blast the "  + type(target).__name__ + "!")
			target.hp -= equip.damage
			equip.currentAmmo -= 1
			inStatus.setRangedCurrent(equip.currentAmmo)
		else:	#if out of ammo
			inLog.addMessage("Lacking ammo, your Blaster sparks uselessly.")
	