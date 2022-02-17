import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
# from avatar import Avatar
import game_functions as gf


# Temp
def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("ALIEN INVASION by Aldo Nunes")

    # Make a ship.
    ship = Ship(ai_settings, screen)

    # Make a group to store bullets.
    bullets = Group()

    # Make a group of aliens.
    aliens = Group()

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Just a joke
    # avatar = Avatar(screen)

    # Start the main loop for the game.
    while True:

        # Watch for keyboard and mouse events.
        gf.check_events(ai_settings, screen, ship, bullets)

        # Moving the ship
        ship.update()

        # Firing bullets
        # Get rid of bullets that have dissapeared.
        gf.update_bullets(bullets)
        # print(len(bullets))

        # Moving the aliens
        gf.update_aliens(ai_settings, aliens)

        # Redraw the screen during each pass through the loop.
        # Make the most recently drawn screen visible.
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)  # avatar


run_game()
