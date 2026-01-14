class manageLevels:
    def __init__(self, dungeonConfig, numberOfLevels, baseSeed):
        self.dungeonConfig = dungeonConfig
        self.numberOfLevels = numberOfLevels
        self.baseSeed = baseSeed
        self.levels = []
        self.current = 0
        self.generators = []

    def getCurrentMap(self):
        return self.levels[self.current] #returns a map for each level
    
    def getCurrentGenerator(self):
        return self.generators[self.current] #generates a dungeon for each level
    
    def getNextLevel(self):
        if self.numberOfLevels == 0:
            return 
        else:
            self.current = (self.current + 1) % (self.numberOfLevels)
            return self.current #using mod allows ensuring the level does not exceed the specified number of levels

    def getPrevLevel(self):
        if self.numberOfLevels == 0:
            return
        else:
            self.current = (self.current - 1 ) % (self.numberOfLevels)
            return self.current

    def nextLevel(self):
        if self.numberOfLevels == 0:
            return
        self.current = (self.current + 1) % self.numberOfLevels

    def prevLevel(self):
        if self.numberOfLevels == 0:
            return
        self.current = (self.current - 1) % self.numberOfLevels

    def getCurrentGen(self):
        return self.generators[self.current] 
        

    def buildAllLevels(self):
        """Build all floors; vary seed per floor if baseSeed provided."""
        from .createDungeon import createDungeon
        self.levels = []
        self.generators = []
        i = 0
        while i < self.numberOfLevels:
            if self.baseSeed is None:
                self.dungeonConfig.seed = None
            else:
                self.dungeonConfig.seed = self.baseSeed + i

            gen = createDungeon(self.dungeonConfig)
            gen.buildDungeon()
            gen.chooseStairsInRooms()
            dmap = gen._rasterizeDungeon()

            self.levels.append(dmap)
            self.generators.append(gen)
            i += 1
        self.current = 0