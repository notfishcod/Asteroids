import pygame  # Import pygame for handling graphics and input
from constants import *  # Import constants
from shapes import CircleShape
from shot import Shot

class Player(CircleShape):
    #Debug toggles False = off True = on
    show_hitbox = False


    def __init__(self, x, y, shots_group):
        super().__init__(x, y, PLAYER_RADIUS)  # Add the player automatically to its containers (groups)
        self.position = pygame.Vector2(x, y)
        self.rotation = 0
        self.shots_group = shots_group
        self.radius = PLAYER_RADIUS
        self.shoot_timer = 0  # Initialize the shooting cooldown timer

    def draw(self, screen):
        # Draw a hollow white triangle
        pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), width=1)

        # Draw the hitbox (circular collision boundary)
        if Player.show_hitbox:
            pygame.draw.circle(
                screen,
                (255, 0, 0),  # Red color for visibility
                (int(self.position.x), int(self.position.y)),
                self.radius,
                width=1  # Make it hollow
            )

    def triangle(self):
        # Create the player's triangular shape to represent it
        forward = pygame.Vector2(0, -1).rotate(self.rotation) * self.radius  # Tip of the triangle
        right = pygame.Vector2(-1, 0).rotate(self.rotation) * self.radius / 1.5  # Sides' offsets
        a = self.position + forward  # Tip of the triangle
        b = self.position - forward + right  # Bottom-left vertex
        c = self.position - forward - right  # Bottom-right vertex
        return [a.xy, b.xy, c.xy]

    def rotate(self, direction, dt):
        # Adjust rotation by PLAYER_TURN_SPEED scaled by time delta
        self.rotation = (self.rotation + direction * PLAYER_TURN_SPEED * dt) % 360

    def move(self, dt, screen_width, screen_height):
        # Movement logic for forward/backward motion
        forward = pygame.Vector2(0, -1).rotate(self.rotation)  # Rotate unit vector
        self.position += forward * PLAYER_SPEED * dt  # Move the position

        # Boundary wrapping logic (wraps to the other side if offscreen)
        self.position.x %= screen_width
        self.position.y %= screen_height

    def update(self, dt, screen_width, screen_height):
        # Handle user input to update the player's state
        keys = pygame.key.get_pressed()

        # Handle rotation and movement
        if keys[pygame.K_a]:  # Rotate left (counter-clockwise)
            self.rotate(-1, dt)
        if keys[pygame.K_d]:  # Rotate right (clockwise)
            self.rotate(1, dt)
        if keys[pygame.K_w]:  # Move forward
            self.move(dt, screen_width, screen_height)
        if keys[pygame.K_s]:  # Move backward
            self.move(-dt, screen_width, screen_height)
        if keys[pygame.K_SPACE]:  # Shoot
            self.shoot()

        # Decrease the shoot timer by dt
        if self.shoot_timer > 0:
            self.shoot_timer -= dt

    def shoot(self):
        # Only shoot if the cooldown timer is at or below 0
        if self.shoot_timer <= 0:
            # Set the shot's velocity
            shot_direction = pygame.Vector2(0, -1)  # Point upward
            shot_direction = shot_direction.rotate(self.rotation)
            shot_direction *= PLAYER_SHOOT_SPEED

            # Create a new shot with position AND velocity passed directly
            new_shot = Shot(self.position.x, self.position.y, shot_direction)
            # Add the shot to the shots group
            self.shots_group.add(new_shot)

            # Reset the timer to the cooldown value
            self.shoot_timer = PLAYER_SHOOT_COOLDOWN
