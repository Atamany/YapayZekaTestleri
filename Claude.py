import pygame
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Physics constants
GRAVITY = 0.5
ELASTICITY = 0.8
FRICTION = 0.99
ROTATION_SPEED = 0.02


class Ball:
    def __init__(self, x, y, radius):
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.array([0.0, 0.0])
        self.radius = radius

    def update(self):
        # Apply gravity
        self.vel[1] += GRAVITY

        # Apply friction
        self.vel *= FRICTION

        # Update position
        self.pos += self.vel


class Hexagon:
    def __init__(self, center_x, center_y, radius):
        self.center = np.array([center_x, center_y])
        self.radius = radius
        self.angle = 0

    def get_vertices(self):
        vertices = []
        for i in range(6):
            angle = self.angle + i * math.pi / 3
            x = self.center[0] + self.radius * math.cos(angle)
            y = self.center[1] + self.radius * math.sin(angle)
            vertices.append(np.array([x, y]))
        return vertices

    def get_edges(self):
        vertices = self.get_vertices()
        edges = []
        for i in range(6):
            edges.append((vertices[i], vertices[(i + 1) % 6]))
        return edges

    def rotate(self):
        self.angle += ROTATION_SPEED


def line_segment_normal(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return np.array([-dy, dx]) / np.sqrt(dx * dx + dy * dy)


def check_collision(ball, hexagon):
    edges = hexagon.get_edges()

    for p1, p2 in edges:
        # Vector from p1 to ball
        v = ball.pos - p1
        # Vector from p1 to p2
        edge = p2 - p1
        # Length of edge
        edge_length = np.linalg.norm(edge)
        # Normalized edge vector
        edge_normalized = edge / edge_length

        # Project v onto edge
        proj_length = np.dot(v, edge_normalized)

        if 0 <= proj_length <= edge_length:
            # Find closest point on line
            closest = p1 + edge_normalized * proj_length
            # Distance from ball to line
            dist = np.linalg.norm(ball.pos - closest)

            if dist < ball.radius:
                # Calculate normal vector
                normal = line_segment_normal(p1, p2)
                # Ensure normal points towards ball
                if np.dot(normal, ball.pos - closest) < 0:
                    normal = -normal

                # Move ball out of collision
                ball.pos = closest + normal * ball.radius

                # Calculate reflection
                rel_vel = ball.vel
                normal_vel = np.dot(rel_vel, normal) * normal
                tangent_vel = rel_vel - normal_vel

                # Apply elasticity and friction
                ball.vel = tangent_vel * FRICTION - normal_vel * ELASTICITY


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bouncing Ball in Rotating Hexagon")
    clock = pygame.time.Clock()

    ball = Ball(WIDTH // 2, HEIGHT // 2, 10)
    hexagon = Hexagon(WIDTH // 2, HEIGHT // 2, 200)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Reset ball position and give it random velocity
                ball.pos = np.array(pygame.mouse.get_pos(), dtype=float)
                ball.vel = np.array([np.random.uniform(-10, 10), np.random.uniform(-10, 10)])

        # Update
        ball.update()
        hexagon.rotate()
        check_collision(ball, hexagon)

        # Draw
        screen.fill(BLACK)

        # Draw hexagon
        vertices = hexagon.get_vertices()
        pygame.draw.polygon(screen, WHITE, vertices, 2)

        # Draw ball
        pygame.draw.circle(screen, RED, ball.pos.astype(int), ball.radius)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()