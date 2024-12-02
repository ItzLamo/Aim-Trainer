import math
import random
import time
import pygame

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

# Constants
TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30
BG_COLOR = (0, 25, 40)
LIVES = 5
TOP_BAR_HEIGHT = 50
LABEL_FONT = pygame.font.SysFont("comicsans", 32)

# Target class
class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.1
    COLOR = "orange"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False
        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), int(self.size))

    def collide(self, x, y):
        distance = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        return distance <= self.size

# Draw the game
def draw(win, targets, elapsed_time, hits, misses):
    win.fill(BG_COLOR)
    for target in targets:
        target.draw(win)
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")
    hits_label = LABEL_FONT.render(f"Hits: {hits}", 1, "black")
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")
    win.blit(time_label, (5, 5))
    win.blit(hits_label, (WIDTH // 3, 5))
    win.blit(lives_label, (WIDTH - 150, 5))
    pygame.display.update()

# Format time
def format_time(seconds):
    return f"{int(seconds // 60):02}:{int(seconds % 60):02}"

# End screen
def end_screen(win, elapsed_time, hits, clicks):
    win.fill(BG_COLOR)
    accuracy = round((hits / clicks) * 100 if clicks > 0 else 0, 1)
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")
    hits_label = LABEL_FONT.render(f"Hits: {hits}", 1, "white")
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")
    win.blit(time_label, (WIDTH // 2 - time_label.get_width() // 2, 150))
    win.blit(hits_label, (WIDTH // 2 - hits_label.get_width() // 2, 250))
    win.blit(accuracy_label, (WIDTH // 2 - accuracy_label.get_width() // 2, 350))
    pygame.display.update()
    time.sleep(3)

# Main game loop
def main():
    clock = pygame.time.Clock()
    run = True
    targets = []
    hits, clicks, misses = 0, 0, 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        elapsed_time = time.time() - start_time
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                targets.append(Target(x, y))
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets[:]:
            target.update()
            if target.size <= 0:
                targets.remove(target)
                misses += 1
            elif click and target.collide(*mouse_pos):
                targets.remove(target)
                hits += 1

        if misses >= LIVES:
            end_screen(WIN, elapsed_time, hits, clicks)
            break

        draw(WIN, targets, elapsed_time, hits, misses)

    pygame.quit()

if __name__ == "__main__":
    main()
 # type: ignore