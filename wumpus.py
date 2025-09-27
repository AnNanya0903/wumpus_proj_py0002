import pygame
import random
import sys

# Constants
GRID_SIZE = 4
TILE_SIZE = 120
MARGIN = 2
WIDTH = HEIGHT = GRID_SIZE * TILE_SIZE + 40  # Extra space for status bar

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (40, 40, 40)
BREEZE_COLOR = (255, 140, 0)
STENCH_COLOR = (186, 85, 211)
GOLD_COLOR = (255, 215, 0)
AGENT_COLOR = (135, 206, 250)
PIT_COLOR = (30, 30, 30)
WUMPUS_COLOR = (255, 0, 0)
SAFE_COLOR = (34, 139, 34)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wumpus World - Enhanced Manual Mode")
clock = pygame.time.Clock()

class Cell:
    def __init__(self):
        self.has_pit = False
        self.has_wumpus = False
        self.has_gold = False
        self.breeze = False
        self.stench = False
        self.glitter = False
        self.visited = False

grid = [[Cell() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def get_neighbors(x, y):
    return [(i, j) for i, j in [(x+1,y), (x-1,y), (x,y+1), (x,y-1)] if 0 <= i < GRID_SIZE and 0 <= j < GRID_SIZE]

def setup_world():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if (i, j) != (0, 0) and random.random() < 0.15:
                grid[i][j].has_pit = True
    while True:
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        if (x, y) != (0, 0) and not grid[x][y].has_pit:
            grid[x][y].has_wumpus = True
            for nx, ny in get_neighbors(x, y):
                grid[nx][ny].stench = True
            break
    while True:
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        if (x, y) != (0, 0) and not grid[x][y].has_pit and not grid[x][y].has_wumpus:
            grid[x][y].has_gold = True
            grid[x][y].glitter = True
            break
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j].has_pit:
                for nx, ny in get_neighbors(i, j):
                    grid[nx][ny].breeze = True

def restart_game():
    global grid, agent_x, agent_y, has_gold, arrow_used, wumpus_dead, score, game_over
    grid = [[Cell() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    setup_world()
    agent_x, agent_y = 0, 0
    has_gold = False
    arrow_used = False
    wumpus_dead = False
    score = 0
    game_over = False
    grid[agent_x][agent_y].visited = True

# Initial game state
agent_x, agent_y = 0, 0
has_gold = False
arrow_used = False
wumpus_dead = False
score = 0
game_over = False
setup_world()
grid[agent_x][agent_y].visited = True

def draw_world():
    screen.fill(BLACK)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = j * TILE_SIZE
            y = i * TILE_SIZE
            cell = grid[i][j]
            tile_color = SAFE_COLOR if cell.visited else DARK_GRAY
            if (i, j) == (agent_x, agent_y):
                tile_color = AGENT_COLOR
            pygame.draw.rect(screen, tile_color, (x, y, TILE_SIZE - MARGIN, TILE_SIZE - MARGIN))
            if cell.visited:
                if cell.breeze:
                    pygame.draw.circle(screen, BREEZE_COLOR, (x+20, y+20), 10)
                if cell.stench and not wumpus_dead:
                    pygame.draw.circle(screen, STENCH_COLOR, (x+100, y+20), 10)
                if cell.glitter:
                    pygame.draw.circle(screen, GOLD_COLOR, (x+60, y+60), 15)
                if cell.has_pit:
                    pygame.draw.circle(screen, PIT_COLOR, (x+60, y+60), 20)
                if cell.has_wumpus and not wumpus_dead:
                    pygame.draw.rect(screen, WUMPUS_COLOR, (x+30, y+30, 40, 40))
                if cell.has_gold:
                    pygame.draw.circle(screen, GOLD_COLOR, (x+60, y+60), 10)

    # Status bar
    font = pygame.font.SysFont(None, 28)
    status = f"Score: {score} | Gold: {'Yes' if has_gold else 'No'} | Arrow Used: {'Yes' if arrow_used else 'No'}"
    if game_over:
        status += " | GAME OVER! Press R to restart."
    text = font.render(status, True, WHITE)
    screen.blit(text, (10, HEIGHT - 30))

    pygame.display.flip()

running = True
while running:
    clock.tick(10)
    draw_world()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                continue
            if game_over:
                continue

            new_x, new_y = agent_x, agent_y
            if event.key == pygame.K_UP:
                new_x = max(agent_x - 1, 0)
            elif event.key == pygame.K_DOWN:
                new_x = min(agent_x + 1, GRID_SIZE - 1)
            elif event.key == pygame.K_LEFT:
                new_y = max(agent_y - 1, 0)
            elif event.key == pygame.K_RIGHT:
                new_y = min(agent_y + 1, GRID_SIZE - 1)
            elif event.key == pygame.K_g:
                cell = grid[agent_x][agent_y]
                if cell.has_gold:
                    has_gold = True
                    cell.has_gold = False
                    score += 100
                    print("🎉 You grabbed the gold!")
                continue
            elif event.key == pygame.K_s and not arrow_used:
                arrow_used = True
                killed = False
                for nx, ny in get_neighbors(agent_x, agent_y):
                    if grid[nx][ny].has_wumpus:
                        grid[nx][ny].has_wumpus = False
                        wumpus_dead = True
                        killed = True
                        print("💥 You shot the Wumpus!")
                        break
                if not killed:
                    print("💨 Missed!")
                continue

            if (new_x, new_y) != (agent_x, agent_y):
                score -= 10
                agent_x, agent_y = new_x, new_y
                grid[agent_x][agent_y].visited = True
                cell = grid[agent_x][agent_y]

                if cell.has_pit:
                    print("💀 Fell into a pit. Game Over.")
                    score -= 1000
                    game_over = True
                elif cell.has_wumpus and not wumpus_dead:
                    print("🧟‍♂️ Eaten by the Wumpus. Game Over.")
                    score -= 1000
                    game_over = True
                elif cell.has_gold:
                    print("✨ You see glitter here. Press 'G' to grab gold!")

pygame.quit()
sys.exit()
