import pygame
import time
import sys
import random
import os
import pygame.freetype
from pygame.locals import *
pygame.freetype.init()

clock = pygame.time.Clock()

WIDTH, HEIGHT = 1150, 512
FPS = 60
playing = True

Hero_sprites = ['run', 'attack', 'jump', 'dash', 'death', 'idle']
Zombie_sprites = ['attack', 'dead', 'hit', 'idle', 'run']

hills = []
enemy_attack_frame = []


font_path = os.path.join(
    os.path.dirname(
        os.path.realpath(__file__)),
    "fonts",
    "astron boy italic.ttf")
Font = pygame.freetype.Font(font_path)


pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tester')
white = (255, 255, 255)
WIN.fill(white)


class Player():
    def __init__(self, x):
        self.hero_direction = 'Right'
        self.image = pygame.image.load(
            'images/Hero/tile000.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (215, 215))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 367
        self.frame = 0
        self.process = 'default'
        self.elapsed = 0
        self.health = 100
        self.level = 1
        self.killed_n = 0
        self.killed_trans_limit = 5
        self.killed = 0

        self.run_frames = []
        self.attack_frames = []
        self.jump_frames = []
        self.dash_frames = []
        self.death_frames = []
        self.idle_frames = []

    def run(self, direction):
        if pygame.time.get_ticks() - self.elapsed > 20:
            self.elapsed = pygame.time.get_ticks()
            if self.process != 'run':
                self.frame = 0
                self.process = 'run'
            self.image = self.run_frames[self.frame]
            if direction == 'Left':
                self.hero_direction = 'Right'
            if self.frame == len(self.run_frames) - 1:
                self.frame = 0
            else:
                self.frame += 1

    def attack(self, direction):
        if pygame.time.get_ticks() - self.elapsed > 45:
            self.elapsed = pygame.time.get_ticks()
            if self.process != 'attack':
                self.frame = 0
                self.process = 'attack'
            self.image = self.attack_frames[self.frame]
            if direction == 'Left':
                self.hero_direction = 'Right'
            if self.frame == len(self.attack_frames) - 1:
                self.process = 'default'
                self.frame = 0
            else:
                self.frame += 1

    def jump(self, direction):
        if pygame.time.get_ticks() - self.elapsed > 45:
            self.elapsed = pygame.time.get_ticks()
            if self.process != 'jump':
                self.frame = 0
                self.process = 'jump'
            self.image = self.jump_frames[self.frame]
            if self.frame < 5:
                player.rect.y -= 10 / (5 - self.frame)
            if self.frame > 5:
                player.rect.y += 10 / (self.frame - 5)
            if direction == 'Left':
                self.hero_direction = 'Right'
            if self.frame == len(self.jump_frames) - 1:
                self.process = 'default'
                self.frame = 0
            else:
                self.frame += 1

    def dash(self, direction):
        if pygame.time.get_ticks() - self.elapsed > 35:
            self.elapsed = pygame.time.get_ticks()
            if self.process != 'dash':
                self.frame = 0
                self.process = 'dash'
            self.image = self.dash_frames[self.frame]
            if direction == 'Left':
                self.hero_direction = 'Right'
            if self.frame == len(self.dash_frames) - 1:
                self.process = 'default'
                self.frame = 0
            else:
                self.frame += 1

    def die(self, direction):
        if self.process != 'death':
            self.frame = 0
            self.process = 'death'
            self.elapsed = 0
        if pygame.time.get_ticks() - self.elapsed > 100:
            self.elapsed = pygame.time.get_ticks()
            self.image = self.death_frames[self.frame]
            if direction == 'Left':
                self.image = pygame.transform.flip(self.image, True, False)
                self.hero_direction = direction
            self.frame += 1

    def set_default(self, direction):
        if pygame.time.get_ticks() - self.elapsed > 45:
            self.elapsed = pygame.time.get_ticks()
            if self.process != 'default':
                self.frame = 0
                self.process = 'default'
            self.image = self.idle_frames[self.frame]
            if direction == 'Left':
                self.hero_direction = 'Right'
            if self.frame == len(self.idle_frames) - 1:
                self.frame = 0
            else:
                self.frame += 1

    def update(self, direction, enemy_frame):
        if direction != self.hero_direction:
            self.image = pygame.transform.flip(self.image, True, False)
            self.hero_direction = direction

        if self.killed_n > self.killed_trans_limit:
            self.level += 1
            self.killed_n = 0
            self.killed_trans_limit += 1

        for i in enemy_frame:
            if i == 5:
                self.health -= 0.3

        if self.health < 0.2:
            self.die(direction)

        WIN.blit(self.image, self.rect)


class background():
    def __init__(self, vel, img_link):
        self.velocity = vel
        self.img_1 = pygame.image.load(img_link).convert_alpha()
        self.img_1 = pygame.transform.scale(self.img_1, (1024, 512))
        self.background_direction = 'Right'
        self.prom = -12

    def update(self, direction, process):
        if process == 'run':
            if direction == 'Right':
                self.prom -= self.velocity

            if direction == 'Left':
                self.prom += self.velocity

        if (process == 'jump' or process == 'dash') and (
                player.frame != 13 or player.frame != 12):
            if direction == 'Right':
                self.prom -= self.velocity * 1.4
            if direction == 'Left':
                self.prom += self.velocity * 1.4

        if direction == 'Left' and player.rect.x < 900:
            self.prom += self.velocity * 4
            if self.velocity == hills[-2].velocity:
                player.rect.x += self.velocity * 4

        if direction == 'Right' and player.rect.x > 50:
            self.prom -= self.velocity * 4
            if self.velocity == hills[-2].velocity:
                player.rect.x -= self.velocity * 4

        WIN.blit(self.img_1, (self.prom, 0))
        WIN.blit(self.img_1, (1024 + self.prom, 0))
        WIN.blit(self.img_1, (self.prom - 1024, 0))
        WIN.blit(self.img_1, (2048 + self.prom, 0))
        if self.prom < -1024 or self.prom > 1024:
            self.prom = 0


class Enemie():
    def __init__(self, x):
        self.hero_direction = None
        self.velocity = 10
        self.image = pygame.image.load(
            'images/Zombie/idle/zombie_Idle_0.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (250, 250))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 390
        self.frame = 0
        self.process = 'run'
        self.elapsed = 0
        self.health = 100
        self.background_prom = -12

        self.run_frames = []
        self.dead_frames = []
        self.attack_frames = []
        self.hit_frames = []
        self.idle_frames = []

    def run(self):
        time = pygame.time.get_ticks() - self.elapsed
        if time > 68:
            self.elapsed = pygame.time.get_ticks()
            if self.process != 'run':
                self.frame = 0
                self.process = 'run'
            self.image = self.run_frames[self.frame]
            if self.hero_direction == 'Left':
                self.image = pygame.transform.flip(self.image, True, False)
            if self.frame == len(self.run_frames) - 1:
                self.frame = 0
            else:
                self.frame += 1

    def attack(self):
        time = pygame.time.get_ticks() - self.elapsed
        if time > 50:
            self.elapsed = pygame.time.get_ticks()
            if self.process != 'attack':
                self.frame = 0
                self.process = 'attack'
            self.image = self.attack_frames[self.frame]
            if self.hero_direction == 'Left':
                self.image = pygame.transform.flip(self.image, True, False)
            if self.frame == len(self.attack_frames) - 1:
                self.frame = 0
            else:
                self.frame += 1

    def death(self):
        if self.process != 'dead':
            if self.process != 'death_process':
                self.process = 'death_process'
                self.frame = 0
            time = pygame.time.get_ticks() - self.elapsed
            if time > 120:
                self.elapsed = pygame.time.get_ticks()
                self.image = self.dead_frames[self.frame]
                if self.hero_direction == 'Left':
                    self.image = pygame.transform.flip(self.image, True, False)
                if self.frame == len(self.dead_frames) - 1:
                    self.process = 'dead'
                    player.killed_n += 1
                    player.killed += 1
                else:
                    self.frame += 1

    def idle(self):
        if self.process != 'idle':
            self.process = 'idle'
        self.image = self.run_frames[0]
        if self.hero_direction == 'Left':
            self.image = pygame.transform.flip(self.image, True, False)

    def hit(self):
        time = pygame.time.get_ticks() - self.elapsed
        if time > 50:
            self.elapsed = time
            if self.process != 'hit':
                self.frame = 0
                self.process = 'hit'
            self.image = self.hit_frames[self.frame]
            if self.hero_direction == 'Left':
                self.image = pygame.transform.flip(self.image, True, False)
            if self.frame == len(self.hit_frames) - 1:
                self.frame = 0
            else:
                self.frame += 1

    def update(self, player_x, player_process, player_frame, background_prom):
        if background_prom == 0:
            self.background_prom = 0
        else:
            self.rect.x += background_prom - self.background_prom
            self.background_prom = background_prom
        if self.process == 'run':
            if self.hero_direction == 'Right':
                self.rect.x += 1
            else:
                self.rect.x -= 1

        if self.process == 'dead' or player_process == 'death':
            if player_process == 'death':
                self.idle()
            pass
        elif self.process == 'death_process':
            self.death()
        elif abs((self.rect.x - player_x)) > 80:
            if self.rect.x < -500 or self.rect.x > 1500:
                self.idle()
            else:
                self.run()
        elif player_process == 'attack' and player_frame == 7:
            self.hit()
        elif player_process == 'attack' and player_frame == 25:
            self.death()
        else:
            self.attack()

        if self.rect.x < player.rect.x:
            self.hero_direction = 'Right'
        elif self.rect.x > player.rect.x:
            self.hero_direction = 'Left'

        WIN.blit(self.image, self.rect)


class ScoreBoard():
    def __init__(self):
        self.health = pygame.Rect(1000, 13, 70, 7)
        self.health_rect = pygame.Rect(1000, 13, 140, 7)

    def update(self, health_level, player_level, zombies_killed):
        health_update = health_level * 1.4
        self.health = pygame.Rect(1000, 13, health_update, 7)

        pygame.draw.rect(WIN, (145, 54, 72), self.health_rect)
        pygame.draw.rect(WIN, (44, 252, 3), self.health)

        Font.render_to(WIN, (1000, 35), "Level: " +
                       str(player_level), (0, 0, 0), None, size=18)
        Font.render_to(WIN, (1000, 55), "Killed: " +
                       str(zombies_killed), (0, 0, 0), None, size=18)


ScoreBoard = ScoreBoard()
player = Player(50)
enemy = Enemie(250)

enemies = []
enemy = Enemie(250)
enemies.append(enemy)
passed_levels = [0]


def create_enemy(player_level):
    global enemies
    if player_level != passed_levels[-1]:
        passed_levels.append(player_level)
    random_number = random.randrange(1, 120, 1)
    if random_number in passed_levels:
        enemy_x = random.choice([1, 2])
        if enemy_x == 1:
            enemy_x = 0 - random.randrange(0, 2000, 50)
        else:
            enemy_x = random.randrange(1150, 3000, 50)
        enemy = Enemie(enemy_x)
        enemy.run_frames = enemies[0].run_frames
        enemy.dead_frames = enemies[0].dead_frames
        enemy.attack_frames = enemies[0].attack_frames
        enemy.hit_frames = enemies[0].hit_frames
        enemy.idle_frames = enemies[0].idle_frames[0]
        enemies.append(enemy)


def filter_enemy(enemies):
    enemies_frame = []
    for enemy in enemies:
        if enemy.process == 'attack':
            enemies_frame.append(enemy.frame)
    return enemies_frame


def instruction():
    Font.render_to(WIN, (20, 55), 'CTRL  +', (0, 0, 0), None, size=35)
    image = pygame.image.load('images/key.png').convert_alpha()
    image = pygame.transform.scale(image, (100, 100))
    WIN.blit(image, (150, 5))


for n in range(1, 7):
    hill = background(n**1.4 * 0.4, f'images/Hill/Hill{n}.png')
    hills.append(hill)


for i in Hero_sprites:
    n = 0
    while True:
        try:
            frame = pygame.image.load(
                f'images/Hero/{i}/tile00{n}.png').convert_alpha()
        except BaseException:
            try:
                frame = pygame.image.load(
                    f'images/Hero/{i}/tile0{n}.png').convert_alpha()
            except BaseException:
                break
        frame = pygame.transform.scale(frame, (215, 215))
        eval('player.{0}_frames.append(frame)'.format(i))
        n += 1


for i in Zombie_sprites:
    n = 0
    while True:
        try:
            frame = pygame.image.load(
                f'images/Zombie/{i}/zombie_{i.capitalize()}_{n}.png').convert_alpha()
        except BaseException:
            break
        frame = pygame.transform.scale(frame, (137, 137))
        eval('enemies[0].{0}_frames.append(frame)'.format(i))
        n += 1


right_or_left = False
direction = 'Right'


while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    right_or_left = keys[K_RIGHT] or keys[K_LEFT]

    if player.process == 'death':
        pass
    elif (keys[K_UP] or player.process == 'jump') and (player.process != 'dash'):
        player.jump(direction)
    elif keys[K_DOWN] or player.process == 'dash':
        player.dash(direction)
    elif keys[K_RIGHT] or keys[K_LEFT]:
        player.run(direction)
        if keys[K_RIGHT]:
            direction = 'Right'
        if keys[K_LEFT]:
            direction = 'Left'
    elif keys[K_LCTRL]:
        player.attack(direction)
    else:
        player.set_default(direction)

    enemy_attack_frame = filter_enemy(enemies)

    for hill in hills[:6]:
        hill.update(direction, player.process)
    for enemy in enemies:
        enemy.update(player.rect.x, player.process,
                     player.frame, hills[-2].prom)
    player.update(direction, enemy_attack_frame)
    hills[-1].update(direction, player.process)

    ScoreBoard.update(player.health, player.level, player.killed)
    create_enemy(player.level)

    if pygame.time.get_ticks() < 3000:
        instruction()

    pygame.display.update()
    clock.tick(60)
    
    if player.process == 'death' and player.frame == 23:
        time.sleep(2)
        break


WIN.fill(white)
Font.render_to(WIN, (380, 200), 'Game Over', (0, 0, 0), None, size=100)
pygame.display.update()
time.sleep(5)
