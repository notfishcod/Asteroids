import pygame
import random
import sys
import time
from shot import Shot
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import *  # Assuming you have a constants.py file with your game constants

# Initialize pygame and the game screen
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroids")

# Create sprite groups
updatable = pygame.sprite.Group()
drawable = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
shots = pygame.sprite.Group()

# Set containers for classes
Player.containers = (updatable, drawable)
Asteroid.containers = (asteroids, updatable, drawable)
AsteroidField.containers = (updatable,)
Shot.containers = (shots, updatable, drawable)

# Create game objects
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, shots)
asteroid_field = AsteroidField()  # Create the asteroid field

# Create a clock to manage time
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    # Calculate time delta (frame duration in seconds)
    dt = clock.tick(60) / 1000.0

    # Handle events (e.g., quit events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update all sprites with appropriate parameters
    for sprite in updatable:
        if isinstance(sprite, Player):
            sprite.update(dt, SCREEN_WIDTH, SCREEN_HEIGHT)
        else:
            sprite.update(dt)

    # Update shots group
    shots.update(dt)

    # Check player-asteroid collisions
    if player:
        for asteroid in asteroids:
             if player.check_collision(asteroid):
                 print("Game over!")
                 player.kill()
                 time.sleep(1)
                 sys.exit()

    def split(self):
        self.kill() # This asteroid is always destroyed

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

    # Check bullet-asteroid collisions
    for asteroid in asteroids:
        for bullet in shots:
            if bullet.check_collision(asteroid):  # Use the same check_collision method
                asteroid.split()
                bullet.kill()

    # Clear the screen with black
    screen.fill((0, 0, 0))

    # Draw each sprite in the 'drawable' group
    for sprite in drawable:
        sprite.draw(screen)

    # Draw shots
    for shot in shots:
        shot.draw(screen)

    # Update the display
    pygame.display.flip()

# Cleanly end game
pygame.quit()
sys.exit()
