import pygame
from shapes import CircleShape
from constants import SHOT_RADIUS

class Shot(CircleShape):
    # This will be set in your game initialization
    # Similar to how you likely set up containers for asteroids
    containers = None

    def __init__(self, x, y, velocity):
        # Call the parent constructor which will add this to containers
        super().__init__(x, y, SHOT_RADIUS)
        # Set the velocity for the shot
        self.velocity = velocity

    def draw(self, screen):
        # Draw a filled circle for the shot
        pygame.draw.circle(
            screen,
            (255, 255, 255),          # White color
            (int(self.position.x), int(self.position.y)),
            self.radius
        )

    def update(self, dt):
        # Move in a straight line
        self.position += self.velocity * dt
