import pygame
import math

# Initialize pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball in Rotating Hexagon")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Ball properties
ball_radius = 15
ball_x = width // 2
ball_y = height // 2
ball_speed_x = 5
ball_speed_y = 5
gravity = 0.2

# Hexagon properties
hexagon_sides = 6
hexagon_radius = 200
hexagon_rotation_speed = 0.02

# Friction
friction = 0.99

# Function to calculate hexagon vertices
def get_hexagon_vertices(center_x, center_y, radius, rotation):
    vertices = []
    angle = math.radians(360 / hexagon_sides)
    for i in range(hexagon_sides):
        x = center_x + radius * math.cos(i * angle + rotation)
        y = center_y + radius * math.sin(i * angle + rotation)
        vertices.append((x, y))
    return vertices

# Function to check for line-circle intersection
def line_intersects_circle(start_point, end_point, circle_center, circle_radius):
    # Calculate line parameters
    x1, y1 = start_point
    x2, y2 = end_point
    dx = x2 - x1
    dy = y2 - y1

    # Calculate closest point on line to circle center
    t = ((circle_center[0] - x1) * dx + (circle_center[1] - y1) * dy) / (dx * dx + dy * dy)
    t = max(0, min(1, t))  # Clamp t to the line segment

    closest_x = x1 + t * dx
    closest_y = y1 + t * dy

    # Calculate distance from closest point to circle center
    distance = math.sqrt((closest_x - circle_center[0])**2 + (closest_y - circle_center[1])**2)

    # Check if distance is less than or equal to circle radius
    return distance <= circle_radius

# Game loop
running = True
clock = pygame.time.Clock()
rotation = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ball position
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    ball_speed_y += gravity

    # Apply friction
    ball_speed_x *= friction
    ball_speed_y *= friction

    # Check for collisions with hexagon walls
    hexagon_vertices = get_hexagon_vertices(width // 2, height // 2, hexagon_radius, rotation)
    for i in range(hexagon_sides):
        start_point = hexagon_vertices[i]
        end_point = hexagon_vertices[(i + 1) % hexagon_sides]
        if line_intersects_circle(start_point, end_point, (ball_x, ball_y), ball_radius):
            # Calculate normal vector
            normal_x = end_point[1] - start_point[1]
            normal_y = -(end_point[0] - start_point[0])
            normal_length = math.sqrt(normal_x**2 + normal_y**2)
            normal_x /= normal_length
            normal_y /= normal_length

            # Calculate reflection
            dot_product = ball_speed_x * normal_x + ball_speed_y * normal_y
            ball_speed_x -= 2 * dot_product * normal_x
            ball_speed_y -= 2 * dot_product * normal_y

    # Rotate hexagon
    rotation += hexagon_rotation_speed

    # Draw
    screen.fill(BLACK)
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)
    pygame.draw.polygon(screen, WHITE, hexagon_vertices)
    pygame.display.flip()

    # Cap frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()