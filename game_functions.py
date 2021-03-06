import sys
import pygame
from time import sleep

from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True

    if event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True

    if event.key == pygame.K_SPACE:
        # Create a new bullet and add it to the bullets group.
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

    if event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ai_settings, screen, ship, bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            # Move the ship to the right or to the left.
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            # Stop moving.
            check_keyup_events(event, ship)


def update_screen(ai_settings, screen, ship, aliens, number_of_aliens, bullets, avatar=None):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()

    # I defined 3 rows of aliens
    for i in range(number_of_aliens):
        aliens[i].draw(screen)

    # Code to joke
    # if avatar:
    #    avatar.blitme()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(ai_settings, screen, aliens, number_of_aliens, bullets):
    """Update position of bullets and get rid of old ones."""
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, aliens, number_of_aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, aliens, number_of_aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    for i in range(number_of_aliens):
        collisions = pygame.sprite.groupcollide(bullets, aliens[i], True, True)

    # Check if all aliens have been destroyed.
    count = 0
    for i in range(number_of_aliens):
        count += len(aliens[i])

    # Repopulate the fleet
    if count == 0:
        bullets.empty()
        for j in range(number_of_aliens):
            create_fleet(ai_settings, screen, aliens[j], j)


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if the limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width)) - 1
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width

    if row % 2 == 0:
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.y = alien.rect.height + 2 * alien.rect.height * row
        # alien.y = alien_width * row
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        aliens.add(alien)

    elif row % 2 == 1:
        alien.x = ai_settings.screen_width - 2 * alien_width - 2 * alien_width * alien_number
        alien.y = alien.rect.height + 2 * alien.rect.height * row
        # alien.y = 10 + alien_width * row
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        aliens.add(alien)


def create_fleet(ai_settings, screen, aliens, row):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    # Spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)

    # Create the first row of aliens.
    for alien_number in range(number_aliens_x):
        # Create an alien and place it in the row.
        create_alien(ai_settings, screen, aliens, alien_number, row)


def check_fleet_edges(ai_settings, aliens, row):
    """Respond appropriately if any aliens have reached an edge."""
    for i in range(len(aliens)):
        for alien in aliens[i].sprites():
            if alien.check_edges():
                change_fleet_direction(ai_settings, aliens, i)
                break


def change_fleet_direction(ai_settings, aliens, row):
    """Drop the entire fleet and change the fleet's direction."""
    for i in range(len(aliens)):
        for alien in aliens[i].sprites():
            alien.rect.y += ai_settings.fleet_drop_speed

        ai_settings.fleet_direction[row] *= -1


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1

        # Empty the list of aliens and bullets.
        for alien in aliens:
            alien.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        for i in range(len(aliens)):
            create_fleet(ai_settings, screen, aliens[i], i)
        ship.center_ship()

        # Pause.
        sleep(1)

    else:
        stats.game_active = False


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for i in range(len(aliens)):
        for alien in aliens[i].sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this same as if the ship got hit.
                ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
                break


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """Update the positions of all aliens in the fleet."""
    for row in range(len(aliens)):
        check_fleet_edges(ai_settings, aliens, row)
        check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

        if row % 2 == 0:
            aliens[row].update(row, 1)
        elif row % 2 == 1:
            aliens[row].update(row, -1)

        if pygame.sprite.spritecollideany(ship, aliens[row]):
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
