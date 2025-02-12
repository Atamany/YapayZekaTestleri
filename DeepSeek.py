import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Rotating Hexagon")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Hexagon properties
hexagon_radius = 200
hexagon_center = (WIDTH // 2, HEIGHT // 2)
hexagon_angle = 0  # Rotation angle in degrees
hexagon_rotation_speed = 1  # Degrees per frame

# Ball properties
ball_radius = 20
ball_position = [hexagon_center[0], hexagon_center[1] - hexagon_radius + ball_radius]
ball_velocity = [5, 0]  # Initial velocity (x, y)
gravity = 0.5
friction = 0.99

# Function to calculate hexagon vertices
def calculate_hexagon_vertices(center, radius, angle):
    vertices = []
    for i in range(6):
        x = center[0] + radius * math.cos(math.radians(60 * i + angle))
        y = center[1] + radius * math.sin(math.radians(60 * i + angle))
        vertices.append((x, y))
    return vertices

# Function to check if a point is inside a polygon
def point_inside_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

# Function to reflect the ball's velocity off a wall
def reflect_velocity(velocity, normal):
    dot_product = velocity[0] * normal[0] + velocity[1] * normal[1]
    velocity[0] -= 2 * dot_product * normal[0]
    velocity[1] -= 2 * dot_product * normal[1]
    return velocity

# Main loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update hexagon rotation
    hexagon_angle += hexagon_rotation_speed
    if hexagon_angle >= 360:
        hexagon_angle -= 360

    # Calculate hexagon vertices
    hexagon_vertices = calculate_hexagon_vertices(hexagon_center, hexagon_radius, hexagon_angle)

    # Update ball position and velocity
    ball_velocity[1] += gravity  # Apply gravity
    ball_position[0] += ball_velocity[0]
    ball_position[1] += ball_velocity[1]

    # Check for collisions with hexagon walls
    if not point_inside_polygon(ball_position, hexagon_vertices):
        # Find the closest wall and reflect the ball's velocity
        closest_distance = float('inf')
        closest_normal = (0, 0)
        for i in range(6):
            p1 = hexagon_vertices[i]
            p2 = hexagon_vertices[(i + 1) % 6]
            edge = (p2[0] - p1[0], p2[1] - p1[1])
            normal = (-edge[1], edge[0])
            length = math.hypot(normal[0], normal[1])
            normal = (normal[0] / length, normal[1] / length)

            # Calculate distance from ball to wall
            distance = abs((p2[0] - p1[0]) * (p1[1] - ball_position[1]) - (p1[0] - ball_position[0]) * (p2[1] - p1[1])) / math.hypot(p2[0] - p1[0], p2[1] - p1[1])

            if distance < closest_distance:
                closest_distance = distance
                closest_normal = normal

        # Reflect the ball's velocity
        ball_velocity = reflect_velocity(ball_velocity, closest_normal)

        # Move the ball back inside the hexagon
        ball_position[0] += closest_normal[0] * (ball_radius - closest_distance)
        ball_position[1] += closest_normal[1] * (ball_radius - closest_distance)

    # Apply friction
    ball_velocity[0] *= friction
    ball_velocity[1] *= friction

    # Clear the screen
    screen.fill(WHITE)

    # Draw the hexagon
    pygame.draw.polygon(screen, BLACK, hexagon_vertices, 2)

    # Draw the ball
    pygame.draw.circle(screen, RED, (int(ball_position[0]), int(ball_position[1])), ball_radius)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()