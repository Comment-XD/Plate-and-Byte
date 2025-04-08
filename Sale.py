from datetime import datetime
class Sale:
    def __inti__(self,order, time):
        self.items = order.items
        self.revenue = order.price
        self.time = time

    def getItems(self):
        return self.items

    def getRevenue(self):
        return self.revenue

    def setRevenue(self, newRevenue):
        self.revenue = newRevenue

    def setTtems(self, newItems):
        self.items = newItems
