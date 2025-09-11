import pygame
import random
from .settings import Settings
from .corridor import Corridoor
from .dungeonmap import DungeonMap
from .region import Region, splitUntilCannot
from .room import Room

class createDungeon:
    def __init__(self, dungeonConfig):
        if dungeonConfig.seed is not None:
            random.seed(dungeonConfig.seed)
        self.dungeonConfig = dungeonConfig
        self.root = Region(pygame.Rect(0,0,dungeonConfig.width, dungeonConfig.height))
        self.leaves = []
        self.rooms = []
        self.corridors = []



    def buildDungeon(self):
        self.leaves = splitUntilCannot(self.dungeonConfig, self.root) #binary split
        self._make_rooms() #creating rooms
        self._connectRooms()
        return self._rasterizeDungeon()


    

    def _make_rooms(self):
        i = 0
        while i < len(self.leaves):
            leaf = self.leaves[i]
            r = leaf.rect
            maxWidth = r.width - 2*self.dungeonConfig.roomMargin
            maxheight = r.height - 2*self.dungeonConfig.roomMargin
            if maxWidth >= self.dungeonConfig.minRoomWidth and maxheight >= self.dungeonConfig.minRoomHeight:
                roomWidth = random.randint(self.dungeonConfig.minRoomWidth, maxWidth)
                roomHeight = random.randint(self.dungeonConfig.minRoomHeight, maxheight)
                left = random.randint(r.left + self.dungeonConfig.roomMargin, r.right - self.dungeonConfig.roomMargin - roomWidth)
                top = random.randint(r.top + self.dungeonConfig.roomMargin, r.bottom - self.dungeonConfig.roomMargin - roomHeight)
                leaf.room = Room(pygame.Rect(left, top, roomWidth, roomWidth))
                self.rooms.append(leaf.room)
            i += 1

    
    def _closestPair(self, leftList, rightList): 
        #pick two rooms, one from each list with the smallest manhattahn distance between them
        bestDistance = 10^9
        bestPair = None
        i = 0
        while i < len(leftList):
            a = leftList[i]
            j = 0
            while j < len(rightList):
                b = rightList[j]
                distance = abs(a.center()[0] - b.center()[0]) + abs(a.center()[1] - a.center()[1])
                if distance <  bestDistance:
                    bestdistance = distance
                    bestPair = (a,b)
                j = j + 1
            i = i + 1
        return bestPair

        
    def _connectRooms(self, roomA, roomB):
        #choose points on eacch room edge facing another room and then build a path connecting them  
        roomADoors = roomA.boundaryPointsFacing(roomB.center())
        roomBDoors = roomB.boundaryPointsFacing(roomA.center())
        if len(roomADoors) == 0 or len(roomBDoors) == 0: 
            a = roomA.center()
            b = roomB.center()
            return[a,b]
    
    def _rasterizeDungeon(self):
        DMap = DungeonMap(self.dungeonConfig.width, self.dungeonConfig.height)
        #carve rooms
        i = 0
        while i < len(self.rooms):
            DMap.drawRect(self.rooms[i].rect)
            i = i + 1 #going through each room and drawing a rectangle

        j = 0
        while j < self.corridors:
            x = self.corridors[j]
            k = 0
            while k < len(x.path) - 1:
                DMap.drawLine(x.path[j], x.path[j+1], self.dungeonConfig.corridorWidth)
                k = k + 1
            j = j + 1
        return DMap
                          
        





