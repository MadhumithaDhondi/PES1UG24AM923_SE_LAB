import random
import pygame

from game.balloon import Balloon
from game.click_detection import check_pop
from game.renderer import WIDTH, HEIGHT


SPAWN_INTERVAL_FRAMES = 45
GAME_DURATION_SECONDS = 30


class GameEngine:
    def __init__(self):
        self.balloons = []
        self.frames_until_spawn = 0
        self.score = 0
        self.lives = 3
        self.game_over = False

        self.start_time = pygame.time.get_ticks()
        self.time_remaining = GAME_DURATION_SECONDS

    def _spawn_balloon(self):
        if self.game_over:
            return

        radius = random.randint(16, 44)
        x = random.randint(radius + 10, WIDTH - radius - 10)
        speed = random.uniform(1.5, 3.0)

        balloon_type = random.choice(["normal", "bonus", "penalty"])

        self.balloons.append(
            Balloon(
                x=x,
                y=-radius,
                radius=radius,
                speed=speed,
                balloon_type=balloon_type,
            )
        )

    def handle_click(self, pos):
        if self.game_over:
            return

        popped = check_pop(self.balloons, pos)

        if popped is not None:
            self.balloons.remove(popped)
            self.score += popped.points

    def update(self):
        if self.game_over:
            return

        elapsed_seconds = (pygame.time.get_ticks() - self.start_time) / 1000
        self.time_remaining = max(
            0,
            GAME_DURATION_SECONDS - int(elapsed_seconds)
        )

        if self.time_remaining <= 0:
            self.time_remaining = 0
            self.game_over = True
            self.balloons = []
            return

        self.frames_until_spawn -= 1

        if self.frames_until_spawn <= 0:
            self._spawn_balloon()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for b in self.balloons:
            b.update()

        remaining_balloons = []

        for b in self.balloons:
            if b.is_past_bottom(HEIGHT):
                self.lives -= 1
            else:
                remaining_balloons.append(b)

        self.balloons = remaining_balloons

        if self.lives <= 0:
            self.lives = 0
            self.game_over = True
            self.balloons = []

    def reset(self):
        self.balloons = []
        self.frames_until_spawn = 0
        self.score = 0
        self.lives = 3
        self.game_over = False

        self.start_time = pygame.time.get_ticks()
        self.time_remaining = GAME_DURATION_SECONDS

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(surface, self.balloons)

        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 10),
        )

        renderer.draw_text(
            surface,
            font,
            f"Lives: {self.lives}",
            (10, 40),
        )

        renderer.draw_text(
            surface,
            font,
            f"Time: {self.time_remaining}",
            (10, 70),
        )

        if self.game_over:
            renderer.draw_text(
                surface,
                font,
                "GAME OVER",
                (WIDTH // 2 - 70, HEIGHT // 2),
            )

            renderer.draw_text(
                surface,
                font,
                f"Final Score: {self.score}",
                (WIDTH // 2 - 90, HEIGHT // 2 + 35),
            )

            renderer.draw_text(
                surface,
                font,
                "Press R to restart",
                (WIDTH // 2 - 100, HEIGHT // 2 + 70),
            )