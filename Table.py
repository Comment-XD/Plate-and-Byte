from Order import Order

class Table:
    def __init__(self,Data):
        self.status = "Available"
        self.orders = []
        self.data = Data
        self.menu = Data.menu
    def addOrder(self,items): #input a list of strings (item names)
        try:
            temp = []
            tempPrice = 0
            for item in items:
                temp.append(self.menu.getItem(item))
                tempPrice += self.menu.getItem(item)[1]
            self.orders.append(Order(temp,tempPrice))
        except Exception:
            print("---Something went wrong---")

    def changeStatus(self, status):
        self.status = status

    def getOrders(self):
        return self.orders

    def serveOrder(self, order):
        if order in self.orders:
            self.data.addSale(order)
            self.orders.remove(order)

    def serveAllOrders(self):
        for order in self.orders:
            self.data.addSale(order)
        self.orders = []





