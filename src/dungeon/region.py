import pygame
import random
from.settings import Settings

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



    def split(self, dungeonConfig):
        #split region vertically or horizontally (add parameters)
        if dungeonConfig.seed is not None:
            random.seed(dungeonConfig.seed + self.depth)
        if self.rect.width >= 2*dungeonConfig.minRegionWidth:
            canSplitV = True
        else:
            canSplitV = False
        if self.rect.height >= 2*dungeonConfig.minRegionHeight:
            canSplitH = True
        else:
            canSplitH = False

        if canSplitV == False and canSplitH == False:
            return False #too small to split
        
        ratio = self.rect.width / max(1, self.rect.height)

        if canSplitV == True and canSplitH == False:
            vertical = True #vertical split
        elif canSplitV == False and canSplitH == True:
            vertical = False #horizontal split
        else:
            if ratio > 1.1:
                vertical = True #wide enough
            elif ratio < 0.9:
                vertical = False #tall enough
            else:
                if random.random() < dungeonConfig.splitBias:
                    vertical = True
                else:
                    vertical = False
        #perform the split
        if vertical == True:
            minxcoord = self.rect.left + dungeonConfig.minRegionWidth
            maxxcoord = self.rect.right - dungeonConfig.minRegionWidth
            if maxxcoord <=  minxcoord:
                return False
        
            temp = random.randint(minxcoord, maxxcoord)
            leftRect = pygame.Rect(self.rect.left, self.rect.top, temp - self.rect.left, self.rect.height)
            rightRect = pygame.Rect(temp, self.rect.top, self.rect.right - temp, self.rect.height)
            self.left = Region(leftRect, self.depth + 1)
            self.right = Region(rightRect, self.depth + 1)
        else:
            minycoord = self.rect.top + dungeonConfig.minRegionHeight
            maxycoord = self.rect.bottom - dungeonConfig.minRegionHeight
            if maxycoord <=  minycoord:
                return False
        
            temp = random.randint(minycoord, maxycoord)
            topRect = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, temp - self.rect.top)
            bottomRect = pygame.Rect(self.rect.left, temp, self.rect.width, self.rect.bottom - temp)
            self.left = Region(topRect, self.depth + 1)
            self.right = Region(bottomRect, self.depth + 1)
        return True




def splitUntilCannot(root, dungeonConfig): #try splitting else marks it as a leaf
    leaves = []
    stack = [root]
    while len(stack) > 0:
        node = stack.pop()
        if node.split(dungeonConfig) == True:
            stack.append(node.left)
            stack.append(node.right)
        else:
            leaves.append(node)
    return leaves