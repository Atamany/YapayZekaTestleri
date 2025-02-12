import pygame
import math
import sys

# Pygame başlatma
pygame.init()

# Ekran boyutları
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dönen Altıgen İçinde Zıplayan Top")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Top özellikleri
ball_radius = 10
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [0, 0]
gravity = 0.5
friction = 0.8

# Altıgen özellikleri
hexagon_radius = 200
rotation_angle = 0
rotation_speed = 0.02


def get_hexagon_points(angle):
    points = []
    for i in range(6):
        point_angle = angle + (i * math.pi / 3)
        x = WIDTH // 2 + hexagon_radius * math.cos(point_angle)
        y = HEIGHT // 2 + hexagon_radius * math.sin(point_angle)
        points.append((x, y))
    return points


def check_collision(ball_pos, hexagon_points):
    for i in range(len(hexagon_points)):
        p1 = hexagon_points[i]
        p2 = hexagon_points[(i + 1) % 6]

        # Duvar vektörü
        wall_vector = [p2[0] - p1[0], p2[1] - p1[1]]
        wall_length = math.sqrt(wall_vector[0] ** 2 + wall_vector[1] ** 2)
        wall_normal = [-wall_vector[1] / wall_length, wall_vector[0] / wall_length]

        # Top ile duvar arasındaki mesafe
        to_ball = [ball_pos[0] - p1[0], ball_pos[1] - p1[1]]
        distance = abs(to_ball[0] * wall_normal[0] + to_ball[1] * wall_normal[1])

        if distance < ball_radius:
            # Çarpışma tepkisi
            dot_product = ball_vel[0] * wall_normal[0] + ball_vel[1] * wall_normal[1]
            ball_vel[0] = friction * (ball_vel[0] - 2 * dot_product * wall_normal[0])
            ball_vel[1] = friction * (ball_vel[1] - 2 * dot_product * wall_normal[1])

            # Topun konumunu düzeltme
            correction = ball_radius - distance
            ball_pos[0] += wall_normal[0] * correction
            ball_pos[1] += wall_normal[1] * correction


clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Top fiziği güncelleme
    ball_vel[1] += gravity
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Altıgen rotasyonu
    rotation_angle += rotation_speed
    hexagon_points = get_hexagon_points(rotation_angle)

    # Çarpışma kontrolü
    check_collision(ball_pos, hexagon_points)

    # Çizim
    screen.fill(BLACK)

    # Altıgeni çiz
    pygame.draw.polygon(screen, WHITE, hexagon_points, 2)

    # Topu çiz
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    pygame.display.flip()
    clock.tick(60)