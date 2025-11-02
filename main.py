
"""Simple multi-level 2D platformer built with pygame."""
import sys
from typing import Dict, List, Optional, Tuple

import pygame

# --- Constants ---
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.8
TERMINAL_VELOCITY = 20
PLAYER_SPEED = 5
JUMP_SPEED = -16
BACKGROUND_COLOR = (135, 206, 235)  # Default sky blue

# Level layout configuration. Using explicit dictionaries keeps the
# geometry, spawn points, and decorative elements easy to tweak.
LEVEL_DATA: List[Dict] = [
    {
        "name": "Sunny Fields",
        "width": 2400,
        "bounds": (-200, 2400),
        "spawn": (80, HEIGHT - 220),
        "goal": {"x": 2200, "y": HEIGHT - 200, "height": 170},
        "ground_color": (124, 92, 60),
        "platforms": [
            {"rect": (180, HEIGHT - 180, 220, 20)},
            {"rect": (520, HEIGHT - 260, 220, 20)},
            {"rect": (860, HEIGHT - 320, 180, 20)},
            {"rect": (1220, HEIGHT - 230, 280, 20)},
            {"rect": (1660, HEIGHT - 210, 200, 20)},
            {"rect": (1940, HEIGHT - 290, 160, 20)},
        ],
        "enemies": [
            {
                "position": (1240, HEIGHT - 230 - 40),
                "patrol": (1220, 1220 + 280),
                "speed": 2.5,
            },
        ],
        "decorations": {
            "clouds": [
                {"x": 140, "y": 120, "scale": 1.1},
                {"x": 540, "y": 90, "scale": 0.9},
                {"x": 960, "y": 130, "scale": 1.3},
                {"x": 1720, "y": 110, "scale": 1.1},
            ],
            "bushes": [
                {"x": -150, "y": HEIGHT - 120, "width": 160},
                {"x": 480, "y": HEIGHT - 120, "width": 140},
                {"x": 980, "y": HEIGHT - 110, "width": 200},
                {"x": 1620, "y": HEIGHT - 115, "width": 180},
            ],
            "hills": [
                {"x": -200, "width": 420, "height": 130, "color": (130, 200, 130), "parallax": 0.2},
                {"x": 600, "width": 360, "height": 160, "color": (120, 190, 120), "parallax": 0.15},
                {"x": 1500, "width": 480, "height": 150, "color": (140, 205, 140), "parallax": 0.1},
            ],
            "ground_fill": (120, 190, 120),
        },
    },
    {
        "name": "Crystal Cavern",
        "width": 2600,
        "bounds": (-220, 2600),
        "spawn": (60, HEIGHT - 260),
        "goal": {"x": 2380, "y": HEIGHT - 220, "height": 180},
        "ground_color": (90, 75, 120),
        "background_color": (100, 120, 160),
        "platforms": [
            {"rect": (240, HEIGHT - 200, 160, 20)},
            {"rect": (470, HEIGHT - 300, 200, 20)},
            {"rect": (760, HEIGHT - 360, 180, 20)},
            {"rect": (1050, HEIGHT - 280, 220, 20)},
            {"rect": (1380, HEIGHT - 200, 220, 20)},
            {"rect": (1700, HEIGHT - 300, 200, 20)},
            {"rect": (1980, HEIGHT - 240, 200, 20)},
            {"rect": (2160, HEIGHT - 320, 200, 20)},
        ],
        "enemies": [
            {
                "position": (1090, HEIGHT - 280 - 40),
                "patrol": (1050, 1050 + 220),
                "speed": 2.0,
            },
            {
                "position": (1720, HEIGHT - 300 - 40),
                "patrol": (1700, 1700 + 200),
                "speed": 2.5,
            },
        ],
        "decorations": {
            "clouds": [
                {"x": 200, "y": 100, "scale": 0.8},
                {"x": 880, "y": 70, "scale": 1.4},
                {"x": 1500, "y": 90, "scale": 1.0},
                {"x": 2100, "y": 60, "scale": 0.9},
            ],
            "bushes": [
                {"x": -100, "y": HEIGHT - 125, "width": 140, "color": (70, 110, 140)},
                {"x": 820, "y": HEIGHT - 118, "width": 160, "color": (90, 130, 170)},
                {"x": 1600, "y": HEIGHT - 130, "width": 180, "color": (80, 120, 160)},
                {"x": 2200, "y": HEIGHT - 120, "width": 200, "color": (70, 110, 150)},
            ],
            "hills": [
                {"x": -220, "width": 520, "height": 180, "color": (90, 110, 150), "parallax": 0.15},
                {"x": 900, "width": 480, "height": 160, "color": (110, 130, 170), "parallax": 0.08},
                {"x": 1780, "width": 500, "height": 190, "color": (80, 100, 140), "parallax": 0.12},
            ],
            "ground_fill": (90, 110, 150),
        },
    },
    {
        "name": "Sunset Heights",
        "width": 2800,
        "bounds": (-250, 2800),
        "spawn": (120, HEIGHT - 240),
        "goal": {"x": 2550, "y": HEIGHT - 260, "height": 200},
        "ground_color": (150, 90, 40),
        "background_color": (205, 150, 120),
        "platforms": [
            {"rect": (320, HEIGHT - 260, 200, 20)},
            {"rect": (640, HEIGHT - 340, 220, 20)},
            {"rect": (980, HEIGHT - 280, 180, 20)},
            {"rect": (1280, HEIGHT - 360, 260, 20)},
            {"rect": (1620, HEIGHT - 300, 220, 20)},
            {"rect": (1920, HEIGHT - 240, 200, 20)},
            {"rect": (2140, HEIGHT - 320, 220, 20)},
            {"rect": (2400, HEIGHT - 260, 220, 20)},
        ],
        "enemies": [
            {
                "position": (1340, HEIGHT - 360 - 40),
                "patrol": (1280, 1280 + 260),
                "speed": 3.0,
            },
            {
                "position": (2160, HEIGHT - 320 - 40),
                "patrol": (2140, 2140 + 220),
                "speed": 2.8,
            },
        ],
        "decorations": {
            "clouds": [
                {"x": 160, "y": 110, "scale": 1.2},
                {"x": 620, "y": 90, "scale": 1.0},
                {"x": 1180, "y": 120, "scale": 1.4},
                {"x": 1900, "y": 100, "scale": 1.1},
                {"x": 2400, "y": 130, "scale": 0.9},
            ],
            "bushes": [
                {"x": -80, "y": HEIGHT - 110, "width": 170, "color": (180, 120, 60)},
                {"x": 740, "y": HEIGHT - 115, "width": 200, "color": (200, 140, 80)},
                {"x": 1500, "y": HEIGHT - 120, "width": 220, "color": (190, 130, 70)},
                {"x": 2220, "y": HEIGHT - 115, "width": 180, "color": (210, 150, 90)},
            ],
            "hills": [
                {"x": -260, "width": 520, "height": 200, "color": (230, 170, 120), "parallax": 0.1},
                {"x": 940, "width": 520, "height": 220, "color": (210, 150, 100), "parallax": 0.08},
                {"x": 1900, "width": 520, "height": 210, "color": (200, 140, 90), "parallax": 0.12},
            ],
            "ground_fill": (210, 150, 110),
        },
    },
]


