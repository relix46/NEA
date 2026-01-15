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


def show_main_menu(screen, clock):
    """
    Display the main menu and return the user's choice:
    "play" or "quit". "Load Saved Game" is a placeholder.
    """
    SCREEN_W, SCREEN_H = screen.get_size()

    # Dark, atmospheric colors
    BG_COLOR = (8, 10, 18)
    TITLE_COLOR = (210, 210, 240)
    TEXT_COLOR = (150, 155, 180)
    HIGHLIGHT_COLOR = (200, 170, 80)

    pygame.font.init()
    title_font = pygame.font.Font(None, 80)
    menu_font = pygame.font.Font(None, 48)
    info_font = pygame.font.Font(None, 28)

    options = ["Play New Game", "Load Saved Game", "Quit Game"]
    selected = 0

    message = ""
    message_time = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(options)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if selected == 0:
                        return "play"
                    elif selected == 1:
                        message = "Loading saved games is not implemented yet."
                        message_time = pygame.time.get_ticks()
                    else:
                        return "quit"

        # Drawing
        screen.fill(BG_COLOR)

        # Title
        title_surf = title_font.render("Dungeon Game", True, TITLE_COLOR)
        title_rect = title_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 3))
        screen.blit(title_surf, title_rect)

        # Menu options
        start_y = SCREEN_H // 2
        for i, text in enumerate(options):
            color = HIGHLIGHT_COLOR if i == selected else TEXT_COLOR
            surf = menu_font.render(text, True, color)
            rect = surf.get_rect(center=(SCREEN_W // 2, start_y + i * 55))
            screen.blit(surf, rect)

        # Info / placeholder message
        if message:
            now = pygame.time.get_ticks()
            if now - message_time < 2500:
                info_surf = info_font.render(message, True, TEXT_COLOR)
                info_rect = info_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H - 60))
                screen.blit(info_surf, info_rect)
            else:
                message = ""

        pygame.display.update()
        clock.tick(60)

    return "quit"


def run_game(screen, clock, dungeonConfig, TILE, NUMBEROFLEVELS, BASESEED):
    SCREEN_W, SCREEN_H = screen.get_size()
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

    choice = show_main_menu(screen, clock)
    if choice == "play":
        run_game(screen, clock, dungeonConfig, TILE, NUMBEROFLEVELS, BASESEED)

    pygame.quit()

if __name__ == "__main__":
    main()