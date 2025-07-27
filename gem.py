import pygame
import sys
import math
import random

pygame.init()

width, height = 800, 600
ground_height = 40
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("gem")

white = (255, 255, 255)
blue = (0, 120, 255)
red = (255, 0, 0)
black = (0, 0, 0)
gray = (180, 180, 180)

font = pygame.font.SysFont(None, 64)
small_font = pygame.font.SysFont(None, 36)
warning_text = font.render("get ready child", True, black)

radius = 8
gravity = 0.5
bounce_strength = -10
fade = 255
alive = True
started = False
start_timer = pygame.time.get_ticks()

clock = pygame.time.Clock()

def reset_game():
    global x, y, vx, vy, radius, alive, fade, start_timer, started
    x, y = width // 2, height // 2
    vx, vy = 3, 0
    radius = 8
    fade = 255
    alive = True
    started = False
    start_timer = pygame.time.get_ticks()

reset_game()

class Obstacle:
    def __init__(self, cx, cy, r):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])

    def move(self):
        self.cx += self.dx
        self.cy += self.dy

        if self.cx - self.r <= 0 or self.cx + self.r >= width:
            self.dx = -self.dx
        if self.cy - self.r <= 0 or self.cy + self.r >= height - ground_height:
            self.dy = -self.dy

    def draw(self):
        pygame.draw.circle(screen, black, (int(self.cx), int(self.cy)), self.r)

    def collide_with_player(self, px, py, pr):
        dist = math.hypot(self.cx - px, self.cy - py)
        return dist <= self.r + pr

obstacles = [
    Obstacle(150, 200, 40),
    Obstacle(450, 100, 30),
    Obstacle(650, 350, 50),
    Obstacle(300, 400, 35),
    Obstacle(550, 250, 25),
    Obstacle(700, 150, 45)
]

def draw_reset_button():
    text = small_font.render("RESET", True, black)
    button_width = 120
    button_height = 60
    bx = (width - button_width) // 2
    by = (height - button_height) // 2 + 100
    pygame.draw.rect(screen, gray, (bx, by, button_width, button_height))
    screen.blit(text, (bx + 30, by + 15))
    return pygame.Rect(bx, by, button_width, button_height)

while True:
    current_time = pygame.time.get_ticks()
    elapsed = current_time - start_timer
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if started and alive and event.type == pygame.MOUSEBUTTONDOWN:
            vy = bounce_strength
        elif not alive and event.type == pygame.MOUSEBUTTONDOWN:
            if reset_button.collidepoint(event.pos):
                reset_game()

    if elapsed >= 1000:
        started = True

    if started and alive:
        x += vx
        vy += gravity
        y += vy

        if x - radius <= 0 or x + radius >= width:
            vx = -vx
        if y - radius <= 0:
            y = radius
            vy = 0
        if y + radius >= height - ground_height:
            y = height - ground_height - radius
            alive = False
            vy = 0

        for obs in obstacles:
            if obs.collide_with_player(x, y, radius):
                alive = False
                break

    screen.fill(white)
    pygame.draw.rect(screen, blue, (0, height - ground_height, width, ground_height))

    for obs in obstacles:
        obs.move()
        obs.draw()

    if started and alive:
        pygame.draw.circle(screen, red, (int(x), int(y)), radius)
    elif not alive:
        if fade > 0 and radius > 0:
            fade = max(0, fade - 5)
            radius = max(0, radius - 1)
            ghost = (red[0], red[1], red[2], fade)
            surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, ghost, (radius, radius), radius)
            screen.blit(surface, (int(x - radius), int(y - radius)))
        reset_button = draw_reset_button()
    else:
        screen.blit(warning_text, (width // 2 - warning_text.get_width() // 2,
                                   height // 2 - warning_text.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)