class Platform(pygame.sprite.Sprite):
    """Static platform that the player and enemies can stand on."""

    def __init__(self, rect: Tuple[int, int, int, int], color: Tuple[int, int, int] = (100, 100, 100)):
        super().__init__()
        self.rect = pygame.Rect(rect)
        self.image = pygame.Surface(self.rect.size)
        self.image.fill(color)

    def draw(self, surface: pygame.Surface, offset_x: float) -> None:
        surface.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Player(pygame.sprite.Sprite):
    """Controllable hero that can run, jump, and backtrack."""

    def __init__(self, position: Tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((70, 130, 180))  # Steel blue hero
        self.rect = self.image.get_rect(topleft=position)
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.spawn_point = pygame.Vector2(position)

    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        self.velocity.x = 0
        move_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        move_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]

        if move_left and not move_right:
            self.velocity.x = -PLAYER_SPEED
        elif move_right and not move_left:
            self.velocity.x = PLAYER_SPEED

        if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.on_ground:
            self.velocity.y = JUMP_SPEED
            self.on_ground = False

    def apply_gravity(self) -> None:
        self.velocity.y = min(self.velocity.y + GRAVITY, TERMINAL_VELOCITY)

    def horizontal_collisions(self, platforms: List[Platform]) -> None:
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.x > 0:
                    self.rect.right = platform.rect.left
                elif self.velocity.x < 0:
                    self.rect.left = platform.rect.right

    def vertical_collisions(self, platforms: List[Platform]) -> None:
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

    def update(self, keys: pygame.key.ScancodeWrapper, platforms: List[Platform]) -> None:
        self.handle_input(keys)
        self.apply_gravity()

        # Move horizontally and resolve collisions.
        self.rect.x += self.velocity.x
        self.horizontal_collisions(platforms)

        # Move vertically and resolve collisions.
        self.rect.y += self.velocity.y
        self.vertical_collisions(platforms)

    def reset(self) -> None:
        """Return the player to the current spawn point."""
        self.rect.topleft = (int(self.spawn_point.x), int(self.spawn_point.y))
        self.velocity.update(0, 0)

    def set_spawn(self, position: Tuple[float, float]) -> None:
        """Update the player's spawn and snap them to it."""
        self.spawn_point.update(position)
        self.reset()


