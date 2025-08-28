class DungeonMap:
    #dungeonmap is a 2D tilemap grid using the following key for tiling: 
    #0 = wall, 1 = room, 2 = corridoor
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = []
        ycoord = 0
        while ycoord <  height:
            row = []
            xcoord = 0
            while xcoord < width:
                row.append(0)
                xcoord = xcoord + 1
            self.tiles.append(row)
            ycoord = ycoord + 1
    
    def carveRect(self, rect):
        y = rect.top
        while y < rect.bottom:
            x = rect.left
            while x < rect.right:
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.tiles[y][x] = 1 #room
                x = x + 1
            y = y + 1
    
    def drawLine(self, start, end, width):
        xstart, ystart = start
        xend, yend = end
        if xstart == xend:
            if ystart <= yend:
                y = ystart
                yE = yend
            else:
                y = yend
                yE = ystart
            while y <= yE:
                dx = width // 2
                while dx <= width // 2:
                    xx = xstart + dx
                    if 0 <= xx < self.width and 0 <= y < self.height:
                        if self.tiles[y][xx] == 0:
                            self.tiles[y][xx] = 2 #corridoor
                        dx = dx + 1
                y = y + 1
        elif (ystart == yend):
            if xstart <= xend:
                x = xstart
                xE = xend
            else:
                x = xend
                xE = xstart
            while x <= xE:
                dy = height // 2
                while dy <= height // 2:
                    yy = ystart = dy
                    if 0 <= x < self.width and 0 <= yy < self.height:
                        if self.tiles[yy][x] == 0:
                            self.tiles[yy][x] = 2
                    dy = dy + 1
                x = x + 1

            
        


        

    def createMap(self):
        pass

    def splitRegions(self):
        pass

    def createRoom(self):
        pass

    def connectRooms(self):
        pass

    