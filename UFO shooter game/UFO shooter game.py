import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SPEED = 5
BULLET_SPEED = 10
UFO_SPEED = 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UFO Shooter")

# Load images
player_image = pygame.Surface((50, 50))
player_image.fill(GREEN)
ufo_image = pygame.Surface((40, 30))
ufo_image.fill(WHITE)

# Player class
class Player:
    def __init__(self):
        self.image = player_image
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))

    def move(self, dx):
        self.rect.x += dx
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))

# Bullet class
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x + 20, y, 10, 20)

    def move(self):
        self.rect.y -= BULLET_SPEED

# UFO class
class UFO:
    def __init__(self):
        self.image = ufo_image
        self.rect = self.image.get_rect(x=random.randint(0, WIDTH - 40), y=0)

    def move(self):
        self.rect.y += UFO_SPEED

# Main game loop
def main():
    clock = pygame.time.Clock()
    player = Player()
    bullets = []
    ufos = []
    score = 0
    running = True

    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-PLAYER_SPEED)
        if keys[pygame.K_RIGHT]:
            player.move(PLAYER_SPEED)
        if keys[pygame.K_SPACE]:
            bullets.append(Bullet(player.rect.x, player.rect.y))

        # Move bullets
        for bullet in bullets[:]:
            bullet.move()
            if bullet.rect.y < 0:
                bullets.remove(bullet)

        # Spawn UFOs
        if random.randint(1, 20) == 1:
            ufos.append(UFO())

        # Move UFOs
        for ufo in ufos[:]:
            ufo.move()
            if ufo.rect.y > HEIGHT:
                ufos.remove(ufo)

            # Check for collisions
            if ufo.rect.colliderect(player.rect):
                print("Game Over!")
                running = False
            
            for bullet in bullets[:]:
                if bullet.rect.colliderect(ufo.rect):
                    bullets.remove(bullet)
                    ufos.remove(ufo)
                    score += 1
                    break

        # Draw everything
        screen.blit(player.image, player.rect)
        for bullet in bullets:
            pygame.draw.rect(screen, RED, bullet.rect)
        for ufo in ufos:
            screen.blit(ufo.image, ufo.rect)

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
