from shapes import CircleShape
from constants import *  # This imports all constants including ASTEROID_MIN_RADIUS
import pygame
import random  # Make sure to add this import

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        # Call the parent constructor
        super().__init__(x, y, radius)
        # Any additional initialization can go here

    def draw(self, surface):
        # Draw a circle with position, radius and width of 2
        pygame.draw.circle(
            surface,                  # Surface to draw on
            (255, 255, 255),          # Color (white in this case)
            (int(self.position.x), int(self.position.y)),  # Position (x, y)
            self.radius,              # Radius of the circle
            2                         # Width of 2 (outline only)
        )

    def update(self, dt):
        # Move in a straight line by adding (velocity * dt) to position
        self.position += self.velocity * dt
        
    def split(self):
        self.kill()  # This asteroid is always destroyed
        
        # Check if asteroid is too small to split
        if self.radius <= ASTEROID_MIN_RADIUS:
            return  # Too small, don't spawn new asteroids
        
        # Generate random angle between 20 and 50 degrees
        random_angle = random.uniform(20, 50)
        
        # Create two new velocity vectors
        velocity1 = self.velocity.rotate(random_angle)
        velocity2 = self.velocity.rotate(-random_angle)
        
        # Compute new radius
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        
        # Create two new asteroids
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        
        # Set velocities and make them faster
        asteroid1.velocity = velocity1 * 1.2
        asteroid2.velocity = velocity2 * 1.2
