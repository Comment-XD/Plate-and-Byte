from datetime import date
from idlelib.mainmenu import menudefs

from src.Sale import Sale
from src.Menu import Menu

class Data:
    def __init__(self):
        self.sales = [] #List of all past sales
        self.menu = Menu()
        self.d = date()

    def addSale(self,order):
        self.sales.append(Sale(order, self.d.ctime()))

    def getMenu(self):
        return self.menu

    def getSales(self):
        return self.sales
