from Order import Order

"""Table Class - Stores all data related to a table, such as Orders and Status"""
class Table:
    def __init__(self,Data):
        self.status = "Available"
        self.orders = []
        self.data = Data
        self.menu = Data.menu

    # input a list of strings to "order" objects and stores in "objects" list
    def addOrder(self,items):
        try:
            temp = []
            tempPrice = 0
            for item in items:
                temp.append(self.menu.getItem(item))
                tempPrice += self.menu.getItem(item)[1]
            self.orders.append(Order(temp,tempPrice))
        except Exception:
            print("---Something went wrong---")

    # Changes "status" variable
    def changeStatus(self, status):
        self.status = status

    # Returns "orders" list
    def getOrders(self):
        return self.orders

    # Converts an order to a sale
    def serveOrder(self, order):
        if order in self.orders:
            self.data.addSale(order)
            self.orders.remove(order)

    # Converse all the table's orders to sales
    def serveAllOrders(self):
        for order in self.orders:
            self.data.addSale(order)
        self.orders = []





