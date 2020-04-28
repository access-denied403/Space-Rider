import sys
import pygame
from pygame.locals import *

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Rider')

BACKGROUND = pygame.image.load('Space-Rider/background.jpg')
JET = pygame.image.load('Space-Rider/jet.png')
ENEMY = pygame.image.load('Space-Rider/enemy.png')
SHOT_SOUND = pygame.mixer.Sound('Space-Rider/shot.wav')
EXPLODE_SOUND = pygame.mixer.Sound('Space-Rider/explosion.wav')
BACKGROUND_MUSIC = pygame.mixer.music.load('Space-Rider/bgsound.wav')
pygame.mixer.music.play(-1)

FPS = 60
FPS_CLOCK = pygame.time.Clock()

RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left = False
        self.right = False
        self.speed = 10
        self.hitbox = (self.x, self.y, 50, 60)

    def draw(self, WINDOW):
        WINDOW.blit(JET, (self.x, self.y))
        self.hitbox = (self.x, self.y, 50, 60)
        # pygame.draw.rect(WINDOW, RED, self.hitbox, 2)


class Projectile(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = 15

    def draw(self, WINDOW):
        pygame.draw.circle(WINDOW, self.color, (self.x, self.y), self.radius)


class Enemy(object):
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.speed = 5
        self.hitbox = (self.x, self.y, 95, 75)
        self.health = 100
        self.visible = True

    def draw(self, WINDOW):
        if self.visible:
            self.move()
            WINDOW.blit(ENEMY, (self.x, self.y))
            self.hitbox = (self.x, self.y, 95, 75)
            pygame.draw.rect(WINDOW, RED, (self.hitbox[0], self.hitbox[1] - 20, 10, 20))
            pygame.draw.rect(WINDOW, GREEN, (self.hitbox[0], self.hitbox[1] - 20, 10 - (10 - self.health), 20))
            # pygame.draw.rect(WINDOW, RED, self.hitbox, 2)

    def move(self):
        if self.speed > 0:
            if self.x + self.speed < self.path[1]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
        else:
            if self.x - self.speed > self.path[0]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1

    def hit(self):
        if self.health > 0:
            bullets.pop(bullets.index(bullet))
            self.health -= 1
        else:
            self.visible = False
            EXPLODE_SOUND.play()


def redraw_game_window():
    WINDOW.blit(BACKGROUND, (0,0))
    player.draw(WINDOW)
    enemy.draw(WINDOW)
    for bullet in bullets:
        bullet.draw(WINDOW)
    pygame.display.update()


enemy = Enemy(100, 10, 100, 83, 650)
player = Player(100, 700, 64, 50)
bullets = []
while True:
    FPS_CLOCK.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    for bullet in bullets:
        if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1]:
            if bullet.x + bullet.radius > enemy.hitbox[0] and bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]:
                enemy.hit()

        if bullet.y < 800 and bullet.y > 0:
            bullet.y -= bullet.speed
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if len(bullets) < 50:
            SHOT_SOUND.play()
            bullets.append(Projectile(round(player.x + player.width // 2) + 10, round(player.y + player.height // 2), 6, RED))
            bullets.append(Projectile(round(player.x + player.width // 3) - 12, round(player.y + player.height // 2), 6, RED))

    if keys[pygame.K_LEFT] and player.x > player.speed:
        player.x -= player.speed
        player.left = True
        player.right = False
    elif keys[pygame.K_RIGHT] and player.x < 800 - player.width - player.speed:
        player.x += player.speed
        player.left = False
        player.right = True
    else:
        player.left = False
        player.right = False        
    redraw_game_window()

pygame.quit()
