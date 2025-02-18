from datetime import datetime
import Menu

class Data:
    def __init__(self, customer_path):
        self.sales = [] #List of all past sales, Tuple Format (Item, Time)
        self.menu = Menu()

    def AddSale(self,itemName,Time = datetime.now()):
        if str(itemName) not in self.sales:
            self.sales.append(str(itemName),str(Time))