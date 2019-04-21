'''
Created on Apr 4, 2019

@author: bryan

Item class is used to make the equippable items in the game.
May need modifications to this class later.
'''
class Item:
    def __init__(self, x, y, strName, maxcharges, charges, damage=None):
        self.x = x      # position in x coordinate
        self.y = y      # position in y coordinate
        self.strName = strName      # Name of item
        self.maxcharges = maxcharges    # Maximum charges/ammo for item
        self.charges = charges      # Number of charges/ammo for item
        self.damage = damage        # Amount of damage for weapon, no argument need be passed (ex: shield does no damage)
        #self.useFunction = useFunction
        
class Baddie:
    def __init__(self, hp, x, y, z):
        self.x = x 
        self.y = y
        self.z = z
        self.hp = hp