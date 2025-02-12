import pygame
import math
import sys

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.5
FRICTION = 0.99
HEXAGON_RADIUS = 200
BALL_RADIUS = 10

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Ball properties
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [5, 0]

# Hexagon rotation
angle = 0
rotation_speed = 1  # degrees per frame

def draw_hexagon(surface, center, radius, angle):
    points = []
    for i in range(6):
        theta = math.radians(angle + i * 60)
        x = center[0] + radius * math.cos(theta)
        y = center[1] + radius * math.sin(theta)
        points.append((x, y))
    pygame.draw.polygon(surface, (255, 255, 255), points, 2)

def check_collision(ball_pos, ball_vel):
    # Calculate the distance from the center of the hexagon
    center = (WIDTH // 2, HEIGHT // 2)
    distance = math.sqrt((ball_pos[0] - center[0]) ** 2 + (ball_pos[1] - center[1]) ** 2)

    if distance + BALL_RADIUS > HEXAGON_RADIUS:
        # Calculate the normal vector at the point of collision
        normal_x = (ball_pos[0] - center[0]) / distance
        normal_y = (ball_pos[1] - center[1]) / distance

        # Reflect the ball's velocity
        dot_product = ball_vel[0] * normal_x + ball_vel[1] * normal_y
        ball_vel[0] -= 2 * dot_product * normal_x
        ball_vel[1] -= 2 * dot_product * normal_y

        # Apply friction
        ball_vel[0] *= FRICTION
        ball_vel[1] *= FRICTION

        # Move the ball back inside the hexagon
        overlap = (distance + BALL_RADIUS) - HEXAGON_RADIUS
        ball_pos[0] -= normal_x * overlap
        ball_pos[1] -= normal_y * overlap

def main():
    global angle
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update ball position
        ball_vel[1] += GRAVITY  # Apply gravity
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]

        # Check for collisions with the hexagon
        check_collision(ball_pos, ball_vel)

        # Rotate the hexagon
        angle += rotation_speed
        if angle >= 360:
            angle -= 360

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the rotating hexagon
        draw_hexagon(screen, (WIDTH // 2, HEIGHT // 2), HEXAGON_RADIUS, angle)

        # Draw the ball
        pygame.draw.circle(screen, (255, 0, 0), (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()