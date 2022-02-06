import sys
import pygame


def check_events(ship):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            # Move the ship to the right.
            if event.key == pygame.K_RIGHT:
                ship.rect.centerx += 1




def update_screen(ai_settings, screen, ship, avatar=None):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    if avatar:
        avatar.blitme()

    # Make the most recently drawn screen visible.
    pygame.display.flip()
