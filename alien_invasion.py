import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats
# from alien import Alien
# from avatar import Avatar
import game_functions as gf


def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("ALIEN INVASION by Aldo Nunes")

    # Create an instance to store game statistics.
    stats = GameStats(ai_settings)

    # Make a ship.
    ship = Ship(ai_settings, screen)

    # Make a group to store bullets.
    bullets = Group()

    # Make a group of aliens.
    number_of_aliens = 3
    aliens = [None, None, None]
    for i in range(number_of_aliens):
        aliens[i] = Group()

    # Create a fleet of aliens.
    # The last argument is the number of the row.
    for i in range(number_of_aliens):
        gf.create_fleet(ai_settings, screen, aliens[i], i)

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
        gf.update_bullets(ai_settings, screen, aliens, number_of_aliens, bullets)
        # print(len(bullets))

        # for i in range(number_of_aliens):
        gf.update_aliens(ai_settings, ship, aliens)

        # Redraw the screen during each pass through the loop.
        # Make the most recently drawn screen visible.
        gf.update_screen(ai_settings, screen, ship, aliens, number_of_aliens, bullets)  # avatar


run_game()
