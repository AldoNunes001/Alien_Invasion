import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien imgage and set its rect attribute.
        self.image = pygame.image.load('images/alien1.png')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self, row, factor):
        """Move the alien."""
        if row % 2 == 0:
            self.x += (factor * self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction[row])
        elif row % 2 == 1:
            self.x += (factor * self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction[row])

        self.rect.x = self.x
