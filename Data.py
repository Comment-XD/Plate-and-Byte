from datetime import datetime

import Menu

class Data:
    def __init__(self):
        self.sales = [] #List of all past sales, Tuple Format (Item, Time)
        self.menu = Menu()

    def AddSale(self,itemName,Time = datetime.now()):
        if str(itemName) in
        self.sales.append(str(itemName),str(Time))