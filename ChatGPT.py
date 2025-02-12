import pygame
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Rotating Hexagon")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Physics constants
GRAVITY = 0.2
FRICTION = 0.99

# Hexagon properties
hex_radius = 200
hex_center = (WIDTH // 2, HEIGHT // 2)
rotation_speed = 1  # Degrees per frame
angle = 0

# Ball properties
ball_radius = 10
ball_pos = [WIDTH // 2, HEIGHT // 2 - hex_radius + ball_radius]
ball_vel = [2, 0]

clock = pygame.time.Clock()
running = True


def get_hexagon_points(center, radius, angle):
    points = []
    for i in range(6):
        theta = math.radians(angle + i * 60)
        x = center[0] + radius * math.cos(theta)
        y = center[1] + radius * math.sin(theta)
        points.append((x, y))
    return points


def reflect_velocity(velocity, normal):
    dot_product = velocity[0] * normal[0] + velocity[1] * normal[1]
    reflected = [
        velocity[0] - 2 * dot_product * normal[0],
        velocity[1] - 2 * dot_product * normal[1]
    ]
    return [reflected[0] * FRICTION, reflected[1] * FRICTION]


while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Rotate hexagon
    angle += rotation_speed
    hex_points = get_hexagon_points(hex_center, hex_radius, angle)

    # Update ball physics
    ball_vel[1] += GRAVITY  # Apply gravity
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Check for collisions with hexagon walls
    for i in range(6):
        p1 = hex_points[i]
        p2 = hex_points[(i + 1) % 6]

        edge_vector = (p2[0] - p1[0], p2[1] - p1[1])
        edge_length = math.sqrt(edge_vector[0] ** 2 + edge_vector[1] ** 2)
        edge_normal = (-edge_vector[1] / edge_length, edge_vector[0] / edge_length)

        ball_to_edge = (ball_pos[0] - p1[0], ball_pos[1] - p1[1])
        distance_to_edge = abs(ball_to_edge[0] * edge_normal[0] + ball_to_edge[1] * edge_normal[1])

        if distance_to_edge < ball_radius:
            ball_vel = reflect_velocity(ball_vel, edge_normal)
            overlap = ball_radius - distance_to_edge
            ball_pos[0] += edge_normal[0] * overlap
            ball_pos[1] += edge_normal[1] * overlap

    # Draw hexagon
    pygame.draw.polygon(screen, WHITE, hex_points, 2)

    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
