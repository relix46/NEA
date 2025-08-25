import pygame 
from dungeon import DungeonMap
from dungeon import Settings
import sys


def main():
    #configuring the dungeon
    dungeonConfig = Settings(width=120, height=72, minRegionWidth=18, minRegionHeight=15, minRoomWidth=6, minRoomHeight=5, corridorWidth=1, roomMargin=2)
    pygame.init()
    screen = pygame.display.set_mode((dungeonConfig.width * 10, dungeonConfig.height * 10))
    pygame.display.set_caption('Dungeon Game')
    clock = pygame.time.Clock()
    pygame.display.update()
    running = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('black')
        pygame.display.update()
    

#calls the main method when the project is run
if __name__ == '__main__':
    main()
    pass
