import pygame
import random
import math


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Player vs Enemies")


WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)


PLAYER_SIZE = 50
ENEMY_SIZE = 50
MAX_HEALTH = 100
ENEMY_COUNT = 7  
ENEMY_RESPAWN_DELAY = 100


font = pygame.font.SysFont(None, 36)


background = pygame.image.load('Space Invader Project/WhatsApp Image 2024-11-14 at 6.22.49 PM.jpeg')  
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)) 


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 8
        self.health = MAX_HEALTH

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        
        self.rect.clamp_ip(screen.get_rect())

    def reduce_health(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)
        self.speed = random.randint(2, 6) 
        self.player = player
        self.respawn_time = None  

    def update(self):
        if self.respawn_time and pygame.time.get_ticks() - self.respawn_time > ENEMY_RESPAWN_DELAY:
            self.respawn()  

        
        player_x, player_y = self.player.rect.center
        enemy_x, enemy_y = self.rect.center
        angle = math.atan2(player_y - enemy_y, player_x - enemy_x)

        self.rect.x += self.speed * math.cos(angle)
        self.rect.y += self.speed * math.sin(angle)

        
        self.rect.clamp_ip(screen.get_rect())

    def respawn(self):
        """Respawn the enemy in a random position after a collision."""
        self.rect.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)
        self.respawn_time = None  

    def collide_with_player(self):
        """Handle collision with the player."""
        self.respawn_time = pygame.time.get_ticks()  
        self.player.reduce_health(10)  


player = Player()
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

all_sprites.add(player)


for _ in range(ENEMY_COUNT):
    enemy = Enemy(player)
    all_sprites.add(enemy)
    enemies.add(enemy)


score = 0
game_over = False


clock = pygame.time.Clock()

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if not game_over:
        
        all_sprites.update()

        
        collided_enemies = pygame.sprite.spritecollide(player, enemies, False)
        for enemy in collided_enemies:
            enemy.collide_with_player()  
            score += 1  

        
        if player.health <= 0:
            game_over = True

        
        screen.blit(background, (0, 0))  
        all_sprites.draw(screen)

        
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        
        health_bar_width = 200
        health_percentage = player.health / MAX_HEALTH
        pygame.draw.rect(screen, BLACK, (10, 50, health_bar_width, 25))  
        pygame.draw.rect(screen, BLUE, (10, 50, health_percentage * health_bar_width, 25))  

    else:
        
        game_over_text = font.render("Game Over! Press R to Restart", True, BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))

        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            
            player = Player()
            all_sprites.empty()
            all_sprites.add(player)

            
            enemies.empty()
            for _ in range(ENEMY_COUNT):
                enemy = Enemy(player)
                all_sprites.add(enemy)
                enemies.add(enemy)

            score = 0
            game_over = False

    
    pygame.display.flip()


    clock.tick(60)
