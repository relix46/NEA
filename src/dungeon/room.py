class Room:
    def __init__(self, rect):
        self.rect = rect
        

    def getCenter(self):
        return (self.rect.centerx, self.rect.centery)


    def fitRoom(self):
        #create room and fit it inside region
        pass
    
    def boundaryPointsFacing(self, target):
        #check sorting of coords~~~~~~~~~~~~~~~
        #return a list of points on one edge of the room closer towards the target
        #these points will be used to place the corridors
        result = []
        tx, ty = target #assigning x and y coords for target
        cx, cy = self.getCenter() 
        dx = tx - cx
        dy = ty- cy
        if abs(dx) >= abs(dy):
            horizontal = True
        else:
            horizontal = False
        
        #choosing vertical edge that faces the target
        if horizontal == True:
            if dx >= 0:
                xEdge = self.rect.right - 1
            else:
                xEdge = self.rect.left
            ycoords = [] 
            y = self.rect.top
            while y < self.rect.bottom:
                ycoords.append(y)
                y = y + 1
                #goes through each coordinate and adds it to the list
            i = 0
            while i < len(ycoords):
                result.append((xEdge,ycoords[i]))
                i = i + 1
        else:
            if dy >= 0:
                yEdge = self.rect.bottom - 1
            else:
                yEdge = self.rect.top
            xcoords = []
            x = self.rect.left
            while x < self.rect.right:
                xcoords.append(x)
                x = x + 1
            i = 0
            while i < len(xcoords):
                result.append((xcoords[i], yEdge))
                i = i + 1
        return result



        


        