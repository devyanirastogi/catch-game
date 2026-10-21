import asyncio
import pygame 
import random

# Initilize pygame
pygame.init() 

# CONSTANTS 
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (218, 230, 205) # sage 
TEXT_COLOR = (60, 40, 30) # espresso
PLAYER_COLOR = (80, 200,120)  # green
ITEM_COLOR = (240, 200,60)  # yellow 
PLAYER_SPEED = 8  # how fast the player moves
BASKET_WIDTH = 140
FRUIT_WIDTH = 60
BOMB_WIDTH = 60
ITEM_SPEED = 4
SPAWN_INTERVAL = 800
BOMB_CHANCE = 0.2 # 20% of spawns are bombs

# Create a screen with width and height: canvas we draw on 
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the title of the window
pygame.display.set_caption("Catch Game")


def load_scaled(path, target_width):
    #Load an image and scale it to target_width, keeping its aspect ratio 
    img = pygame.image.load(path).convert_alpha()
    scale = target_width / img.get_width()
    return pygame.transform.smoothscale(img, (target_width, round(img.get_height() * scale)))

basket_img = load_scaled("basket.png", BASKET_WIDTH)
fruit_files = ["apple.png", "banana.png", "cherries.png", "grapes.png"]
fruit_images = [load_scaled(f, FRUIT_WIDTH) for f in fruit_files]
bomb_img = load_scaled("bomb.png", BOMB_WIDTH)

font = pygame.font.Font(None, 40) # none = default for all browsers

# Create a clock to control the frame rate
clock = pygame.time.Clock()

# Game objects 
player = basket_img.get_rect()  # player hitbox matches the basket image
player.centerx = WIDTH // 2  # start in the middle of the screen
player.bottom = HEIGHT - 20  # start near the bottom of the screen

class Item:
    def __init__(self, image,kind):
        self.image = image
        self.kind = kind
        self.rect = image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.bottom = 0

    def update(self):
        self.rect.y += ITEM_SPEED

    def draw(self, surface):
        surface.blit(self.image, self.rect)

async def main():
    # Main game loop 
    running = True 
    paused = False
    items = [] 
    score = 0
    lives = 3
    game_over = False
    last_spawn = pygame.time.get_ticks() 
    while running:
        # Input: for every action by the user of the game
        # Handle events: returns list ofevents that have happened since frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: 
                    paused = not paused 
                if event.key == pygame.K_r and game_over:
                    score = 0
                    lives = 3
                    items = []
                    game_over = False
                    last_spawn = pygame.time.get_ticks()

        # Update game state
        if not paused and not game_over: 
            keys = pygame.key.get_pressed() # get the state of all keys

            if keys[pygame.K_LEFT]:
                player.x -= PLAYER_SPEED # decrease x position to move left
            if keys[pygame.K_RIGHT]:
                player.x += PLAYER_SPEED # increase x position to move right

            # Keep the player within the screen bounds
            if player.left < 0:
                player.left = 0
            if player.right > WIDTH:
                player.right = WIDTH

        # Spawn 
        if not paused and not game_over: 
            now = pygame.time.get_ticks()
            if now - last_spawn > SPAWN_INTERVAL: 
                if random.random() < BOMB_CHANCE:
                    items.append(Item(bomb_img, "bomb"))
                else: 
                    items.append(Item(random.choice(fruit_images), "fruit"))
                last_spawn = now

            # Fall 
            for item in items: 
                item.update() 

            # Only the top part of the basket counts as the opening
            catch_zone = pygame.Rect(player.x, player.y, player.width, player.height // 3)

            # Check for catches, and remove items that left the screen
            remaining = [] 
            for item in items: 
                if catch_zone.colliderect(item.rect):
                    if item.kind == "fruit":
                        score += 1
                    else: 
                        lives -= 1
                elif item.rect.top < HEIGHT:
                    remaining.append (item)
                elif item.kind == "fruit":
                    lives -= 1 # missed a fruit
            items = remaining

            if lives <= 0:
                game_over = True

        # Draw everything
        screen.fill(BACKGROUND_COLOR)  # fill with sky blue
        screen.blit(basket_img, player)
        for item in items: 
            item.draw(screen)

        # Push what we drew to the screen
        score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
        screen.blit(score_text, (10, 10))

        lives_text = font.render(f"Lives: {lives}", True, TEXT_COLOR)
        screen.blit(lives_text, lives_text.get_rect(topright=(WIDTH - 10, 10)))

        if game_over:
            over_text = font.render("GAME OVER - press R to restart", True, TEXT_COLOR)
            screen.blit(over_text, over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

        pygame.display.flip()
        clock.tick(60)  # limit to 60 FPS
        await asyncio.sleep(0)  # yield control to the event loop 

    pygame.quit()

asyncio.run(main())