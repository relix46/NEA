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
        self.stairsUp = None
        self.stairsDown = None



    def buildDungeon(self):
        self.leaves = splitUntilCannot(self.root, self.dungeonConfig) #binary split
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
                leaf.room = Room(pygame.Rect(left, top, roomWidth, roomHeight))
                self.rooms.append(leaf.room)
            i += 1

    
    def _closestPair(self, leftList, rightList): 
        #pick two rooms, one from each list with the smallest manhattahn distance between them
        bestDistance = 10**9
        bestPair = None
        i = 0
        while i < len(leftList):
            a = leftList[i]
            j = 0
            while j < len(rightList):
                b = rightList[j]
                distance = abs(a.getCenter()[0] - b.getCenter()[0]) + abs(a.getCenter()[1] - b.getCenter()[1])
                if distance <  bestDistance:
                    bestDistance = distance
                    bestPair = (a,b)
                j = j + 1
            i = i + 1
        return bestPair

        
    def _connectRooms(self):
        """
        Traverse the BSP; at each internal node connect
        one room from left subtree to one from right subtree
        with a simple L-shaped corridor joining edge points.
        """
        def collect(node):
            if node is None:
                return []
            if node.isLeaf():
                if node.room is not None:
                    return [node.room]
                else:
                    return []

            left_rooms  = collect(node.left)
            right_rooms = collect(node.right)

            if len(left_rooms) > 0 and len(right_rooms) > 0:
                a, b = self._closestPair(left_rooms, right_rooms)
                path = self._route_doors_l(a, b)
                self.corridors.append(Corridoor(path, width=self.dungeonConfig.corridorWidth))

            merged = []
            i = 0
            while i < len(left_rooms):
                merged.append(left_rooms[i]); i += 1
            j = 0
            while j < len(right_rooms):
                merged.append(right_rooms[j]); j += 1
            return merged

        collect(self.root)

    def _route_doors_l(self, room_a, room_b):
        """
        Choose 'door' points on each room edge facing the other room, then
        build a simple L-shaped path: A -> bend -> B.
        """
        a_doors = room_a.boundaryPointsFacing(room_b.getCenter())
        b_doors = room_b.boundaryPointsFacing(room_a.getCenter())

        if len(a_doors) == 0 or len(b_doors) == 0:
            a = room_a.getCenter()
            b = room_b.getCenter()
            return [a, (b[0], a[1]), b]

        a = a_doors[0]
        b = b_doors[0]

        # Two equivalent L options; either is fine
        return [a, (b[0], a[1]), b]
    
    def _rasterizeDungeon(self):
        DMap = DungeonMap(self.dungeonConfig.width, self.dungeonConfig.height)
        #carve rooms
        i = 0
        while i < len(self.rooms):
            DMap.drawRect(self.rooms[i].rect)
            i = i + 1 #going through each room and drawing a rectangle

        j = 0
        while j < len(self.corridors):
            x = self.corridors[j]
            k = 0
            while k < len(x.path) - 1:
                DMap.drawLine(x.path[k], x.path[k+1], self.dungeonConfig.corridorWidth)
                k = k + 1
            j = j + 1
        if self.stairsUp is not None:
            DMap.markTile(self.stairsUp[0], self.stairsUp[1], 3)
        if self.stairsDown is not None:
            DMap.markTile(self.stairsDown[0], self.stairsDown[1], 4)
        
        return DMap
                          

    def chooseStairsInRooms(self): #picks a random room for up and another for down
        if len(self.rooms) == 0:
            self.stairsUp = None
            self.stairsDown = None
            return None, None
        else:
            upRoom = random.choice(self.rooms)
            if len(self.rooms) >= 2:
                downRoom = random.choice(self.rooms)
                counter = 0
                while downRoom is upRoom and counter < 10:
                    downRoom = random.choice(self.rooms)
                    counter = counter + 1
            else:
                downRoom = upRoom

            mapCenterX = self.dungeonConfig.width // 2
            mapCenterY = self.dungeonConfig.height // 2
            upEdge = upRoom.boundaryPointsFacing((mapCenterX, mapCenterY))
            downEdge = downRoom.boundaryPointsFacing((mapCenterX, mapCenterY))
            if len(upEdge) > 0:
                self.stairsUp = upEdge[0]
            else:
                self.stairsUp = upRoom.getCenter()
            if len(downEdge) > 0:
                self.stairsDown = downEdge[0]
            else:
                self.stairsDown = downRoom.getCenter()
            return self.stairsUp, self.stairsDown
            


    



        





