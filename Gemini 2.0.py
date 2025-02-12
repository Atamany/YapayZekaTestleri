import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Rotating Hexagon")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Ball properties
ball_radius = 15
ball_color = RED
ball_start_pos = [WIDTH // 2, HEIGHT // 2 - 100]
ball_pos = list(ball_start_pos)  # Use list for mutability
ball_velocity = [2, 2]  # Initial velocity (x, y)
gravity = 0.15
friction = 0.01
elasticity = 0.8  # Energy retention on bounce

# Hexagon properties
hexagon_center = [WIDTH // 2, HEIGHT // 2]
hexagon_size = 150
hexagon_color = BLUE
hexagon_rotation_speed = 0.01  # Radians per frame
hexagon_rotation_angle = 0

def get_hexagon_vertices(center_x, center_y, size, rotation_angle):
    """Calculates the vertices of a regular hexagon."""
    vertices = []
    for i in range(6):
        angle_rad = math.radians(60 * i) + rotation_angle
        x = center_x + size * math.cos(angle_rad)
        y = center_y + size * math.sin(angle_rad)
        vertices.append((int(x), int(y)))
    return vertices

def draw_hexagon(surface, vertices, color):
    """Draws the hexagon on the surface."""
    pygame.draw.polygon(surface, color, vertices, 2) # 2 for border width

def distance_point_segment(point, segment_p1, segment_p2):
    """
    Calculates the shortest distance from a point to a line segment.
    Based on: http://geomalgorithms.com/a02-_1-C.html
    """
    x0, y0 = point
    x1, y1 = segment_p1
    x2, y2 = segment_p2

    l2 = ((x1 - x2)**2) + ((y1 - y2)**2)  # i.e. |v|^2 -  avoid a sqrt
    if l2 == 0.0:
        return math.sqrt((x0-x1)**2 + (y0-y1)**2)   # segment is a point

    # Consider the line extending the segment, parameterized as P = P1 + t * (P2 - P1).
    # We clamp t to be in the range [0, 1] to meet the segment.
    dx = x2 - x1
    dy = y2 - y1
    t = ((x0 - x1) * dx + (y0 - y1) * dy) / float(l2)
    t = max(0, min(1, t))
    projection_x = x1 + t * dx
    projection_y = y1 + t * dy

    return math.sqrt((x0 - projection_x)**2 + (y0 - projection_y)**2), (projection_x, projection_y)


def get_edge_normal(segment_p1, segment_p2):
    """Calculates the normal vector of a line segment, pointing outwards."""
    dx = segment_p2[0] - segment_p1[0]
    dy = segment_p2[1] - segment_p1[1]
    # Normal can be (-dy, dx) or (dy, -dx). We need to ensure it points outwards from the hexagon
    # For a regular hexagon centered at origin, normals point outwards in the general direction of vertices.
    # Let's use (-dy, dx) and we might need to flip if it's consistently inward facing in a complex scenario.
    return -dy, dx # Negate dy to generally point outwards from clockwise defined polygons


def reflect_velocity(ball_velocity, normal_vector):
    """Reflects the ball's velocity vector across a normal vector."""
    normal_x, normal_y = normal_vector
    ball_vx, ball_vy = ball_velocity

    # Normalize the normal vector
    normal_magnitude = math.sqrt(normal_x**2 + normal_y**2)
    if normal_magnitude == 0:
        return ball_velocity # Avoid division by zero if somehow normal is zero

    normalized_normal_x = normal_x / normal_magnitude
    normalized_normal_y = normal_y / normal_magnitude

    # Calculate dot product of ball velocity and normal vector
    dot_product = ball_vx * normalized_normal_x + ball_vy * normalized_normal_y

    # Reflection formula: v_reflected = v - 2 * (v . n) * n
    reflected_vx = ball_vx - 2 * dot_product * normalized_normal_x
    reflected_vy = ball_vy - 2 * dot_product * normalized_normal_y

    return [reflected_vx, reflected_vy]


# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Update hexagon rotation
    hexagon_rotation_angle += hexagon_rotation_speed

    # Get hexagon vertices
    hexagon_vertices = get_hexagon_vertices(hexagon_center[0], hexagon_center[1], hexagon_size, hexagon_rotation_angle)

    # Draw hexagon
    draw_hexagon(screen, hexagon_vertices, hexagon_color)

    # Apply gravity
    ball_velocity[1] += gravity

    # Apply friction (air resistance, simplified - reduces velocity in both directions)
    ball_velocity[0] *= (1 - friction)
    ball_velocity[1] *= (1 - friction)

    # Move the ball
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]

    # Bounce off screen edges
    if ball_pos[0] + ball_radius > WIDTH or ball_pos[0] - ball_radius < 0:
        ball_velocity[0] *= -elasticity
        if ball_pos[0] + ball_radius > WIDTH:
            ball_pos[0] = WIDTH - ball_radius
        else:
            ball_pos[0] = ball_radius
    if ball_pos[1] + ball_radius > HEIGHT or ball_pos[1] - ball_radius < 0:
        ball_velocity[1] *= -elasticity
        if ball_pos[1] + ball_radius > HEIGHT:
            ball_pos[1] = HEIGHT - ball_radius
        else:
            ball_pos[1] = ball_radius


    # Collision detection with hexagon edges
    for i in range(6):
        segment_start = hexagon_vertices[i]
        segment_end = hexagon_vertices[(i + 1) % 6] # Wrap around to first vertex for last segment

        distance, projection_point = distance_point_segment(ball_pos, segment_start, segment_end)

        if distance <= ball_radius:
            # Collision detected!
            normal = get_edge_normal(segment_start, segment_end)
            ball_velocity = reflect_velocity(ball_velocity, normal)

            # Correct ball position to be just outside the hexagon edge
            # Move ball along the normal away from the edge by the overlap distance
            overlap = ball_radius - distance
            normalized_normal_x = normal[0] / math.sqrt(normal[0]**2 + normal[1]**2) if math.sqrt(normal[0]**2 + normal[1]**2) != 0 else 0
            normalized_normal_y = normal[1] / math.sqrt(normal[0]**2 + normal[1]**2) if math.sqrt(normal[0]**2 + normal[1]**2) != 0 else 0

            ball_pos[0] += normalized_normal_x * overlap * 1.1  # 1.1 to ensure we move completely out and avoid sticking
            ball_pos[1] += normalized_normal_y * overlap * 1.1

            ball_velocity[0] *= elasticity # Apply elasticity on bounce
            ball_velocity[1] *= elasticity


    # Draw ball
    pygame.draw.circle(screen, ball_color, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    # Update display
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

pygame.quit()