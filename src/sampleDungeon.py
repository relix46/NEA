import pygame
import argparse
import sys
from dungeon.createDungeon import createDungeon
from dungeon.settings import Settings
from dungeon.manageLevels import manageLevels
import random
from collections import deque

#Dijkstra / BFS
def isWalkable(grid, x, y):
    if 0 <= x < grid.width and 0 <= y < grid.height:
        return grid.tiles[y][x] != 0
    return False

def findPath(grid, start, goal):
    sx, sy = start
    gx, gy = goal

    if not isWalkable(grid, sx, sy) or not isWalkable(grid, gx, gy):
        return None

    queue = deque()
    visited = {}
    visited[(sx, sy)] = None
    queue.append((sx, sy))

    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    while queue:
        x, y = queue.popleft()
        if (x, y) == (gx, gy):
            break
        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if isWalkable(grid, nx, ny) and (nx, ny) not in visited:
                visited[(nx, ny)] = (x, y)
                queue.append((nx, ny))

    if (gx, gy) not in visited:
        return None

    #Reconstruct path
    path = []
    node = (gx, gy)
    while node:
        path.append(node)
        node = visited[node]
    path.reverse()
    return path

#Manages enemies
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 0
        self.path = None

    def update(self, grid, player_pos):
        self.timer += 1
        if self.timer >= 25:  #speed
            self.timer = 0
            self.path = findPath(grid, (self.x, self.y), player_pos)
            if self.path and len(self.path) > 1:
                self.x, self.y = self.path[1]

    def draw(self, surface, camX, camY, tileSize):
        rect = pygame.Rect(self.x*tileSize - camX, self.y*tileSize - camY, tileSize, tileSize)
        pygame.draw.rect(surface, (50, 50, 255), rect)

class EnemyManager:
    def __init__(self, grid, num_enemies=3):
        self.enemies = []
        w, h = grid.width, grid.height
        while len(self.enemies) < num_enemies:
            x = random.randint(0, w-1)
            y = random.randint(0, h-1)
            if isWalkable(grid, x, y):
                self.enemies.append(Enemy(x, y))

    def update(self, player_pos, grid):  #grid parameters
        for e in self.enemies:
            e.update(grid, player_pos)

    def draw(self, surface, camX, camY, tileSize):
        for e in self.enemies:
            e.draw(surface, camX, camY, tileSize)

def parseArgs():
    p = argparse.ArgumentParser(description='NEA Dungeon Game')
    p.add_argument('--levels', type=int, default=3)
    p.add_argument('--seed', type=int, default=None)
    p.add_argument('--tile', type=int, default=16)
    return p.parse_args()

def buildLevels(dungeonConfig, numberOfLevels, baseSeed):
    if numberOfLevels <= 1:
        DungeonGen = createDungeon(dungeonConfig)
        DungeonGen.buildDungeon()
        DungeonGen.chooseStairsInRooms()
        DungeonMap = DungeonGen._rasterizeDungeon()
        return {"type": "single", "maps": [DungeonMap], "generators": [DungeonGen]}
    else:
        levels = manageLevels(dungeonConfig, numberOfLevels, baseSeed)
        levels.buildAllLevels()
        return {"type": "multiple", "levels": levels}

def findSpawn(gen, dungeonMap):
    if gen.stairsUp:
        return gen.stairsUp
    for y in range(dungeonMap.height):
        for x in range(dungeonMap.width):
            if dungeonMap.tiles[y][x] != 0:
                return (x, y)
    return (0, 0)


def main():
    args = parseArgs()

    dungeonConfig = Settings(
        width=120,
        height=72,
        minRegionWidth=18,
        minRegionHeight=15,
        minRoomWidth=6,
        minRoomHeight=5,
        corridorWidth=1,
        roomMargin=2,
        splitBias=0.6,
        seed=args.seed
    )

    TILE = args.tile
    NUMBEROFLEVELS = args.levels
    BASESEED = args.seed

    pygame.init()
    SCREEN_W, SCREEN_H = 1280, 720
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Dungeon Game")
    clock = pygame.time.Clock()

    bundle = buildLevels(dungeonConfig, NUMBEROFLEVELS, BASESEED)
    if bundle["type"] == "single":
        currentMap = bundle["maps"][0]
        currentGen = bundle["generators"][0]
    else:
        levels = bundle["levels"]
        currentMap = levels.getCurrentMap()
        currentGen = levels.getCurrentGen()

    px, py = findSpawn(currentGen, currentMap)
    enemies = EnemyManager(currentMap, num_enemies=3)

    worldSurface = pygame.Surface((currentMap.width*TILE, currentMap.height*TILE))
    moveDelay = 60
    lastMove = 0

    running = True
    while running:
        dt = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        moved = False
        nx, ny = px, py

        if dt - lastMove > moveDelay:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                ny -= 1
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                ny += 1
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                nx -= 1
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                nx += 1

            if (nx, ny) != (px, py) and isWalkable(currentMap, nx, ny):
                px, py = nx, ny
                lastMove = dt
                moved = True

        #stairs
        if moved and bundle["type"] == "multiple":
            tile = currentMap.tiles[py][px]
            if tile == 3:  # stairs up
                levels.prevLevel()
                currentMap = levels.getCurrentMap()
                currentGen = levels.getCurrentGen()
                px, py = findSpawn(currentGen, currentMap)
                enemies = EnemyManager(currentMap, num_enemies=3)
            elif tile == 4:  # stairs down
                levels.nextLevel()
                currentMap = levels.getCurrentMap()
                currentGen = levels.getCurrentGen()
                px, py = findSpawn(currentGen, currentMap)
                enemies = EnemyManager(currentMap, num_enemies=3)

        #update enemy pos
        enemies.update((px, py), currentMap)

        #check for player collision
        for e in enemies.enemies:
            if e.x == px and e.y == py:
                pygame.quit()
                sys.exit()

        #draw world
        worldSurface.fill((0, 0, 0))
        currentMap.drawDungeon(worldSurface, tileSize=TILE)

        #draw player
        pygame.draw.rect(worldSurface, (255, 40, 120), pygame.Rect(px*TILE, py*TILE, TILE, TILE))
        #draw enemies
        enemies.draw(worldSurface, 0, 0, TILE)

        #'camera'
        camX = px*TILE - SCREEN_W//2
        camY = py*TILE - SCREEN_H//2
        camX = max(0, min(camX, worldSurface.get_width()-SCREEN_W))
        camY = max(0, min(camY, worldSurface.get_height()-SCREEN_H))
        screen.blit(worldSurface, (-camX, -camY))

        #minimap
        miniScale = 0.15
        miniMap = pygame.transform.scale(worldSurface, (int(worldSurface.get_width()*miniScale), int(worldSurface.get_height()*miniScale)))
        miniX = SCREEN_W - miniMap.get_width() - 10
        miniY = 10
        screen.blit(miniMap, (miniX, miniY))
        pygame.draw.circle(screen, (255,0,0), (miniX + int(px*TILE*miniScale), miniY + int(py*TILE*miniScale)), 3)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()