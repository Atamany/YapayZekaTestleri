import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
HEX_RADIUS = 200
BALL_RADIUS = 10
GRAVITY = 0.5
FRICTION = 0.99
ROTATION_SPEED = 1  # Degrees per frame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bouncing Ball in Rotating Hexagon')

# Hexagon vertices
def hexagon_vertices(center, radius, angle):
    vertices = []
    for i in range(6):
        theta = math.radians(angle + i * 60)
        x = center[0] + radius * math.cos(theta)
        y = center[1] + radius * math.sin(theta)
        vertices.append((x, y))
    return vertices

# Ball class
class Ball:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def update(self):
        self.vy += GRAVITY  # Apply gravity
        self.vx *= FRICTION  # Apply friction
        self.vy *= FRICTION
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), BALL_RADIUS)

# Main loop
running = True
clock = pygame.time.Clock()
ball = Ball(WIDTH // 2, HEIGHT // 2, 2, -5)
center = (WIDTH // 2, HEIGHT // 2)
angle = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ball
    ball.update()

    # Rotate hexagon
    angle += ROTATION_SPEED
    hex_vertices = hexagon_vertices(center, HEX_RADIUS, angle)

    # Ball collision with hexagon walls
    for i in range(6):
        x1, y1 = hex_vertices[i]
        x2, y2 = hex_vertices[(i + 1) % 6]
        dx, dy = x2 - x1, y2 - y1
        length = math.hypot(dx, dy)
        nx, ny = -dy / length, dx / length
        p = (ball.x - x1) * nx + (ball.y - y1) * ny
        if p < BALL_RADIUS and (ball.x - x1) * (ball.x - x2) + (ball.y - y1) * (ball.y - y2) < 0:
            overlap = BALL_RADIUS - p
            ball.x += nx * overlap
            ball.y += ny * overlap
            ball.vx, ball.vy = ball.vx - 2 * (ball.vx * nx + ball.vy * ny) * nx, ball.vy - 2 * (ball.vx * nx + ball.vy * ny) * ny

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.polygon(screen, WHITE, hex_vertices, 1)
    ball.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
