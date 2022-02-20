class Settings:
    """A class to store all setings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings.
        self.ship_speed_factor = 2.5

        # Bullets settings
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 128, 255, 0
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = [None, None, None]
        number_of_aliens = 3
        for i in range(number_of_aliens):
            self.fleet_direction[i] = 1

