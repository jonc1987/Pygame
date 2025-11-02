"""Simple 2D platformer built with pygame."""
import sys
import pygame

# --- Constants ---
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.8
TERMINAL_VELOCITY = 20
PLAYER_SPEED = 5
JUMP_SPEED = -16
BACKGROUND_COLOR = (135, 206, 235)  # Sky blue


class Platform(pygame.sprite.Sprite):
    """Static platform that the player and enemies can stand on."""

    def __init__(self, rect, color=(100, 100, 100)):
        super().__init__()
        self.rect = pygame.Rect(rect)
        self.image = pygame.Surface(self.rect.size)
        self.image.fill(color)
        self.color = color

    def draw(self, surface, offset_x):
        surface.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Player(pygame.sprite.Sprite):
    """Controllable hero that can run and jump."""

    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((70, 130, 180))  # Steel blue
        self.rect = self.image.get_rect(topleft=position)
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.spawn_point = pygame.Vector2(position)

    def handle_input(self, keys):
        self.velocity.x = 0
        if keys[pygame.K_LEFT]:
            self.velocity.x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.velocity.x = PLAYER_SPEED
        if keys[pygame.K_UP] and self.on_ground:
            self.velocity.y = JUMP_SPEED
            self.on_ground = False

    def apply_gravity(self):
        self.velocity.y = min(self.velocity.y + GRAVITY, TERMINAL_VELOCITY)

    def horizontal_collisions(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.x > 0:
                    self.rect.right = platform.rect.left
                elif self.velocity.x < 0:
                    self.rect.left = platform.rect.right

    def vertical_collisions(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity.y = 0
                    self.on_ground = True
                elif self.velocity.y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity.y = 0

    def update(self, keys, platforms):
        self.handle_input(keys)
        self.apply_gravity()

        # Move horizontally and resolve collisions.
        self.rect.x += self.velocity.x
        self.horizontal_collisions(platforms)

        # Move vertically and resolve collisions.
        self.rect.y += self.velocity.y
        self.vertical_collisions(platforms)

    def reset(self):
        """Return the player to the spawn point."""
        self.rect.topleft = self.spawn_point.xy
        self.velocity.update(0, 0)


class Enemy(pygame.sprite.Sprite):
    """Simple patrolling enemy that walks between two x-coordinates."""

    def __init__(self, position, patrol_range, speed=2):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((200, 70, 70))
        self.rect = self.image.get_rect(topleft=position)
        self.min_x, self.max_x = patrol_range
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        # Reverse direction when reaching patrol boundaries.
        if self.rect.left <= self.min_x or self.rect.right >= self.max_x:
            self.speed *= -1
            self.rect.x += self.speed

    def draw(self, surface, offset_x):
        surface.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Level:
    """Encapsulates the level geometry, enemies, and camera."""

    def __init__(self, player):
        self.player = player
        self.level_width = 2600
        self.platforms = []
        self.enemies = pygame.sprite.Group()
        self.offset_x = 0
        self.goal_rect = pygame.Rect(self.level_width - 100, HEIGHT - 200, 40, 160)
        self._build_level()

    def _add_platform(self, rect, color=(100, 100, 100)):
        platform = Platform(rect, color)
        self.platforms.append(platform)
        return platform

    def _build_level(self):
        # Ground platform spanning the entire level width.
        self._add_platform((0, HEIGHT - 40, self.level_width, 40), (110, 70, 30))

        # Floating platforms of varying heights.
        self._add_platform((200, HEIGHT - 160, 200, 20))
        self._add_platform((500, HEIGHT - 260, 200, 20))
        self._add_platform((850, HEIGHT - 320, 150, 20))
        self._add_platform((1200, HEIGHT - 220, 220, 20))
        self._add_platform((1600, HEIGHT - 180, 180, 20))
        self._add_platform((1900, HEIGHT - 280, 160, 20))
        self._add_platform((2200, HEIGHT - 140, 200, 20))

        # Enemy patrolling on a mid-level platform.
        enemy_platform = self._add_platform((1400, HEIGHT - 120, 300, 20))
        enemy = Enemy((enemy_platform.rect.x + 20, enemy_platform.rect.y - 40),
                      (enemy_platform.rect.x, enemy_platform.rect.right))
        self.enemies.add(enemy)

    def reset_player(self):
        self.player.reset()

    def update(self, keys):
        self.player.update(keys, self.platforms)
        self.enemies.update()

        # If the player touches an enemy, reset to the start.
        if pygame.sprite.spritecollideany(self.player, self.enemies):
            self.reset_player()

        # Smooth camera that follows the player horizontally.
        target_offset = self.player.rect.centerx - WIDTH // 2
        target_offset = max(0, min(target_offset, self.level_width - WIDTH))
        # Linear interpolation (lerp) for smooth scrolling.
        self.offset_x += (target_offset - self.offset_x) * 0.1

    def check_win(self):
        return self.player.rect.colliderect(self.goal_rect)

    def draw(self, surface):
        surface.fill(BACKGROUND_COLOR)

        # Draw all platforms with camera offset.
        for platform in self.platforms:
            platform.draw(surface, self.offset_x)

        # Draw goal flag pole and banner.
        pole_rect = pygame.Rect(self.goal_rect.x - self.offset_x, self.goal_rect.y - 120, 8, 200)
        pygame.draw.rect(surface, (180, 180, 180), pole_rect)
        flag_points = [
            (self.goal_rect.x - self.offset_x + 8, self.goal_rect.y - 120),
            (self.goal_rect.x - self.offset_x + 8, self.goal_rect.y - 80),
            (self.goal_rect.x - self.offset_x + 8 + 60, self.goal_rect.y - 100),
        ]
        pygame.draw.polygon(surface, (255, 0, 0), flag_points)

        # Draw enemy sprites.
        for enemy in self.enemies:
            enemy.draw(surface, self.offset_x)

        # Finally draw the player.
        surface.blit(self.player.image, (self.player.rect.x - self.offset_x, self.player.rect.y))

        # Draw the start marker for reference.
        start_rect = pygame.Rect(self.player.spawn_point.x - self.offset_x, HEIGHT - 40, 60, 5)
        pygame.draw.rect(surface, (0, 0, 0), start_rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Platformer Adventure")
    clock = pygame.time.Clock()

    player = Player((100, HEIGHT - 200))
    level = Level(player)
    font = pygame.font.SysFont(None, 64)

    game_won = False
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if not game_won:
            level.update(keys)
            if level.check_win():
                game_won = True

        level.draw(screen)

        if game_won:
            # Render a translucent overlay with the victory message.
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            text = font.render("You Win!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
