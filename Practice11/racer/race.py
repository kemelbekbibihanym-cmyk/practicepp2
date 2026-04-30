import pygame
import random
import time

pygame.init()

WIDTH = 400
HEIGHT = 600
last_speedup = 0
N = 5  
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load Assets
image_background = pygame.image.load('resources/AnimatedStreet.png')
image_player = pygame.image.load('resources/Player.png')
image_enemy = pygame.image.load('resources/Enemy.png')
coin_image = pygame.image.load('resources/dollar.png').convert_alpha()

collected = 0

pygame.mixer.music.load('resources/background.wav')
pygame.mixer.music.play(-1)
sound_crash = pygame.mixer.Sound('resources/crash.wav')

font = pygame.font.SysFont("Verdana", 60)
fontt = pygame.font.SysFont("Verdana", 20)

image_game_over = font.render("Game Over", True, "black")
image_game_over_rect = image_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_player
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_enemy
        self.rect = self.image.get_rect()
        self.speed = 10
        self.generate_random_rect()

    def generate_random_rect(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.generate_random_rect()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_image
        self.speed = 5 # Speed at which coins fall
        self.size = 1
        self.rect = self.image.get_rect()
        self.generate_random_rect()

    def generate_random_rect(self):
        self.size = random.randint(1, 3)
        # Scale the coin based on random size
        side = int(30 * (self.size * 0.5))
        self.image = pygame.transform.scale(coin_image, (side, side))
        # Update rect after scaling
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0 # Start at the top

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.generate_random_rect()

# Initialization
player = Player()
enemy = Enemy()
coin = Coin()

all_sprites = pygame.sprite.Group(player, enemy, coin)
enemy_sprites = pygame.sprite.Group(enemy)
coin_sprites = pygame.sprite.Group(coin)

clock = pygame.time.Clock()
FPS = 60
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement Logic
    player.move()
    for entity in all_sprites:
        if entity != player: # Let enemies and coins fall
            entity.move()

    # Collision Logic: Coins
    if pygame.sprite.spritecollideany(player, coin_sprites):
        collected += coin.size
        # Speed up logic
        if collected // N > last_speedup:
            enemy.speed += 2
            last_speedup = collected // N
        coin.generate_random_rect()

    # Collision Logic: Enemy
    if pygame.sprite.spritecollideany(player, enemy_sprites):
        sound_crash.play()
        pygame.mixer.music.stop()
        screen.fill("red")
        screen.blit(image_game_over, image_game_over_rect)
        pygame.display.flip()
        time.sleep(2)
        running = False

    # Drawing
    screen.blit(image_background, (0, 0))
    score_img = fontt.render(f"Score: {collected}", True, "black")
    screen.blit(score_img, (WIDTH - 120, 10))
    
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()