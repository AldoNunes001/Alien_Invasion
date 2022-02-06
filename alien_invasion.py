import pygame

from settings import Settings
from ship import Ship
# from avatar import Avatar
import game_functions as gf


def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("ALIEN INVASION by Aldo Nunes")

    # Make a ship.
    ship = Ship(screen)

    # Just a joke
    # avatar = Avatar(screen)

    # Start the main loop for the game.
    while True:

        # Watch for keyboard and mouse events.
        gf.check_events(ship)

        # Redraw the screen during each pass through the loop.
        # Make the most recently drawn screen visible.
        gf.update_screen(ai_settings, screen, ship)  # avatar


run_game()
