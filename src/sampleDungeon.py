import pygame 
import argparse
from dungeon import createDungeon
from dungeon import Settings
import sys
from dungeon import manageLevels
from dungeon.manageLevels import manageLevels


def isWalkable(dungeonMap,x,y):
    if 0 <= x < dungeonMap.width and 0 <= y < dungeonMap.height:
        if dungeonMap.tiles[y][x] != 0: #0 is wall
            return True
    return False


def buildLevels(dungeonConfig, numberOfLevels, baseSeed):
    if numberOfLevels <= 1:
        DungeonGen = createDungeon(dungeonConfig)
        DungeonGen.buildDungeon()
        DungeonGen.chooseStairsInRooms()
        DungeonMap = DungeonGen.rasterizeDungeon
        return {"type":"single", "maps":[DungeonMap], "generators":[DungeonGen], "ID" : 0}
    else:
        levels = manageLevels(dungeonConfig, numberOfLevels, baseSeed)
        levels.buildAllLevels()
        return {"type":"multiple", "level":"levels"}

def findSpawn(gen, dungeonMap):
    if gen.stairsUp is not None:
        return gen.stairsUp
    else:
        y = 0
        while y < dungeonMap.height:
            x = 0
            while x < dungeonMap.width:
                if dungeonMap[y][x] != 0: ##wall***
                    return [x,y]
                else:
                    x += 1
            y += 1
        return (0,0)

def parseArgs():
    p = argparse.ArgumentParser(description= 'roguelike NEA')
    p.add_argument('--levels', type=int, default=3, help='number of levels')
    p.add_argument('--seed', type=int, default=None, help='base seed(none = random) each run')
    p.add_argument('--width', type=int, default=120, help='base map width')
    p.add_argument('--height', type=int, default=120, help='base map height')
    p.add_argument('--tile', type=int, default=10, help='tile size (px)')
    p.add_argument('--bias', type=float, default=0.6, help='split bias where region is a square') #used to randomly decide the room orientation
    return p.parse_args()

def main():
    #configuring the dungeon
    args = parseArgs()
    dungeonConfig = Settings(width=120, height=72, minRegionWidth=18, minRegionHeight=15, minRoomWidth=6, minRoomHeight=5, corridorWidth=1, roomMargin=2, splitBias=args.bias, seed=None)
    NUMBEROFLEVELS = args.levels
    BASESEED = args.seed
    TILE = args.tile
    PLAYER = (255,67,4) #player color

    #build floors
    bundle = buildLevels(dungeonConfig, NUMBEROFLEVELS, BASESEED)
    #pygame setup
    pygame.init()
    screen = pygame.display.set_mode((dungeonConfig.width * TILE, dungeonConfig.height * TILE))
    pygame.display.set_caption('Dungeon Game')
    clock = pygame.time.Clock()
    pygame.display.update()
    running = True 

    #get current map
    if bundle['type'] == 'single':
        currentMap = bundle['maps'][0]
        currentGen = bundle['generators'][0]
    else:
        levels = bundle['levels']
        currentMap = levels.getCurrentMap()
        currentGen = levels.getCurrentGenerator() 
    
    #get spawn
    px,py = findSpawn(currentGen, currentMap)

    
    while running:
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                running = False
            elif event.py == pygame.KEYDOWN:
                nx, ny = px, py
                if event.key == pygame.K_UP:
                    ny = ny + 1  
                elif event.key == pygame.K_DOWN:
                    ny = ny - 1
                elif event.key == pygame.K_LEFT:
                    nx = nx - 1
                elif event.key == pygame.K_RIGHT:
                    nx = nx + 1

                if (nx, ny) != (px,py) and isWalkable[nx, ny]:
                    px,py = nx,ny
                    tile = currentMap.tiles[py][px]
                    if bundle['type'] == 'multi':
                        if tile == 3:
                            levels.getPrevLevel() 
                            currentMap = levels.getCurrentMap()
                            currentGen = levels.getCurrentGen()
                            if currentGen.stairDown is not None:
                                px,py = currentGen.stairDown
                            else:
                                px,py = findSpawn(currentGen, currentMap)
                        elif tile == 4:
                            levels.getNextLevel()
                            currentMap = levels.getCurrentMap()
                            currentGen = levels.getCurrentGen()
                            if currentGen.stairUp is not None:
                                px,py = currentGen.stairUp
                            else:
                                px,py = findSpawn(currentGen, currentMap)
                    
                    #level switching
                    if event.key == pygame.K_r:
                        bundle = buildLevels(dungeonConfig, NUMBEROFLEVELS, BASESEED)
                        if bundle['type'] == 'single':
                            currentMap = bundle['DungeonMap'][0]
                            currentGen = bundle['DungeonGen'][0]
                        else:
                            levels = bundle['levels']
                            currentMap = levels.getCurrentMap()
                            currentGen = levels.getCurrentGen()
                        px,py = findSpawn(currentGen, currentMap)
                    elif event.key == pygame.K_RIGHTBRACKET:
                        if bundle['type'] == 'multi':
                            levels.nextLevel()
                            currentMap = levels.getCurrentMap()
                            currentGen = levels.getCurrentGen()
                            px,py = findSpawn(currentGen, currentMap)
                    elif event.key == pygame.K_LEFTBRACKET:
                        if bundle['type'] == 'multi':
                            levels.nextLevel()
                            currentMap = levels.getCurrentMap()
                            currentGen = levels.getCurrentGen()
                            px,py = findSpawn(currentGen, currentMap)
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        NUMBEROFLEVELS += 1
                        bundle = buildLevels(dungeonConfig, NUMBEROFLEVELS, BASESEED)
                        if bundle['type'] == 'single':
                            currentMap = bundle['DungeonMap'][0]
                            currentGen = bundle['DungeonGen'][0]
                        else:
                            levels = bundle['levels']
                            currentMap = levels.getCurrentMap()
                            currentGen = levels.getCurrentGen()
                        px,py = findSpawn(currentGen, currentMap)
                    elif event.key == pygame.K_MINUS:
                        if NUMBEROFLEVELS > 1:
                            NUMBEROFLEVELS -= 1
                            bundle = buildLevels(dungeonConfig, NUMBEROFLEVELS, BASESEED)
                        if bundle['type'] == 'single':
                            currentMap = bundle['DungeonMap'][0]
                            currentGen = bundle['DungeonGen'][0]
                        else:
                            levels = bundle['levels']
                            currentMap = levels.getCurrentMap()
                            currentGen = levels.getCurrentGen()
                        px,py = findSpawn(currentGen, currentMap)

        #draw screen
        screen.fill((0,0,0))
        if bundle['type'] == 'single':
            currentMap = bundle['DungeonMap'][0]
            currentGen = bundle['DungeonGen'][0]
        else:
            currentMap = levels.getCurrentMap()
            currentGen = levels.getCurrentGen()
        currentMap.drawDungeon(screen, tileSize = TILE)

        #draw player
        pygame.draw.rect(screen, (255,40,120), pygame.rect(px*TILE, py*TILE, TILE, TILE))

        pygame.display.update()
        clock.tick(60)
    pygame.quit()




#calls the main method when the project is run
if __name__ == '__main__':
    main()
    


