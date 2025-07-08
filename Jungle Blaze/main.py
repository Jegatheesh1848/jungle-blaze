import os
import random
import pygame
from pygame.locals import *

from objects import World, Player, Button, draw_lines, load_level, draw_text, sounds

# Window setup
SIZE = WIDTH, HEIGHT = 1000, 650
tile_size = 50

pygame.init()
win = pygame.display.set_mode(SIZE)
pygame.display.set_caption('DASH')
clock = pygame.time.Clock()
FPS = 30

# background images
bg1 = pygame.image.load('assets/BG1.jpeg')
bg2 = pygame.image.load('assets/BG2.png')
bg = pygame.transform.scale(bg1, SIZE)  # Scale bg1 to fit the window size
sun = pygame.image.load('assets/sun.png')
jungle_dash = pygame.image.load('assets/jungle blaze.png')
you_won = pygame.image.load('assets/won.png')

# loading level 1
level = 1
max_level = len(os.listdir('levels/'))
data = load_level(level)

player_pos = (10, 340)

# creating world & objects
water_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
forest_group = pygame.sprite.Group()
diamond_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
bridge_group = pygame.sprite.Group()
groups = [water_group, lava_group, forest_group, diamond_group, enemies_group, exit_group, platform_group, bridge_group]
world = World(win, data, groups)
player = Player(win, player_pos, world, groups)

# creating buttons
play = pygame.image.load('assets/play.png')
replay = pygame.image.load('assets/replay.png')
home = pygame.image.load('assets/home.png')
exit = pygame.image.load('assets/exit.png')
setting = pygame.image.load('assets/setting.png')

play_btn = Button(play, (128, 64), WIDTH // 2 - WIDTH // 16, HEIGHT // 2)
replay_btn = Button(replay, (45, 42), WIDTH // 2 - 110, HEIGHT // 2 + 20)
home_btn = Button(home, (45, 42), WIDTH // 2 - 20, HEIGHT // 2 + 20)
exit_btn = Button(exit, (45, 42), WIDTH // 2 + 70, HEIGHT // 2 + 20)

# Initialize lives
lives = 4  # Player has 4 chances per level
max_lives = 4  # Set maximum lives to 4

# function to reset a level
def reset_level(level):
    global cur_score
    cur_score = 0

    data = load_level(level)
    if data:
        for group in groups:
            group.empty()
        world = World(win, data, groups)
        player.reset(win, player_pos, world, groups)

    return world


score = 0
cur_score = 0

main_menu = True
game_over = False
level_won = False
game_won = False
running = True

while running:
    # Clear the window by filling it with a color (e.g., black)
    win.fill((0, 0, 0))  # Fill the screen with black before drawing the background
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()

    # displaying background & sun image
    win.blit(bg, (0, 0))  # Background is blitted only once per frame, scaled to full screen
    win.blit(sun, (40, 40))
    
    # Draw the world and objects
    world.draw()  # Draw the world after the background
    for group in groups:
        group.draw(win)

    if main_menu:
        # Adjust the alignment of the jungle_dash image (above the start button)
        win.blit(jungle_dash, (WIDTH // 1.8 - WIDTH // 5.1, HEIGHT // 34.5))  # Adjusted Y position to align with play button

        # draw the play button
        play_game = play_btn.draw(win)
        if play_game:
            # Reset game settings for a fresh start
            main_menu = False
            game_over = False
            game_won = False
            score = 0
            level = 1  # Always reset to level 1 if starting from the menu
            lives = max_lives  # Reset lives at the start of the game
            world = reset_level(level)  # Reset to the first level

    else:
        if not game_over and not game_won:
            # Normal gameplay logic
            enemies_group.update(player)
            platform_group.update()
            exit_group.update(player)

            if pygame.sprite.spritecollide(player, diamond_group, True):
                sounds[0].play()
                cur_score += 1
                score += 1
            
            # Adjusted alignment of 'Score' and 'Lives'
            draw_text(win, f'Score: {score}', (WIDTH - 160, 10))  # Right-aligned Score
            draw_text(win, f'Lives: {lives}', (20, 10))  # Left-aligned Lives

            game_over, level_won = player.update(pressed_keys, game_over, level_won, game_won)

        if game_over and not game_won:
            # Player has lost the current level
            lives -= 1  # Reduce lives by 1
            if lives > 0:
                # Player still has lives, reset the current level
                score -= cur_score
                world = reset_level(level)
                game_over = False
            else:
                # No lives left, restart the entire game from Level 1
                level = 1  # Reset to level 1
                lives = max_lives  # Reset lives for the new run
                world = reset_level(level)
                game_over = False
                main_menu = True  # Return to main menu to start over

        if level_won:
            if level < max_level:
                level += 1
                game_level = f'levels/level{level}_data'
                if os.path.exists(game_level):
                    data = []
                    world = reset_level(level)
                    level_won = False
                    score += cur_score
                    bg = pygame.transform.scale(random.choice([bg1, bg2]), SIZE)  # Scale bg1/bg2 to full screen
            else:
                game_won = True
                bg = pygame.transform.scale(bg1, SIZE)  # Keep bg1 as background after winning, scaled to full screen
                win.blit(you_won, (WIDTH // 4, HEIGHT // 4))
                home = home_btn.draw(win)

                if home:
                    game_over = True
                    main_menu = True
                    level_won = False
                    level = 1
                    lives = max_lives  # Reset lives at the end of the game
                    world = reset_level(level)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()