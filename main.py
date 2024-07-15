import sys

import pygame
import random
import math
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

pygame.init()

win_width = 900
win_height = 700
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Игра с уровнями и стрельбой")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

font = pygame.font.Font(None, 50)
game_over_font = pygame.font.Font(None, 72)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load('player_image.png').convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (win_width // 2, win_height - 50)
        self.speed = 5
        self.health = 5
        self.is_hit = False
        self.hit_time = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[1092]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_d] or keys[1074]) and self.rect.right < win_width:
            self.rect.x += self.speed
        if (keys[pygame.K_w] or keys[1094]) and self.rect.top > 0:
            self.rect.y -= self.speed
        if (keys[pygame.K_s] or keys[1099]) and self.rect.bottom < win_height:
            self.rect.y += self.speed
        if self.is_hit:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time < 80:
                self.original_image = pygame.image.load('player_damage_image.png').convert_alpha()
                self.image = pygame.transform.scale(self.original_image, (80, 80))
            else:
                self.original_image = pygame.image.load('player_image.png').convert_alpha()
                self.image = pygame.transform.scale(self.original_image, (80, 80))

    def take_damage(self, amount):
        self.health -= amount
        self.is_hit = True
        self.hit_time = pygame.time.get_ticks()

    def shoot(self, direction):
        if direction == 'up':
            dx, dy = 0, -1
        elif direction == 'down':
            dx, dy = 0, 1
        elif direction == 'left':
            dx, dy = -1, 0
        elif direction == 'right':
            dx, dy = 1, 0
        bullet = Bullet(self.rect.centerx, self.rect.centery, dx, dy)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load('enemy_image.png').convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, win_width - self.rect.width)
        self.rect.y = 1
        self.speed = 1

    def update(self):
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed


class NewEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load('new_enemy_image.png').convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, win_height - self.rect.height)
        self.rect.y = 2

        self.speed = 1.5

    def update(self):
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

        if random.random() < 0.02:
            bullet = Bullet(self.rect.centerx, self.rect.centery, dx, dy, color=red)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, color=white):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 10
        self.dx = dx
        self.dy = dy

    def update(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

        if self.rect.bottom < 0 or self.rect.top > win_height or self.rect.right < 0 or self.rect.left > win_width:
            self.kill()


all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
new_enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(5):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)


def show_game_over(text=""):
    win.fill(black)
    game_over_text = game_over_font.render(text, True, white)
    game_over_rect = game_over_text.get_rect(center=(win_width // 2, win_height // 2 - 50))
    win.blit(game_over_text, game_over_rect)

    play_again_text = font.render("Play", True, white)
    play_again_rect = play_again_text.get_rect(center=(win_width // 2, win_height // 2 + 50))
    win.blit(play_again_text, play_again_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event_ in pygame.event.get():
            if event_.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event_.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_rect.collidepoint(mouse_pos):
                    waiting = False
                    restart_game()


def restart_game():
    global player, all_sprites, enemies, new_enemies, bullets, enemy_bullets, level
    player.health = 5
    level = 1
    all_sprites.empty()
    enemies.empty()
    new_enemies.empty()
    bullets.empty()
    enemy_bullets.empty()
    player = Player()
    all_sprites.add(player)
    for i in range(3):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)


def show_start_screen():
    win.fill(black)
    play_text = font.render("Play", True, white)
    play_rect = play_text.get_rect(center=(win_width // 2, win_height // 2))
    win.blit(play_text, play_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for _event in pygame.event.get():
            if _event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif _event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_rect.collidepoint(mouse_pos):
                    waiting = False


def show_next_level_button(level):
    win.fill(black)
    next_level_text = font.render(f"Level {level}", True, white)
    next_level_rect = next_level_text.get_rect(center=(win_width // 2, win_height // 2))
    win.blit(next_level_text, next_level_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if next_level_rect.collidepoint(mouse_pos):
                    waiting = False


running = True
clock = pygame.time.Clock()
level = 1
show_start_screen()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.shoot('up')
            elif event.key == pygame.K_DOWN:
                player.shoot('down')
            elif event.key == pygame.K_LEFT:
                player.shoot('left')
            elif event.key == pygame.K_RIGHT:
                player.shoot('right')

    all_sprites.update()

    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    new_hits = pygame.sprite.groupcollide(new_enemies, bullets, True, True)

    hits = pygame.sprite.spritecollide(player, enemies, False)
    for hit in hits:
        player.take_damage(0.8)
        if player.health <= 0:
            show_game_over("Game over")

    hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
    for hit in hits:
        player.take_damage(0.8)
        if player.health <= 0:
            show_game_over("Game over")

    if level == 1 and len(enemies) == 0:
        show_next_level_button(level + 1)
        level += 1
        for i in range(5):
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
    elif level == 2 and len(enemies) == 0:
        show_next_level_button(level + 1)
        level += 1
        new_enemy = NewEnemy()
        all_sprites.add(new_enemy)
        new_enemies.add(new_enemy)
    elif level == 3 and len(new_enemies) == 0:
        show_next_level_button(level + 1)
        level += 1
        for i in range(3):
            new_enemy = NewEnemy()
            new_enemy.speed = 1.7
            all_sprites.add(new_enemy)
            new_enemies.add(new_enemy)
    elif level == 4 and len(new_enemies) == 0:
        show_next_level_button(level + 1)
        level += 1
        for i in range(5):
            new_enemy = NewEnemy()
            new_enemy.speed = 2
            all_sprites.add(new_enemy)
            new_enemies.add(new_enemy)
    elif level == 5 and len(new_enemies) == 0:
        show_game_over("You won")

    win.fill(black)
    all_sprites.draw(win)

    health_text = font.render(f'Health: {player.health:.2f}', True, (0, 128, 128))
    level_text = font.render(f'Level: {level}', True, (50, 205, 50))
    win.blit(health_text, (10, 10))
    win.blit(level_text, (10, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()