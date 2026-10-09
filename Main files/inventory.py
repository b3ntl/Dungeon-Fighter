class Inventory:
    def __init__(self, size=5):
        self.size = size    #size of inventory
        self.items = [] #inventory list

    #add item to inventory
    def add_item(self, item):
        if len(self.items) < self.size: #if there is space in the inventory
            self.items.append(item) #append to list
            return True
        return False

    #use item
    def use_item(self, index, player):
        if 0 <= index < len(self.items):    #indexes how many items are in the inventory
            item = self.items.pop(index)    #remove from inventory
            item.effect(player) #effect on player