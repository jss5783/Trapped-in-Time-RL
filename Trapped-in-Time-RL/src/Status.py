'''
---CHANGELOG---
2019/04/18		(JSS5783)
				Created from MessageLog of the same date.
				Implemented tooltip.
				Implemented shield.
				Implemented timeline.
'''

import tcod
from src.constants import *
import textwrap


class Status:
	def __init__(self):
		self.intWidth = STATUS_WIDTH
		self.intHeight = STATUS_HEIGHT
		self.lstStatus = [str() for i in range(5)]	#store strings in here; corresponds to variable order in comment below SO BE CAREFUL WHEN EDITING CODE
		'''
			0: "strTooltip"
			1: "intShieldCurrent / intShieldMax"
			2: "intMeleeCurrent / intMeleeMax"
			3: "intRangedCurrent / intRangedMax"
			4: "intTimeline"
		'''
		
		#shield (HP), melee weapon (charges/total), ranged weapon (charges/total), mouseover, timeline
		self.strTooltip = ""
		self.intShieldCurrent = -1
		self.intShieldMax = -1
		self.intMeleeCurrent = -1
		self.intMeleeMax = -1
		self.intRangedCurrent = -1
		self.intRangedMax = -1
		self.intTimeline = 0	#TODO (real): set to -1, as the player may eventually start in a non-first-timeline
		self.updateTooltip()
		self.updateShield()
		self.updateMelee()
		self.updateRanged()
		self.updateTimeline()
		self.bHasShield = False
		self.bHasMelee = False
		self.bHasRanged = False


	'''
		Getters/setters for Status variables.
		Enables UI element when Shield is obtained, for example.
	'''
	def setTooltip(self, strInTooltip):
		self.strTooltip = strInTooltip
		self.updateTooltip()
	
	def getTooltip(self):
		return self.strTooltip
	
	def updateTooltip(self):
		self.lstStatus[0] = self.strTooltip


	def setShieldCurrent(self, intInShieldCurrent):
		self.intShieldCurrent = intInShieldCurrent
		if not self.bHasShield: self.bHasShield = True
		self.updateShield()
	
	def getShieldCurrent(self):
		return self.intShieldCurrent

	def setShieldMax(self, intInShieldMax):
		self.intShieldMax = intInShieldMax
		self.updateShield()
		if not self.bHasShield: self.bHasShield = True
	
	def getShieldMax(self):
		return self.intShieldMax
	
	def updateShield(self):
		self.lstStatus[1] = "Shield: " + str(self.intShieldCurrent) + "/" + str(self.intShieldMax)


	def setMeleeCurrent(self, intInMeleeCurrent):
		self.intMeleeCurrent = intInMeleeCurrent
		self.updateMelee()
		if not self.bHasMelee: self.bHasMelee = True
	
	def getMeleeCurrent(self):
		return self.intMeleeCurrent

	def setMeleeMax(self, intInMeleeMax):
		self.intMeleeMax = intInMeleeMax
		self.updateMelee()
		if not self.bHasMelee: self.bHasMelee = True
	
	def getMeleeMax(self):
		return self.intMeleeMax

	def updateMelee(self):
		self.lstStatus[2] = "Fist: " + str(self.intMeleeCurrent) + "/" + str(self.intMeleeMax)


	def setRangedCurrent(self, intInRangedCurrent):
		self.intRangedCurrent = intInRangedCurrent
		self.updateRanged()
		if not self.bHasRanged: self.bHasRanged = True
	
	def getRangedCurrent(self):
		return self.intRangedCurrent

	def setRangedMax(self, intInRangedMax):
		self.intRangedMax = intInRangedMax
		self.updateRanged()
		if not self.bHasRanged: self.bHasRanged = True
	
	def getRangedMax(self):
		return self.intRangedMax

	def updateRanged(self):
		self.lstStatus[3] = "Ranged: " + str(self.intRangedCurrent) + "/" + str(self.intRangedMax)


	def setTimeline(self, intInTimeline):
		'''
		Sets timeline.
		'''
		self.intTimeline = intInTimeline
		self.updateTimeline()
	
	def getTimeline(self):
		return self.intTimeline
	
	def updateTimeline(self):
		'''
		NOTE: Timelines in code are 0-based index (0-9). Timelines in user interface are "numrow 1-9, followed by 0".
		'''
		if (self.intTimeline >= 0 and self.intTimeline <= 8): #first to ninth timelines
			self.lstStatus[4] = "Timeline: " + str(self.intTimeline + 1)
		elif (self.intTimeline == 9):	#tenth timeline
			self.lstStatus[4] = "Timeline: 0"
		else:
			self.lstStatus[4] = "Timeline: ERROR"

	
	def printStatus(self, inConsole : tcod.console.Console):
		'''
		Draws status on console.
		'''
		inConsole.print_(0, MAP_HEIGHT, self.lstStatus[0])
		if self.bHasShield: inConsole.print_(0, MAP_HEIGHT + 1, self.lstStatus[1])
		if self.bHasMelee: inConsole.print_(0, MAP_HEIGHT + 2, self.lstStatus[2])
		if self.bHasRanged: inConsole.print_(0, MAP_HEIGHT + 3, self.lstStatus[3])
		inConsole.print_(0, MAP_HEIGHT + 4, self.lstStatus[4])
