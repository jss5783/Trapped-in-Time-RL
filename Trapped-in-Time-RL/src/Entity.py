'''
---CHANGELOG---
2019/04/16		(Bryan)
				Updated Item classes (Blaster, Shield, and Fisto Kit) as needed
				Updated Player and Enemy classes enough for item testing (may need further updating)
				
2019/04/05		(JSS5783)
				Finished reworking code. Creating a new Entity type in code is simpler now.

2019/03/29		(JSS5783)
				Added strict typing as a test.

2019/03/27		(JSS5783)
				Created main.py.
				Hard-coded entities.
'''


from src.constants import *


class Entity:
	def __init__(self, cInSymbol='?', strInName="UNDEFINED (please report to developers)", clrInForeground=MAGENTA_DARK, clrInBackground=GREEN_DARK, bInIsSolid=True, bInIsTranslucent=False):
		'''
			Entity constructor.
			Uses ear-searing default colors to help identify generation errors.
		'''
		self.cSymbol = cInSymbol
		self.strName = strInName
		self.clrForeground = clrInForeground
		self.clrBackground = clrInBackground
		self.bIsSolid = bInIsSolid
		self.bIsTransparent = bInIsTranslucent
	#END __init__(self, cInSymbol='?', strInName="UNDEFINED (please report to developers)", clrInForeground=MAGENTA_DARK, clrInBackground=GREEN_DARK, bInIsSolid=True, bInIsTranslucent=False)
	
	
	def setSymbol(self, cInSymbol):
		'''
		Set Entity symbol.
		The symbol is the character used to represent an Entity on the screen, and must be found in CP437 (https://en.wikipedia.org/wiki/Code_page_437).
		'''
		self.cSymbol = cInSymbol
	#END setSymbol(self, cInSymbol)
		
	def getSymbol(self):
		'''
		Get Entity symbol.
		The symbol is the character used to represent an Entity on the screen.
		'''
		return self.cSymbol
	#END getSymbol(self)
	
	
	def setName(self, strInName):
		'''
		Set Entity name.
		'''
		self.strName = strInName
	#END setName(self, strInName)
	
	def getName(self):
		'''
		Get Entity name.
		'''
		return self.strName
	#END getName(self)


	def setFGColor(self, clrInForeground):
		'''
		Set Entity foreground color (text color).
		'''
		self.clrForeground = clrInForeground
	#END setFGColor(self, clrInForeground)
	
	def getFGColor(self):
		'''
		Get Entity foreground color (text color).
		'''
		return self.clrForeground
	#END getFGColor(self)
	
	
	def setBGColor(self, clrInBackground):
		'''
		Set Entity background color (color behind text).
		'''
		self.clrBackground = clrInBackground
	#END setBGColor(self, clrInBackground)
	
	def getBGColor(self):
		'''
		Get Entity background color (color behind text).
		'''
		return self.clrBackground
	#END getBGColor(self)
#END Entity


class Wall(Entity):
	def __init__(self):
		super().__init__('#', "wall", WHITE, BLACK, True, False)
#END Wall(Entity)


class Floor(Entity):
	def __init__(self):
		super().__init__('.', "floor", GRAY_LIGHT, BLACK, False, True)
#END Floor(Entity)


class Enemy(Entity):
	def __init__(self, x, y, hp):
		super().__init__('E', "enemy", ORANGE_LIGHT, BLACK, True, True)
		self.x = x
		self.y = y 
		self.hp = hp
#END Enemy(Entity)


class Player(Entity):
	def __init__(self, hp=1, damage=0):
		super().__init__('@', "player", WHITE, BLACK, True, True)
		self.hp = hp
		self.damage = damage
#END Player(Entity)




class Shield(Entity):
	def __init__(self, x, y, charges, maxCharges):
		super().__init__('¿', "Shield", BLUE_LIGHT, BLACK, False, True)
		self.x = x
		self.y = y
		self.charges = charges
		self.maxCharges = maxCharges
		


class FistoKit(Entity):
	def __init__(self, x, y, charges, maxCharges, damage):
		super().__init__('¡', "Fisto Kit", BLUE_LIGHT, BLACK, False, True)
		self.x = x
		self.y = y
		self.charges = charges
		self.maxCharges = maxCharges
		self.damage = damage
		
#END HealthConsumable(Entity)


class Blaster(Entity):
	def __init__(self, x, y, ammo, maxAmmo, damage):
		super().__init__(',', "Blaster", BLUE_LIGHT, BLACK, False, True)
		self.x = x
		self.y = y
		self.ammo = ammo
		self.maxAmmo = maxAmmo
		self.damage = damage
		
#END Ammo(Entity)


class Portal(Entity):
	'''
	Level's end.
	'''
	def __init__(self):
		super().__init__('☼', "portal", BLUE_LIGHT, BLACK, True, True)
#END Portal(Entity)


class GateOpen(Entity):
	'''
	Open state of gate.
	'''
	def __init__(self):
		super().__init__('▬', "gate (open)", BLUE_LIGHT, BLACK, False, True)
#END GateOpen(Entity)


class GateClosed(Entity):
	'''
	Closed state of gate.
	'''
	def __init__(self):
		super().__init__('╬', "gate (closed)", BLACK, ORANGE_LIGHT, True, False)
#END GateClosed(Entity)
