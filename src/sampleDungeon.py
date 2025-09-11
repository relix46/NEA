import pygame 
import argparse
from dungeon import DungeonMap
from dungeon import Settings
import sys


def isWalkable(dungeonMap,x,y):
    if 0 <= x < dungeonMap.width and 0 <= y < dungeonMap.height:
        if dungeonMap.tiles[y][x] != 0: #0 is wall
            return True
    return False




def main():
    #configuring the dungeon
    args = parseArgs()
    dungeonConfig = Settings(width=120, height=72, minRegionWidth=18, minRegionHeight=15, minRoomWidth=6, minRoomHeight=5, corridorWidth=1, roomMargin=2, corridorWidth=1, splitBias=args.bias, seed=None)
  
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


