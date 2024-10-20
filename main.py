import pygame
import random
import cv2
import numpy as np

# Constants
WIDTH, HEIGHT = 800, 600
CIRCLE_RADIUS = 250
CIRCLE_CENTER = (WIDTH // 2, HEIGHT // 2)
BALL_RADIUS = 15
FPS = 60
VIDEO_LENGTH = 60  # in seconds
VIDEO_FPS = 30  # frames per second for video

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Ball class
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.choice([-5, 5])
        self.vy = random.choice([-5, 5])

    def move(self):
        self.x += self.vx
        self.y += self.vy
        # Check for collision with the circle
        if (self.x - CIRCLE_CENTER[0]) ** 2 + (self.y - CIRCLE_CENTER[1]) ** 2 > (CIRCLE_RADIUS - BALL_RADIUS) ** 2:
            # Reflect the ball's direction
            self.vx = -self.vx
            self.vy = -self.vy

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Balls Inside a Circle")
clock = pygame.time.Clock()

# Generate random number and create balls
random_number = random.randint(1, 6)
balls = [Ball(random.randint(CIRCLE_CENTER[0] - CIRCLE_RADIUS + BALL_RADIUS,
                             CIRCLE_CENTER[0] + CIRCLE_RADIUS - BALL_RADIUS),
               random.randint(CIRCLE_CENTER[1] - CIRCLE_RADIUS + BALL_RADIUS,
                             CIRCLE_CENTER[1] + CIRCLE_RADIUS - BALL_RADIUS)) for _ in range(random_number)]

# Set up video recording
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_writer = cv2.VideoWriter('bouncing_balls.avi', fourcc, VIDEO_FPS, (WIDTH, HEIGHT))

# Main loop
frame_count = VIDEO_LENGTH * VIDEO_FPS
running = True
while running and frame_count > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Draw the white circle
    pygame.draw.circle(screen, WHITE, CIRCLE_CENTER, CIRCLE_RADIUS, 0)

    # Update and draw balls
    for ball in balls:
        ball.move()
        pygame.draw.circle(screen, RED, (int(ball.x), int(ball.y)), BALL_RADIUS)

    # Record the current frame
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
