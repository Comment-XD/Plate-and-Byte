from datetime import datetime

import Menu

class Data:
    def __init__(self):
        self.sales = [] #List of all past sales, Tuple Format (Item, Time)
        self.menu = Menu()

    def addSale(self,itemName,Time = datetime.now()):
        pass