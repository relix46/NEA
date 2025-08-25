import pygame
from dungeon import Settings
class Region:
    #represents a BSP node which may split into 2 child nodes
    def __init__(self, rect, depth=0):
        self.rect = rect
        self.left = None
        self.right = None
        self.room = None
        self.depth = depth
        #create a rectangle
    
        
    def isLeaf(self):
        #checks that this region has no children
        if (self.left is None and self.right is None):
            return True
        else:
            return False
        
    def getLeaves(self):
        #returns a list of all leaves in the subtree
        if self.isLeaf():
            return [self]
        leaves = []
        if self.left is not None:
            leftLeaves = self.left.getLeaves()
            counter = 0
            while counter < len(leftLeaves):
                leaves.append(leftLeaves[counter])
                counter += 1
        if self.right is not None:
            rightLeaves = self.right.getLeaves()
            counter = 0
            while counter < len(rightLeaves):
                leaves.append(rightLeaves[counter])
                counter +=1 
        return leaves



    def split(self):
        #split region vertically or horizontally (add parameters)
        pass

    def createRoom(self):
        pass