class Enemy(pygame.sprite.Sprite):
    """Simple patrolling enemy that walks between two x-coordinates."""

    def __init__(self, position: Tuple[int, int], patrol_range: Tuple[int, int], speed: float = 2):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((200, 70, 70))
        self.rect = self.image.get_rect(topleft=position)
        self.min_x, self.max_x = patrol_range
        self.speed = speed

    def update(self) -> None:
        self.rect.x += self.speed
        # Reverse direction when reaching patrol boundaries.
        if self.rect.left <= self.min_x or self.rect.right >= self.max_x:
            self.speed *= -1
            self.rect.x += self.speed

    def draw(self, surface: pygame.Surface, offset_x: float) -> None:
        surface.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Level:
    """Encapsulates the level geometry, enemies, and camera."""

    def __init__(self, player: Player, data: Dict):
        self.player = player
        self.name = data.get("name", "Level")
        self.width = data["width"]
        self.world_left, self.world_right = data.get("bounds", (0, self.width))
        self.background_color = data.get("background_color", BACKGROUND_COLOR)
        self.decorations = data.get("decorations", {})
        self.ground_fill_color = self.decorations.get("ground_fill", (120, 180, 110))
        self.platforms: List[Platform] = []
        self.enemies = pygame.sprite.Group()
        self.offset_x = 0.0

        self.spawn_point = pygame.Vector2(data["spawn"])  # Save for resets
        self.player.set_spawn(tuple(self.spawn_point))

        self.goal_rect = pygame.Rect(
            data["goal"]["x"],
            data["goal"]["y"],
            data["goal"].get("width", 40),
            data["goal"].get("height", 160),
        )

        ground_color = data.get("ground_color", (110, 70, 30))
        ground_rect = (
            self.world_left - 400,
            HEIGHT - 40,
            (self.world_right - self.world_left) + 800,
            40,
        )
        self._add_platform(ground_rect, ground_color)

        for platform in data.get("platforms", []):
            rect = platform["rect"]
            color = platform.get("color", (120, 120, 120))
            self._add_platform(rect, color)

        for enemy_cfg in data.get("enemies", []):
            enemy = Enemy(
                enemy_cfg["position"],
                enemy_cfg["patrol"],
                enemy_cfg.get("speed", 2),
            )
            self.enemies.add(enemy)

    def _add_platform(self, rect: Tuple[int, int, int, int], color: Tuple[int, int, int]) -> Platform:
        platform = Platform(rect, color)
        self.platforms.append(platform)
        return platform

    def reset_player(self) -> None:
        self.player.reset()

    def update(self, keys: pygame.key.ScancodeWrapper) -> None:
        self.player.update(keys, self.platforms)
        self.enemies.update()

        # If the player touches an enemy, reset to the start.
        if pygame.sprite.spritecollideany(self.player, self.enemies):
            self.reset_player()

        # Respawn if the player falls off-screen.
        if self.player.rect.top > HEIGHT + 200:
            self.reset_player()

        # Smooth camera that follows the player horizontally.
        target_offset = self.player.rect.centerx - WIDTH // 2
        max_offset = self.world_right - WIDTH
        min_offset = self.world_left
        if max_offset < min_offset:
            max_offset = min_offset
        target_offset = max(min_offset, min(target_offset, max_offset))
        # Linear interpolation (lerp) for smooth scrolling.
        self.offset_x += (target_offset - self.offset_x) * 0.1

    def check_win(self) -> bool:
        return self.player.rect.colliderect(self.goal_rect)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(self.background_color)
        self._draw_background(surface)

        # Draw all platforms with camera offset.
        for platform in self.platforms:
            platform.draw(surface, self.offset_x)

        # Draw enemy sprites.
        for enemy in self.enemies:
            enemy.draw(surface, self.offset_x)

        # Draw goal flag pole and banner.
        goal_body = pygame.Rect(
            self.goal_rect.x - self.offset_x,
            self.goal_rect.y,
            self.goal_rect.width,
            self.goal_rect.height,
        )
        pygame.draw.rect(surface, (245, 245, 245), goal_body, border_radius=6)
        pole_rect = pygame.Rect(
            self.goal_rect.x - self.offset_x + self.goal_rect.width - 6,
            self.goal_rect.y - 140,
            8,
            self.goal_rect.height + 140,
        )
        pygame.draw.rect(surface, (180, 180, 180), pole_rect)
        flag_points = [
            (self.goal_rect.x - self.offset_x + self.goal_rect.width + 2, self.goal_rect.y - 120),
            (self.goal_rect.x - self.offset_x + self.goal_rect.width + 2, self.goal_rect.y - 70),
            (self.goal_rect.x - self.offset_x + self.goal_rect.width + 60, self.goal_rect.y - 95),
        ]
        pygame.draw.polygon(surface, (255, 0, 0), flag_points)

        # Finally draw the player.
        surface.blit(self.player.image, (self.player.rect.x - self.offset_x, self.player.rect.y))

        # Draw the start marker for reference.
        start_rect = pygame.Rect(self.spawn_point.x - self.offset_x, HEIGHT - 44, 60, 8)
        pygame.draw.rect(surface, (30, 30, 30), start_rect)

    def _draw_background(self, surface: pygame.Surface) -> None:
        """Render simple parallax decorations behind gameplay layers."""
        ground_horizon = int(HEIGHT * 0.75)
        pygame.draw.rect(surface, self.background_color, (0, 0, WIDTH, ground_horizon))
        pygame.draw.rect(surface, self.ground_fill_color, (0, ground_horizon, WIDTH, HEIGHT - ground_horizon))

        for hill in self.decorations.get("hills", []):
            parallax = hill.get("parallax", 0.2)
            base_x = hill["x"] - self.offset_x * parallax
            width = hill.get("width", 320)
            height = hill.get("height", 140)
            color = hill.get("color", (120, 180, 120))
            points = [
                (base_x, HEIGHT),
                (base_x + width / 2, HEIGHT - height),
                (base_x + width, HEIGHT),
            ]
            pygame.draw.polygon(surface, color, points)

        for cloud in self.decorations.get("clouds", []):
            parallax = cloud.get("parallax", 0.5)
            base_x = cloud["x"] - self.offset_x * parallax
            base_y = cloud.get("y", 120)
            scale = cloud.get("scale", 1.0)
            radius = int(20 * scale)
            positions = [
                (base_x, base_y),
                (base_x + radius, base_y - radius // 2),
                (base_x + radius * 2, base_y),
            ]
            for pos in positions:
                pygame.draw.circle(surface, (255, 255, 255), (int(pos[0]), int(pos[1])), radius)

        for bush in self.decorations.get("bushes", []):
            base_x = bush["x"] - self.offset_x
            base_y = bush.get("y", HEIGHT - 110)
            width = bush.get("width", 120)
            color = bush.get("color", (60, 160, 80))
            rect = pygame.Rect(base_x, base_y, width, 50)
            pygame.draw.ellipse(surface, color, rect)


class LevelManager:
    """Coordinates progression through multiple levels."""

    def __init__(self, player: Player):
        self.player = player
        self.levels = LEVEL_DATA
        self.current_index = 0
        self.level: Optional[Level] = None
        self.transition_timer = 0
        self.transition_text = ""
        self.final_victory = False
        self.load_level(0)

    def load_level(self, index: int) -> None:
        self.current_index = index
        self.level = Level(self.player, self.levels[self.current_index])
        self.transition_text = self.level.name
        self.transition_timer = 90

    def update(self, keys: pygame.key.ScancodeWrapper) -> bool:
        if self.final_victory or self.level is None:
            return self.final_victory

        self.level.update(keys)

        if self.level.check_win():
            if self.current_index + 1 < len(self.levels):
                self.load_level(self.current_index + 1)
            else:
                self.final_victory = True
                return True

        return False

    def draw(self, surface: pygame.Surface) -> None:
        if self.level is None:
            return

        self.level.draw(surface)

        if self.transition_timer > 0:
            self.transition_timer -= 1

    def reset(self) -> None:
        """Restart the campaign from the first level."""
        self.final_victory = False
        self.load_level(0)


def draw_hud(surface: pygame.Surface, title_font: pygame.font.Font, small_font: pygame.font.Font, manager: LevelManager) -> None:
    """Draw level information and instructions."""
    if manager.level is None:
        return

    level_label = small_font.render(
        f"Level {manager.current_index + 1}: {manager.level.name}", True, (30, 30, 30)
    )
    surface.blit(level_label, (20, 20))

    instructions = small_font.render(
        "←/→ move (backtrack), ↑ jump, space also jumps, R restart", True, (30, 30, 30)
    )
    surface.blit(instructions, (20, 50))

    if manager.transition_timer > 0:
        alpha = max(0, min(255, int(255 * (manager.transition_timer / 90))))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(alpha * 0.4)))
        surface.blit(overlay, (0, 0))
        title = title_font.render(manager.transition_text, True, (255, 255, 255))
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
        surface.blit(title, title_rect)
        sub = small_font.render("Reach the flag to advance!", True, (230, 230, 230))
        sub_rect = sub.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
        surface.blit(sub, sub_rect)


def draw_victory(surface: pygame.Surface, font: pygame.font.Font, small_font: pygame.font.Font) -> None:
    """Display the victory overlay when all levels are cleared."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    surface.blit(overlay, (0, 0))

    text = font.render("You Win!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    surface.blit(text, text_rect)

    prompt = small_font.render("Press R to play again.", True, (240, 240, 240))
    prompt_rect = prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
    surface.blit(prompt, prompt_rect)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Platformer Adventure")
    clock = pygame.time.Clock()

    player = Player((100, HEIGHT - 200))
    level_manager = LevelManager(player)
    title_font = pygame.font.SysFont(None, 64)
    hud_font = pygame.font.SysFont(None, 28)

    running = True
    final_victory = False
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                level_manager.reset()
                final_victory = False

        keys = pygame.key.get_pressed()

        if not final_victory:
            if level_manager.update(keys):
                final_victory = True

        level_manager.draw(screen)
        draw_hud(screen, title_font, hud_font, level_manager)

        if final_victory:
            draw_victory(screen, title_font, hud_font)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
