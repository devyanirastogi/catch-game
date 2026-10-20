import asyncio
import pygame 
import random

# initilize pygame
pygame.init() 

# CONSTANTS 
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (30, 30, 50)  # dark blue 
PLAYER_COLOR = (80, 200,120)  # green
ITEM_COLOR = (240, 200,60)  # yellow 
PLAYER_SPEED = 8  # how fast the player moves
ITEM_SIZE = 30
ITEM_SPEED = 4
SPAWN_INTERVAL = 800

# create a screen with width and height: canvas we draw on 
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# set the title of the window
pygame.display.set_caption("Catch Game")

# create a clock to control the frame rate
clock = pygame.time.Clock()

# Game objects 
player = pygame.Rect (0,0, 100, 20)  # player is a rectangle
player.centerx = WIDTH // 2  # start in the middle of the screen
player.bottom = HEIGHT - 20  # start near the bottom of the screen

async def main():
    # main game loop 
    running = True 
    paused = False
    items = [] 
    last_spawn = pygame.time.get_ticks() 
    while running:
        # input: for every action by the user of the game
        # handle events: returns list ofevents that have happened since frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_q: 
                    running = False 
                if event.key == pygame.K_p: 
                    paused = not paused 

        # update game state
        if not paused: 
            keys = pygame.key.get_pressed() # get the state of all keys

            if keys[pygame.K_LEFT]:
                player.x -= PLAYER_SPEED # decrease x position to move left
            if keys[pygame.K_RIGHT]:
                player.x += PLAYER_SPEED # increase x position to move right

            # keep the player within the screen bounds
            if player.left < 0:
                player.left = 0
            if player.right > WIDTH:
                player.right = WIDTH

        # spawn 
        now = pygame.time.get_ticks()
        if now - last_spawn > SPAWN_INTERVAL: 
            x = random.randint (0, )

        # draw everything
        screen.fill(BACKGROUND_COLOR)  # fill with dark blue
        pygame.draw.rect(screen, PLAYER_COLOR, player)  # draw player rectangle
        pygame.draw.circle(screen, ITEM_COLOR, (200,150), 15)  # draw an item in the middle

        # push what we drew to the screen
        pygame.display.flip()
        clock.tick(60)  # limit to 60 FPS
        await asyncio.sleep(0)  # yield control to the event loop 

    pygame.quit()

asyncio.run(main())