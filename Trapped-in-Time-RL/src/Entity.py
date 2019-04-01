'''
---CHANGELOG---
2019/03/29		(JSS5783)
				Added strict typing as a test.

2019/03/27		(JSS5783)
				Created main.py.
				Hard-coded entities.
'''

from src.constants import * 

class Entity:
# 	def __init__(self, cInSymbol, strInName, clrInForeground, clrInBackground=None):
	def __init__(self):
		self.cSymbol : char = '?'				#experimenting with static types here, since these variables are so predictable
		self.strName : str = "UNDEFINED (please report to developers)"			#also, ear-searing defaults in case of generation errors
		self.clrForeground : MAGENTA_DARK
		self.clrBackground : GREEN_DARK
		self.bIsSolid : bool
		self.bIsTranslucent : bool	#or translucent
	
	def setSymbol(self, cInSymbol):
		self.cSymbol = cInSymbol
		
	def getSymbol(self):
		return self.cSymbol
	
	def setName(self, strInName):
		self.strName = strInName
	
	def getName(self):
		return self.strName

	def setFGColor(self, clrInForeground):
		self.clrForeground = clrInForeground
	
	def getFGColor(self):
		return self.clrForeground
	
	def setBGColor(self, clrInBackground):
		self.clrBackground = clrInBackground
	
	def getBGColor(self):
		return self.clrBackground
#END Entity


class Wall(Entity):
	def __init__(self, cInSymbol='#', strInName="wall", clrInForeground=WHITE, clrInBackground=BLACK):
		self.cSymbol = cInSymbol
		self.strName = strInName
		self.clrForeground = clrInForeground
		self.clrBackground = clrInBackground

class Floor(Entity):
	def __init__(self, cInSymbol='.', strInName="floor", clrInForeground=GRAY_LIGHT, clrInBackground=BLACK):
		self.cSymbol = cInSymbol
		self.strName = strInName
		self.clrForeground = clrInForeground
		self.clrBackground = clrInBackground

class Enemy(Entity):
	def __init__(self, cInSymbol='E', strInName="enemy", clrInForeground=ORANGE_LIGHT, clrInBackground=BLACK):
		self.cSymbol = cInSymbol
		self.strName = strInName
		self.clrForeground = clrInForeground
		self.clrBackground = clrInBackground

class Player(Entity):
	def __init__(self, cInSymbol='@', strInName="player", clrInForeground=WHITE, clrInBackground=BLACK):
		self.cSymbol = cInSymbol
		self.strName = strInName
		self.clrForeground = clrInForeground
		self.clrBackground = clrInBackground

class ShieldConsumable(Entity):
	def __init__(self, cInSymbol='¿', strInName="shield repair kit", clrInForeground=BLUE_LIGHT, clrInBackground=BLACK):
		self.cSymbol = cInSymbol
		self.strName = strInName
		self.clrForeground = clrInForeground
		self.clrBackground = clrInBackground

class HealthConsumable(Entity):
	def __init__(self, cInSymbol='¡', strInName="medical kit", clrInForeground=BLUE_LIGHT, clrInBackground=BLACK):
		self.cSymbol = cInSymbol
		self.strName = strInName
		self.clrForeground = clrInForeground
		self.clrBackground = clrInBackground

class Ammo(Entity):
	def __init__(self, cInSymbol=',', strInName="pistol bullet", clrInForeground=BLUE_LIGHT, clrInBackground=BLACK):
		self.cSymbol = cInSymbol
		self.strName = strInName
		self.clrForeground = clrInForeground
		self.clrBackground = clrInBackground

class Portal(Entity):
	def __init__(self, cInSymbol='☼', strInName="portal", clrInForeground=BLUE_LIGHT, clrInBackground=BLACK):
		self.cSymbol = cInSymbol
		self.strName = strInName
		self.clrForeground = clrInForeground
		self.clrBackground = clrInBackground

class GateOpen(Entity):
	def __init__(self, cInSymbol='▬', strInName="gate (open)", clrInForeground=BLUE_LIGHT, clrInBackground=BLACK):
		self.cSymbol = cInSymbol
		self.strName = strInName
		self.clrForeground = clrInForeground
		self.clrBackground = clrInBackground

class GateClosed(Entity):
	def __init__(self, cInSymbol='╬', strInName="gate (closed)", clrInForeground=BLACK, clrInBackground=ORANGE_LIGHT):
		self.cSymbol = cInSymbol
		self.strName = strInName
		self.clrForeground = clrInForeground
		self.clrBackground = clrInBackground

