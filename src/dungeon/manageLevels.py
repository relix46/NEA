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
        

    def getCurrentGen(self):
        return self.generators[self.current]


    def buildAllLevels(self):
        #build all floors, very seed per floor if baseSeed is provided
        from .createDungeon import createDungeon
        self.levels = []
        self.generators = []
        i = 0
        while i < self.numberOfLevels:
            if self.baseSeed is not None:
                self.dungeonConfig.seed = self.baseSeed + i

            gen = createDungeon(self.dungeonConfig)
            gen.buildDungeon()
            gen.chooseStairsInRooms()
            dungeonMap = gen._rasterizeDungeon()
            self.levels.append(dungeonMap)
            self.generators.append(gen)
            i += 1
        self.current = 0