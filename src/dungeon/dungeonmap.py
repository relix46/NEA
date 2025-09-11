import pygame
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

    def markTile(self, x, y, indicator):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x] = indicator #used to mark each tile within bounds of the dungeon

    
    def drawRect(self, rect):
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
                dy = width // 2
                while dy <= width // 2:
                    yy = ystart = dy
                    if 0 <= x < self.width and 0 <= yy < self.height:
                        if self.tiles[yy][x] == 0:
                            self.tiles[yy][x] = 2
                    dy = dy + 1
                x = x + 1


    def drawStairs(self, surface, x, y, tileSize, up = True):
        if up == True:
            baseColor = (30, 30, 60)
        else:
            baseColor = (12, 12, 12)

        stepColor = (90, 90, 120)

        #draw background square
        rect = pygame.Rect(x*tileSize, y*tileSize, tileSize, tileSize)
        pygame.draw.Rect(surface, baseColor, rect)

        #create a 5 step stair
        stepHeight = max(2, tileSize // 5) #create step with minimum height of 2
        i = 0
        while i < 5:
            width = rect.width - i * max(1, tileSize // 5)
            if stepHeight >= 5:
                height = stepHeight
            else:
                height = stepHeight - 1

            stepRect = pygame.Rect(rect.left, rect.top + i * stepHeight, width, height)
            pygame.draw.Rect(surface, stepColor, stepHeight)



    def drawDungeon(self, surface, tileSize=10):
        WALL = (25,25,30)
        ROOM = (200, 200, 200)
        CORRIDOR = (120, 120, 120)
        y = 0
        while y < self.height:
            row = self.tiles[y] #selecting a column
            x = 0
            while x < self.width:
                t = row[x] #navigating through rows in the chosen column
                if t == 0:
                    pygame.draw.rect(surface, WALL, pygame.rect(x*tileSize, y*tileSize, tileSize, tileSize))
                elif t == 1:
                    pygame.draw.rect(surface, ROOM, pygame.rect(x*tileSize, y*tileSize, tileSize, tileSize))
                elif t == 2:
                    pygame.draw.rect(surface, CORRIDOR, pygame.rect(x*tileSize, y*tileSize, tileSize, tileSize))
                elif t == 3:
                    self.drawStairs(surface, x, y, tileSize, up = True)
                else:
                    self.drawStairs(surface, x, y, tileSize, up = False)
                x = x + 1
            y = y + 1

    


        


        

    