from datetime import date
from idlelib.mainmenu import menudefs

from src.Sale import Sale
from src.Menu import Menu


"""Data Class - Stores and manages Sales and Menu"""
class Data:
    def __init__(self):
        self.sales = []
        self.menu = Menu()
        self.d = date()

    # Adds a new object of Sale to "sales" list
    def addSale(self,order):
        self.sales.append(Sale(order, self.d.ctime()))

    # Returns menu
    def getMenu(self):
        return self.menu

    # Returns "Sales" List
    def getSales(self):
        return self.sales
