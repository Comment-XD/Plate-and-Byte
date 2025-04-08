

class Menu:
    def __init__(self):
        self.itemList = [] #list of items, Tuple Format (Item Name, Price)

    def addItem(self, itemName, price):
        try:
            self.itemList.append((str(itemName),float(price)))
            return True
        except Exception:
            print("---Error in AddItem Method---")
            print("Inputs: \"" + str(itemName)+"\", " + str(price))
            return False
    def getItem(self,itemName):
        for item in self.itemsList:
            if item[0] == itemName:
                return item
        print("Not an Item")
