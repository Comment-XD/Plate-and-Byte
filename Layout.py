from Table import Table


class Layout:
    def __init__(self,sizeX,sizeY,Parent):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.map = []
        for i in range(self.sizeY):
            temp = [None]*self.sizeX
            self.map.append(temp)



    """
    Creates a table in the map 2d list
    
    startTile (x, y) - table position
    endTile (x, y) - used for tables which take up more than one tile. Must share an x or y position.
    """
    def AddTable(self,startTile,endTile = None):
        temp = Table()
        try:
            x = startTile[0]
            y = startTile[1]
            if endTile == None or startTile == endTile:
                self.map[x][y] = temp
                return True
            x2 = endTile[0]
            y2 = endTile[1]
            if x==x2:
                if y<y2:
                    for i in range(y,y2+1,1):
                        self.map[x][i] = temp
                else:
                    for i in range(y2, y + 1, 1):
                        self.map[x][i] = temp
                return True
            elif y==y2:
                if x<x2:
                    for i in range(x,x2+1,1):
                        self.map[i][y] = temp
                else:
                    for i in range(x2, x + 1, 1):
                        self.map[i][y] = temp
                return True
            else:
                print("startTile and endTile must share an x or y coordinate")

        except Exception:
            print("Something when wrong. Please enter inputs in tuple format (x, y).")
            return False



    """
    Takes an x and y coordinates and returns the value in the position in the map array
    """
    def getMapPosition(self,x,y):
        return self.map[x][y]
