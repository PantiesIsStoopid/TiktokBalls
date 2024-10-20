import pygame
import random
import cv2
import numpy as np
import math

# Constants
WIDTH, HEIGHT = 800, 600
CIRCLE_RADIUS = 250
CIRCLE_CENTER = (WIDTH // 2, HEIGHT // 2)
BALL_RADIUS = 15
FPS = 60
VIDEO_LENGTH = 60  # in seconds
VIDEO_FPS = 60  # frames per second for video

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Rainbow colors
RAINBOW_COLORS = [
    (255, 0, 0),  # Red
    (255, 127, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (75, 0, 130),  # Indigo
    (148, 0, 211),  # Violet
]

# Physics constants
BOUNCINESS = 1.0  # No loss of energy during collisions
GRAVITY = 0.1  # Optional gravity, can be removed if no gravity is needed

# Initialize pygame and sound system
pygame.init()
pygame.mixer.init()

# Load collision sound
collision_sound = pygame.mixer.Sound("collision_sound.wav")


# Ball class
class Ball:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        # Generate random velocity in random direction
        speed = random.uniform(2, 5)  # Random speed between 2 and 5
        angle = random.uniform(0, 2 * math.pi)  # Random angle in radians
        self.x_speed = speed * math.cos(angle)
        self.y_speed = speed * math.sin(angle)
        self.color = random.choice(RAINBOW_COLORS)

    def draw(self):
        pygame.draw.circle(
            screen, self.color, (int(self.x_pos), int(self.y_pos)), BALL_RADIUS
        )

    def update_pos(self):
        # Apply gravity (optional, can be removed if you don't want gravity)
        self.y_speed += GRAVITY

        # Update position
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed

        # Check for collision with the circular boundary
        self.check_circle_collision()

        # Collision with walls (left/right boundaries)
        if self.x_pos < BALL_RADIUS or self.x_pos > WIDTH - BALL_RADIUS:
            self.x_speed *= -BOUNCINESS  # Reverse speed and apply bounciness
            collision_sound.play()  # Play sound on wall collision

        # Collision with floor/ceiling (top/bottom boundaries)
        if self.y_pos < BALL_RADIUS or self.y_pos > HEIGHT - BALL_RADIUS:
            self.y_speed *= -BOUNCINESS  # Reverse speed and apply bounciness
            collision_sound.play()  # Play sound on floor/ceiling collision

    def check_circle_collision(self):
        # Calculate distance from the center of the circle
        distance = math.sqrt(
            (self.x_pos - CIRCLE_CENTER[0]) ** 2 + (self.y_pos - CIRCLE_CENTER[1]) ** 2
        )

        # Check if the ball is outside the circle
        if distance > (CIRCLE_RADIUS - BALL_RADIUS):
            # Calculate the reflection vector
            angle = math.atan2(
                self.y_pos - CIRCLE_CENTER[1], self.x_pos - CIRCLE_CENTER[0]
            )
            self.x_speed = (
                -self.x_speed * BOUNCINESS
            )  # Reverse x-speed and apply bounciness
            self.y_speed = (
                -self.y_speed * BOUNCINESS
            )  # Reverse y-speed and apply bounciness

            # Move the ball back inside the circle to avoid clipping
            overlap = distance - (CIRCLE_RADIUS - BALL_RADIUS)
            self.x_pos -= overlap * math.cos(angle)
            self.y_pos -= overlap * math.sin(angle)

            # Play sound on circle collision
            collision_sound.play()


# Initialize pygame display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Balls with No Energy Loss and Sound")
clock = pygame.time.Clock()

# Generate random number and create balls with random velocity
random_number = random.randint(1, 6)
balls = [
    Ball(
        random.randint(
            CIRCLE_CENTER[0] - CIRCLE_RADIUS + BALL_RADIUS,
            CIRCLE_CENTER[0] + CIRCLE_RADIUS - BALL_RADIUS,
        ),
        random.randint(
            CIRCLE_CENTER[1] - CIRCLE_RADIUS + BALL_RADIUS,
            CIRCLE_CENTER[1] + CIRCLE_RADIUS - BALL_RADIUS,
        ),
    )
    for _ in range(random_number)
]

# Set up video recording
fourcc = cv2.VideoWriter_fourcc(*"XVID")
video_writer = cv2.VideoWriter(
    "bouncing_balls_with_sound.avi", fourcc, VIDEO_FPS, (WIDTH, HEIGHT)
)

# Main loop
frame_count = VIDEO_LENGTH * VIDEO_FPS
running = True
while running and frame_count > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Draw the white circle
    pygame.draw.circle(screen, WHITE, CIRCLE_CENTER, CIRCLE_RADIUS)

    # Update and draw all the balls
    for ball in balls:
        ball.update_pos()
        ball.draw()

    # Record the current frame for video output
    frame = pygame.surfarray.array3d(pygame.display.get_surface())
    frame = np.rot90(frame)  # Rotate frame for correct orientation
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert to BGR format
    video_writer.write(frame)

    pygame.display.flip()
    clock.tick(FPS)
    frame_count -= 1

# Cleanup
video_writer.release()
pygame.quit()
