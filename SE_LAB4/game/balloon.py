import pygame


class Balloon:
    def __init__(self, x, y, radius, speed, balloon_type="normal"):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.balloon_type = balloon_type

        if balloon_type == "normal":
            self.color = (220, 90, 120)
            self.points = 10
        elif balloon_type == "bonus":
            self.color = (80, 200, 100)
            self.points = 25
        elif balloon_type == "penalty":
            self.color = (220, 60, 60)
            self.points = -10

    def update(self):
        self.y += self.speed

    def is_past_bottom(self, height):
        return self.y - self.radius > height

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )