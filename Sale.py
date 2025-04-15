from datetime import datetime

"""Sale CLass - Stores all data used in a completed order"""
class Sale:
    def __inti__(self,order, time):
        self.items = order.items
        self.revenue = order.price
        self.time = time

    # Returns "items" list
    def getItems(self):
        return self.items

    # Returns "revenue" variable
    def getRevenue(self):
        return self.revenue

    # Sets "items" list
    def setRevenue(self, newRevenue):
        self.revenue = newRevenue

    # Sets "revenue" variable
    def setTtems(self, newItems):
        self.items = newItems
