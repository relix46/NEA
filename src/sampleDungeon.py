import pygame 
import argparse
from dungeon import createDungeon
from dungeon import Settings
import sys
from dungeon import manageLevels    


def isWalkable(dungeonMap,x,y):
    if 0 <= x < dungeonMap.width and 0 <= y < dungeonMap.height:
        if dungeonMap.tiles[y][x] != 0: #0 is wall
            return True
    return False


def buildLevels(dungeonConfig, numberOfLevels, baseSeed):
    if numberOfLevels <= 1:
        gen = createDungeon(dungeonConfig)
        gen.buildDungeon()
        gen.chooseStairsInRooms()
        DungeonMap = gen.rasterizeDungeon
        return {"type":"single", "maps":[DungeonMap], "generators":[gen], "ID" : 0}
    else:
        levels = manageLevels[dungeonConfig, numberOfLevels, baseSeed]
        levels.buildAllLevels()
        return {"type":"multiple", "level":levels}



def main():
    #configuring the dungeon
    args = parseArgs()
    dungeonConfig = Settings(width=120, height=72, minRegionWidth=18, minRegionHeight=15, minRoomWidth=6, minRoomHeight=5, corridorWidth=1, roomMargin=2, corridorWidth=1, splitBias=args.bias, seed=None)
    NUMBEROFLEVELS = args.levels
    BASESEED = args.seed
    TILE = args.tile
    PLAYER = (255,67,4)
   #pygame setup
    pygame.init()
    screen = pygame.display.set_mode((dungeonConfig.width * TILE, dungeonConfig.height * TILE))
    pygame.display.set_caption('Dungeon Game')
    clock = pygame.time.Clock()
    pygame.display.update()
    running = True 
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
                
                sys.exit()

        screen.fill('black')
        pygame.display.update()


def parseArgs():
    p = argparse.ArgumentPasser(desc = 'roguelike NEA')
    p.addArgument('--levels', type=int, default=3, help='number of levels')
    p.addArguement('--seed', type=int, default=None, help='base seed(none = random) each run')
    p.addArguement('--width', type=int, default=120, help='base map width')
    p.addArguement('--height', type=int, default=120, help='base map height')
    p.addArguement('--tile', type=int, default=10, help='tile size (px)')
    p.addArguement('--bias', type=float, default=0.6, help='split bias where region is a square') #used to randomly decide the room orientation
    return p.parseArgs()

#calls the main method when the project is run
if __name__ == '__main__':
    main()
    pass


